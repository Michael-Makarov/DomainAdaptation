import tensorflow as tf
from tensorflow.python.keras.layers import Layer
from tensorflow.python.keras import backend as k


def build_grad_reverse(lambda_):
    @tf.custom_gradient
    def grad_reverse(x):
        y = tf.identity(x)

        def custom_grad(dy):
            return -lambda_ * dy

        return y, custom_grad

    return grad_reverse


def reverse_gradient(x, l=1.0):
    positive_path = tf.stop_gradient(x * tf.cast(1 + l, tf.float32))
    negative_path = x * tf.cast(-l, tf.float32)
    return positive_path + negative_path


def reverse_gradient_old(x, alpha):
    '''Flips the sign of the incoming gradient during training.'''
    try:
        reverse_gradient.num_calls += 1
    except AttributeError:
        reverse_gradient.num_calls = 1

    reverse_grad_name = "GradientReversal%d" % reverse_gradient.num_calls

    @tf.RegisterGradient(reverse_grad_name)
    def _flip_gradients(unused_op, grad):
        return [tf.negative(grad) * alpha]

    g = tf.compat.v1.get_default_graph()
    with g.gradient_override_map({'Identity': reverse_grad_name}):
        y = tf.identity(x, name='Identity')

    return y


class GradientReversal(Layer):
    '''Flip the sign of gradient during training.'''

    def __init__(self, alpha, **kwargs):
        super(GradientReversal, self).__init__(**kwargs)
        self._trainable = False
        self.alpha = alpha
        self.grad_reverse = build_grad_reverse(self.alpha)

    def build(self, input_shape):
        pass

    def call(self, x):
        return self.grad_reverse(x)

    def compute_output_shape(self, input_shape):
        return input_shape
