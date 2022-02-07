import tensorflow as tf
from consts import GameConsts


class DeepQNetwork:
	def __init__(self):
		input_size = GameConsts.GRID_WIDTH * GameConsts.GRID_HEIGHT + 1
		tf.compat.v1.disable_eager_execution()
		self.input = tf.compat.v1.placeholder(tf.float32, shape=input_size, name="input")

		layer1 = tf.keras.layers.Dense(units=input_size, activation='relu')(self.input)
		layer2 = tf.keras.layers.Dense(units=128, activation='relu')(layer1)
		layer3 = tf.keras.layers.Dense(units=10, activation='relu')(layer2)

		self.output = tf.keras.layers.Dense(units=4)(layer3)

		# Predict
		self.predict_action = tf.argmax(self.output, 1)

		# Train
		self.target_Q = tf.compat.v1.placeholder(tf.float32, [None, 4])
		self.learning_rate = tf.compat.v1.placeholder(tf.float32, name="learning_rate")
		self.loss = tf.losses.mean_squared_error(self.target_Q, self.output)
		self.update_model = tf.compat.v1.train.AdamOptimizer(self.learning_rate).minimize(self.loss)
