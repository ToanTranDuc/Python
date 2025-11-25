

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Model configurations
MODEL_CONFIG = {
    # CNN Encoder (EfficientNetB0) - Updated to match training code
    "cnn_model_name": "EfficientNetB0",
    "image_size": (224, 224),  # EfficientNetB0 uses 224x224
    "feature_shape": (1280,),  # EfficientNetB0 output is 1280 dims (not 2048)
    "embedding_dim": 256,  
    
    # LSTM Decoder
    "lstm_units": 512,  # Matches your Bidirectional LSTM(256) * 2 = 512
    "dropout_rate": 0.5,
    
    # Vocabulary (will be determined from tokenizer.pkl)
    "max_length": 40,  # Will be auto-detected from tokenizer
    "vocab_size": 10000,  # Will be auto-detected from tokenizer
    
    # Special tokens (matches your training)
    "start_token": "startseq",  # Changed from <start>
    "end_token": "endseq",      # Changed from <end>
    "pad_token": "<pad>",
}

# Beam Search configuration
BEAM_SEARCH_CONFIG = {
    "beam_width": 3,  # k=3 như yêu cầu
    "max_length": MODEL_CONFIG["max_length"],
    "alpha": 0.7,  # Length penalty factor
}

# Model file paths
MODEL_FILES = {
    "encoder": MODELS_DIR / "encoder_model.h5",
    "decoder": MODELS_DIR / "decoder_model.h5",
    "full_model": MODELS_DIR / "lstm_cnn_model.h5",
    "tokenizer": MODELS_DIR / "tokenizer.pkl",
    "feature_extractor": MODELS_DIR / "feature_extractor.h5",
}

# API configurations
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "title": "Image Captioning API - LSTM-CNN",
    "description": "API for automatic image caption generation using LSTM-CNN model",
    "version": "1.0.0",
    "allowed_image_types": ["image/jpeg", "image/png", "image/jpg"],
    "max_image_size_mb": 10,
}

# CORS settings
CORS_CONFIG = {
    "allow_origins": ["*"],  # Trong production nên chỉ định cụ thể
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

# Preprocessing settings
PREPROCESSING_CONFIG = {
    # InceptionV3 preprocessing: scale to [-1, 1]
    "normalization_type": "inception",  # or "vgg", "standard"
    "resize_mode": "bilinear",
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# Performance settings
PERFORMANCE_CONFIG = {
    "batch_size": 1,  # For single image inference
    "use_gpu": True,
    "gpu_memory_fraction": 0.8,
}
