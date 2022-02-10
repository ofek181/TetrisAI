import tensorflow as tf
from consts import GameConsts


class DeepQNetwork:
	def __init__(self):
		input_shape = (None, 1, GameConsts.GRID_HEIGHT, GameConsts.GRID_WIDTH)
		tf.compat.v1.disable_eager_execution()
		self.input = tf.compat.v1.placeholder(tf.float32, shape=input_shape, name="input")

		conv_layer_1 = tf.keras.layers.Conv2D(
			filters=8,
			kernel_size=(4, 4),
			strides=(2, 2),
			activation='relu',
			padding="same",
			input_shape=input_shape)(self.input)

		conv_layer_2 = tf.keras.layers.Conv2D(
			filters=16,
			kernel_size=(2, 2),
			strides=(1, 1),
			activation='relu',
			padding="same")(conv_layer_1)

		conv_2_flat = tf.keras.layers.Flatten()(conv_layer_2)

		hidden1 = tf.keras.layers.Dense(
			units=128,
			activation='relu')(conv_2_flat)

		self.output_Q = tf.keras.layers.Dense(units=4)(hidden1)

		# Predict
		self.predict_action = tf.argmax(self.output_Q, 1)

		# Train
		self.target_Q = tf.compat.v1.placeholder(tf.float32, [None, 4])
		self.learning_rate = tf.compat.v1.placeholder(tf.float32, name="learning_rate")
		self.loss = tf.losses.mean_squared_error(self.target_Q, self.output_Q)
		self.update_model = tf.compat.v1.train.AdamOptimizer(self.learning_rate).minimize(self.loss)
