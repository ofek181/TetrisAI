import os
import sys
import tensorflow as tf
import numpy as np
from model import DeepQNetwork
from memory import ExperienceBuffer
from tetris.api import Environment
from datetime import datetime
import matplotlib.pyplot as plt
from consts import GameConsts, Action

global start_time, times

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, ROOT_DIR)


class Agent:
    def __init__(self, max_step: int = 1000):
        tf.compat.v1.reset_default_graph()
        self.model = DeepQNetwork()
        self.saver = tf.compat.v1.train.Saver()
        self.session = tf.compat.v1.Session()
        self.max_step = max_step
        self.sum_of_scores = 0
        self.mean_scores = []

    def load_model(self, name: str):
        save_path = os.path.join(ROOT_DIR, 'trained_model', name)
        self.saver.restore(self.session, save_path)

    def _save_model(self, name: str):
        save_path = os.path.join(ROOT_DIR, 'trained_model', name)
        self.saver.save(self.session, save_path)

    def _take_scores(self, i: int, num_steps: int, e: float, max_step: int, name: str):
        global start_time
        global times
        times = 1000
        if i % times == 0:
            mean = self.sum_of_scores / times
            self.mean_scores.append(mean)
            self.sum_of_scores = 0
            print("Episode: {0}, Score: {1}, Exploration: {2}, Max step: {3}".format(i, mean, e, max_step))
            self._save_model(name)

        if i % 100 == 0:
            end_time = datetime.now()
            time_difference = (end_time - start_time).total_seconds()
            print("Episode: {0} out of: {1} Episodes, Time: {2}".format(i, num_steps, time_difference))
            start_time = datetime.now()

    # @staticmethod
    # def helper_reward(state) -> int:
    #     reward = 0
    #     state = state.tolist()
    #     for idx, line in enumerate(state):
    #         idx += 1
    #         new_reward = line.count(1) * idx // GameConsts.GRID_HEIGHT
    #         if new_reward > reward:
    #             reward = new_reward
    #     return reward

    @staticmethod
    def helper_reward_positive(state) -> int:
        reward = 0
        state = state.tolist()
        for line in state:
            if line.count(1) >= 5:
                reward += 1
        return reward

    @staticmethod
    def helper_reward_negative(state) -> int:
        reward = 0
        state = state.tolist()
        for line in state:
            for idx, block in enumerate(line):
                if 1 <= idx < GameConsts.GRID_WIDTH - 1:
                    if block == 0 and line[idx - 1] == 1 and line[idx + 1] == 1:
                        reward -= 1
                if idx == 0 and block == 0 and line[1] == 1:
                    reward -= 1
                if idx == GameConsts.GRID_WIDTH and block == 0 and line[9] == 1:
                    reward -= 1
        return reward

    def train(self, num_steps: int = 10000, batch_size: int = 1024,
              learning_rate: float = 0.01, y: float = 0.9,
              start_e: float = 1.0, end_e: float = 0.001,
              start_max_step: int = 10000, exploration_steps: int = 2500, save_name: str = None):

        fps = 2000
        global start_time

        env = Environment()
        experience_buffer = ExperienceBuffer(state_shape=(1, GameConsts.GRID_HEIGHT, GameConsts.GRID_WIDTH))

        self.session.run(tf.compat.v1.global_variables_initializer())
        e = start_e
        step_optimizer = 0
        max_step = start_max_step
        start_time = datetime.now()
        for i in range(num_steps):
            if i <= exploration_steps:
                e -= (start_e - end_e) / exploration_steps
                step_optimizer += self.max_step / exploration_steps
                if step_optimizer >= 1 and max_step < self.max_step:
                    max_step += 1
                    step_optimizer -= 1

            env.reset(fps)
            state = env.get_state()
            step = 0
            while not (env.game_over or step > max_step):
                step += 1
                if np.random.rand(1) <= e:  # exploration - random action
                    action = np.random.randint(1, 4)
                else:  # exploitation - let the model decide the action
                    action = self.session.run(
                        self.model.predict_action,
                        feed_dict={self.model.input: np.expand_dims(np.expand_dims(state, axis=0), axis=0)})[0]

                action = Action(action)

                score = env.score
                env.play(action, fps)

                if env.game_over:
                    self.sum_of_scores += env.score
                    reward = -10
                else:
                    reward = env.score - score + Agent.helper_reward_positive(state) + Agent.helper_reward_negative(state)

                state_next = env.get_state()
                experience_buffer.add(state, action.value, reward, state_next, env.game_over)
                state = state_next

            if len(experience_buffer.buffer) >= batch_size:
                batch = experience_buffer.get_batch(batch_size)  # get new batch

                next_q = self.session.run(self.model.output_Q, feed_dict={self.model.input: batch['state_next']})
                target_q = self.session.run(self.model.output_Q, feed_dict={self.model.input: batch['state']})
                distance = 1 - batch['done'].reshape(batch_size)
                target_q[range(batch_size),
                         batch['action']] = batch['reward'] + y * distance * np.max(next_q, axis=1)  # bellman

                self.session.run(
                    self.model.update_model,
                    feed_dict={
                        self.model.input: batch['state'],
                        self.model.target_Q: target_q,
                        self.model.learning_rate: learning_rate})  # update model parameters

            self._take_scores(i, num_steps, e, max_step, save_name)

        if save_name is not None:
            self._save_model(save_name)
            self.plot_learning_curve(num_steps, save_name)

    def test(self) -> None:
        fps = 30
        tetris = Environment()
        tetris.reset(fps)
        while not tetris.game_over:
            state = tetris.get_state()
            action = self.session.run(
                self.model.predict_action,
                feed_dict={self.model.input: np.expand_dims(np.expand_dims(state, axis=0), axis=0)})[0]

            action = Action(action)
            tetris.play(action, fps)

    def plot_learning_curve(self, num_steps: int, name: str):
        save_path = os.path.join(ROOT_DIR, 'trained_model', name)
        x_data = list(range(0, num_steps // times))
        y_data = self.mean_scores
        print(y_data)
        print(x_data)
        plt.plot(x_data, y_data)
        plt.title('Average score vs Episodes')
        plt.xlabel('Episodes (in ten thousands)')
        plt.ylabel('Score')
        plt.grid(True)
        plt.savefig(save_path)
        plt.show()

    # def plot_test_histogram(self, test_num: int):
    #     scores = []
    #     for i in range(test_num):
    #         scores.append(self.test())
    #     scores.sort()
    #
    #     plt.hist(scores, bins='auto')
    #     plt.xlabel('Score')
    #     plt.ylabel('Count')
    #     plt.title('Histogram of test scores')
    #     plt.grid(True)
    #     save_path = os.path.join(ROOT_DIR, 'trained_model', 'histogram')
    #     plt.savefig(save_path)
    #     plt.show()
    #
    #     print("Max score: {0}, Min score: {1}, Average score: {2}".format(max(scores),
    #                                                                       min(scores), sum(scores) / len(scores)))


def main():
    agent = Agent(max_step=50000)
    agent.train(save_name="1.0")
    # agent.load_model("1.0")
    # agent.test()


if __name__ == '__main__':
    main()
