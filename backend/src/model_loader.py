"""
Model Loader - Load pre-trained LSTM-CNN models and tokenizer
Tải và quản lý các model đã huấn luyện vào bộ nhớ
"""

import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences
import logging
from pathlib import Path

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_CONFIG, MODEL_FILES, PREPROCESSING_CONFIG

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Class để load và quản lý models cho Image Captioning
    """
    
    def __init__(self):
        self.encoder = None
        self.decoder = None
        self.full_model = None
        self.tokenizer = None
        self.word_to_idx = None
        self.idx_to_word = None
        self.max_length = MODEL_CONFIG["max_length"]
        self.image_size = MODEL_CONFIG["image_size"]
        
    def load_cnn_encoder(self, custom_weights_path=None):
        """
        Load CNN Encoder (EfficientNetB0) để trích xuất đặc trưng ảnh
        
        Args:
            custom_weights_path: Path đến weights tùy chỉnh (nếu có)
        
        Returns:
            Model: CNN encoder model
        """
        logger.info("Loading CNN Encoder (EfficientNetB0)...")
        
        try:
            if custom_weights_path and Path(custom_weights_path).exists():
                # Load custom encoder
                self.encoder = load_model(custom_weights_path)
                logger.info(f"Loaded custom encoder from {custom_weights_path}")
            else:
                # Load pretrained EfficientNetB0 với average pooling
                # Output shape: (batch, 1280) - matches training code
                self.encoder = EfficientNetB0(
                    weights='imagenet',
                    include_top=False,
                    pooling='avg'  # Global average pooling → (1280,)
                )
                logger.info("Loaded EfficientNetB0 encoder from ImageNet weights")
            
            logger.info(f"Encoder output shape: {self.encoder.output_shape}")
            return self.encoder
            
        except Exception as e:
            logger.error(f"Error loading CNN encoder: {e}")
            raise
    
    def load_lstm_decoder(self, decoder_path):
        """
        Load LSTM Decoder model
        
        Args:
            decoder_path: Path đến decoder model file
        
        Returns:
            Model: LSTM decoder model
        """
        logger.info(f"Loading LSTM Decoder from {decoder_path}...")
        
        try:
            if Path(decoder_path).exists():
                self.decoder = load_model(decoder_path)
                logger.info(f"Loaded LSTM decoder successfully")
                logger.info(f"Decoder input shapes: {[inp.shape for inp in self.decoder.inputs]}")
                return self.decoder
            else:
                logger.warning(f"Decoder file not found: {decoder_path}")
                logger.info("You need to provide your trained decoder model")
                return None
                
        except Exception as e:
            logger.error(f"Error loading LSTM decoder: {e}")
            raise
    
    def load_full_model(self, model_path):
        """
        Load full end-to-end model (nếu bạn train như vậy)
        
        Args:
            model_path: Path đến full model file
        
        Returns:
            Model: Full model
        """
        logger.info(f"Loading full model from {model_path}...")
        
        try:
            if Path(model_path).exists():
                self.full_model = load_model(model_path)
                logger.info("Loaded full model successfully")
                return self.full_model
            else:
                logger.warning(f"Full model file not found: {model_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading full model: {e}")
            raise
    
    def load_tokenizer(self, tokenizer_path):
        """
        Load tokenizer (word <-> index mapping)
        
        Args:
            tokenizer_path: Path đến tokenizer pickle file
        
        Returns:
            Tokenizer object
        """
        logger.info(f"Loading tokenizer from {tokenizer_path}...")
        
        try:
            if Path(tokenizer_path).exists():
                with open(tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                
                # Create word-index mappings
                self.word_to_idx = self.tokenizer.word_index
                self.idx_to_word = {v: k for k, v in self.word_to_idx.items()}
                
                logger.info(f"Tokenizer loaded. Vocabulary size: {len(self.word_to_idx)}")
                return self.tokenizer
                
            else:
                logger.warning(f"Tokenizer file not found: {tokenizer_path}")
                logger.info("Creating dummy tokenizer for demo purposes")
                # Create dummy mapping
                self.word_to_idx = {
                    '<pad>': 0, '<start>': 1, '<end>': 2,
                    'a': 3, 'dog': 4, 'cat': 5, 'on': 6, 'the': 7, 'beach': 8
                }
                self.idx_to_word = {v: k for k, v in self.word_to_idx.items()}
                return None
                
        except Exception as e:
            logger.error(f"Error loading tokenizer: {e}")
            raise
    
    def load_all_models(self):
        """
        Load tất cả models và tokenizer vào bộ nhớ
        Gọi hàm này khi khởi động API để giảm độ trễ inference
        """
        logger.info("=" * 50)
        logger.info("LOADING ALL MODELS INTO MEMORY")
        logger.info("=" * 50)
        
        # Load tokenizer trước
        self.load_tokenizer(MODEL_FILES["tokenizer"])
        
        # Load CNN encoder
        encoder_path = MODEL_FILES.get("encoder") or MODEL_FILES.get("feature_extractor")
        self.load_cnn_encoder(encoder_path)
        
        # Load LSTM decoder
        if MODEL_FILES["decoder"].exists():
            self.load_lstm_decoder(MODEL_FILES["decoder"])
        
        # Hoặc load full model
        if MODEL_FILES["full_model"].exists():
            self.load_full_model(MODEL_FILES["full_model"])
        
        logger.info("=" * 50)
        logger.info("ALL MODELS LOADED SUCCESSFULLY")
        logger.info("=" * 50)
        
        return {
            "encoder": self.encoder,
            "decoder": self.decoder,
            "full_model": self.full_model,
            "tokenizer": self.tokenizer
        }
    
    def get_models(self):
        """
        Trả về các models đã load
        """
        return {
            "encoder": self.encoder,
            "decoder": self.decoder,
            "full_model": self.full_model,
            "tokenizer": self.tokenizer,
            "word_to_idx": self.word_to_idx,
            "idx_to_word": self.idx_to_word,
            "max_length": self.max_length
        }


# Singleton instance
_model_loader_instance = None

def get_model_loader():
    """
    Get singleton instance của ModelLoader
    """
    global _model_loader_instance
    if _model_loader_instance is None:
        _model_loader_instance = ModelLoader()
        _model_loader_instance.load_all_models()
    return _model_loader_instance
