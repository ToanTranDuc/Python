"""
Custom Keras layers for model compatibility
"""
import tensorflow as tf
from tensorflow import keras


class NotEqual(keras.layers.Layer):
    """
    Custom layer to handle the NotEqual operation created by mask_zero=True in Embedding layer.
    This layer is automatically created by TensorFlow when using mask_zero=True.
    """
    
    def __init__(self, y=None, **kwargs):
        """
        Args:
            y: The value to compare against (usually 0 for mask_zero)
        """
        super(NotEqual, self).__init__(**kwargs)
        self.y = y if y is not None else 0
    
    def call(self, inputs):
        """
        Returns a boolean mask indicating which values are not equal to y.
        This is what mask_zero=True does internally.
        """
        # Convert y to a tensor with the same dtype as inputs
        y_tensor = tf.cast(self.y, dtype=inputs.dtype)
        return tf.math.not_equal(inputs, y_tensor)
    
    def get_config(self):
        """Return the config of the layer for serialization"""
        config = super(NotEqual, self).get_config()
        config.update({'y': self.y})
        return config
    
    @classmethod
    def from_config(cls, config):
        """Create layer from config"""
        return cls(**config)


# Register the custom layer globally in TensorFlow's custom object scope
# This makes it available for deserialization
tf.keras.utils.get_custom_objects()['NotEqual'] = NotEqual
