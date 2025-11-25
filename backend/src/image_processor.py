"""
Image Processor - Tiền xử lý ảnh đầu vào
Xử lý resize, normalization theo yêu cầu của InceptionV3
"""

import numpy as np
from PIL import Image
import io
import logging
from pathlib import Path

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_CONFIG, PREPROCESSING_CONFIG

logger = logging.getLogger(__name__)


class ImageProcessor:
    """
    Class để xử lý ảnh đầu vào cho model
    """
    
    def __init__(self, image_size=None):
        self.image_size = image_size or MODEL_CONFIG["image_size"]
        self.normalization_type = PREPROCESSING_CONFIG["normalization_type"]
        
    def load_image_from_path(self, image_path):
        """
        Load ảnh từ file path
        
        Args:
            image_path: Path đến ảnh
        
        Returns:
            PIL.Image: Ảnh đã load
        """
        try:
            img = Image.open(image_path).convert('RGB')
            logger.info(f"Loaded image from {image_path}, size: {img.size}")
            return img
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            raise
    
    def load_image_from_bytes(self, image_bytes):
        """
        Load ảnh từ bytes (upload từ web)
        
        Args:
            image_bytes: Bytes của ảnh
        
        Returns:
            PIL.Image: Ảnh đã load
        """
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            logger.info(f"Loaded image from bytes, size: {img.size}")
            return img
        except Exception as e:
            logger.error(f"Error loading image from bytes: {e}")
            raise
    
    def resize_image(self, image):
        """
        Resize ảnh về kích thước yêu cầu (299x299 cho InceptionV3)
        
        Args:
            image: PIL.Image
        
        Returns:
            PIL.Image: Ảnh đã resize
        """
        try:
            resized = image.resize(self.image_size, Image.BILINEAR)
            logger.debug(f"Resized image to {self.image_size}")
            return resized
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            raise
    
    def normalize_image(self, image_array):
        """
        Normalize pixel values theo chuẩn của EfficientNetB0
        EfficientNet: uses ImageNet normalization
        
        Args:
            image_array: numpy array (H, W, 3) với giá trị [0, 255]
        
        Returns:
            numpy array: Ảnh đã normalize
        """
        try:
            if self.normalization_type == "inception" or self.normalization_type == "efficientnet":
                # EfficientNet: Chuẩn hóa ImageNet (giống Inception)
                # Scale to [0, 1] then normalize with ImageNet mean/std
                normalized = image_array / 255.0
                # ImageNet mean
                mean = np.array([0.485, 0.456, 0.406])
                std = np.array([0.229, 0.224, 0.225])
                normalized = (normalized - mean) / std
            elif self.normalization_type == "vgg":
                # VGG: subtract ImageNet mean
                mean = np.array([123.68, 116.779, 103.939])
                normalized = image_array - mean
            else:
                # Standard: scale to [0, 1]
                normalized = image_array / 255.0
            
            logger.debug(f"Normalized image using {self.normalization_type} method")
            logger.debug(f"Pixel range: [{normalized.min():.2f}, {normalized.max():.2f}]")
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing image: {e}")
            raise
    
    def preprocess_image(self, image):
        """
        Full preprocessing pipeline:
        1. Resize
        2. Convert to array
        3. Normalize
        4. Add batch dimension
        
        Args:
            image: PIL.Image hoặc numpy array
        
        Returns:
            numpy array: Ảnh đã preprocess, shape (1, 299, 299, 3)
        """
        try:
            # Nếu input là PIL Image
            if isinstance(image, Image.Image):
                # Resize
                image = self.resize_image(image)
                # Convert to array
                image_array = np.array(image)
            else:
                # Nếu đã là numpy array
                image_array = image
            
            # Normalize
            normalized = self.normalize_image(image_array.astype(np.float32))
            
            # Add batch dimension: (299, 299, 3) -> (1, 299, 299, 3)
            batched = np.expand_dims(normalized, axis=0)
            
            logger.info(f"Preprocessed image shape: {batched.shape}")
            return batched
            
        except Exception as e:
            logger.error(f"Error in preprocessing pipeline: {e}")
            raise
    
    def preprocess_from_path(self, image_path):
        """
        Load và preprocess ảnh từ path
        
        Args:
            image_path: Path đến ảnh
        
        Returns:
            numpy array: Ảnh đã preprocess
        """
        img = self.load_image_from_path(image_path)
        return self.preprocess_image(img)
    
    def preprocess_from_bytes(self, image_bytes):
        """
        Load và preprocess ảnh từ bytes
        
        Args:
            image_bytes: Bytes của ảnh
        
        Returns:
            numpy array: Ảnh đã preprocess
        """
        img = self.load_image_from_bytes(image_bytes)
        return self.preprocess_image(img)


# Singleton instance
_image_processor_instance = None

def get_image_processor():
    """
    Get singleton instance của ImageProcessor
    """
    global _image_processor_instance
    if _image_processor_instance is None:
        _image_processor_instance = ImageProcessor()
    return _image_processor_instance
