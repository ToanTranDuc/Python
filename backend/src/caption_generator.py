"""
Caption Generator - Sinh chú thích cho ảnh sử dụng LSTM Decoder và Beam Search
Thực hiện giải mã chuỗi tuần tự với Beam Search optimization (k=3)
"""

import numpy as np
import logging
from pathlib import Path

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_CONFIG, BEAM_SEARCH_CONFIG

logger = logging.getLogger(__name__)


class CaptionGenerator:
    """
    Class để generate caption từ image features sử dụng LSTM Decoder
    """
    
    def __init__(self, encoder, decoder, word_to_idx, idx_to_word, max_length=None):
        self.encoder = encoder
        self.decoder = decoder
        self.word_to_idx = word_to_idx
        self.idx_to_word = idx_to_word
        self.max_length = max_length or MODEL_CONFIG["max_length"]
        
        # Beam search config
        self.beam_width = BEAM_SEARCH_CONFIG["beam_width"]
        self.alpha = BEAM_SEARCH_CONFIG["alpha"]
        
        # Special tokens
        self.start_token = MODEL_CONFIG["start_token"]
        self.end_token = MODEL_CONFIG["end_token"]
        self.pad_token = MODEL_CONFIG["pad_token"]
        
        logger.info(f"CaptionGenerator initialized with beam_width={self.beam_width}")
    
    def extract_features(self, image):
        """
        Trích xuất đặc trưng từ ảnh sử dụng CNN Encoder
        
        Args:
            image: Preprocessed image array (1, 299, 299, 3)
        
        Returns:
            numpy array: Image features (1, 8, 8, 2048) hoặc (1, 256) tùy model
        """
        try:
            features = self.encoder.predict(image, verbose=0)
            logger.info(f"Extracted features shape: {features.shape}")
            return features
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            raise
    
    def greedy_search(self, features):
        """
        Greedy search - chọn từ có xác suất cao nhất mỗi bước
        Đơn giản nhưng có thể không tối ưu
        
        Args:
            features: Image features từ CNN encoder
        
        Returns:
            str: Generated caption
        """
        logger.info("Generating caption using Greedy Search...")
        
        try:
            # Bắt đầu với <start> token
            caption = [self.word_to_idx.get(self.start_token, 1)]
            
            for _ in range(self.max_length):
                # Pad sequence to max_length
                sequence = np.zeros((1, self.max_length))
                sequence[0, :len(caption)] = caption
                
                # Predict next word
                # Input: [features, sequence]
                predictions = self.decoder.predict([features, sequence], verbose=0)
                
                # Get word with highest probability
                predicted_idx = np.argmax(predictions[0, len(caption)-1, :])
                
                # Convert index to word
                predicted_word = self.idx_to_word.get(predicted_idx, '<unk>')
                
                # Stop if <end> token
                if predicted_word == self.end_token:
                    break
                
                caption.append(predicted_idx)
            
            # Convert indices to words
            caption_words = [self.idx_to_word.get(idx, '<unk>') for idx in caption[1:]]
            caption_text = ' '.join(caption_words)
            
            logger.info(f"Generated caption: {caption_text}")
            return caption_text
            
        except Exception as e:
            logger.error(f"Error in greedy search: {e}")
            raise
    
    def beam_search(self, features):
        """
        Beam Search - Tìm kiếm k chuỗi tốt nhất đồng thời (k=3)
        Tối ưu hóa chất lượng caption
        
        Args:
            features: Image features từ CNN encoder
        
        Returns:
            str: Best generated caption
        """
        logger.info(f"Generating caption using Beam Search (k={self.beam_width})...")
        
        try:
            # Initialize với <start> token
            start_idx = self.word_to_idx.get(self.start_token, 1)
            
            # Beam: list of (sequence, score)
            beams = [([start_idx], 0.0)]
            
            for step in range(self.max_length):
                candidates = []
                
                for sequence, score in beams:
                    # Nếu sequence đã kết thúc, giữ nguyên
                    if sequence[-1] == self.word_to_idx.get(self.end_token, 2):
                        candidates.append((sequence, score))
                        continue
                    
                    # Pad sequence
                    padded_seq = np.zeros((1, self.max_length))
                    padded_seq[0, :len(sequence)] = sequence
                    
                    # Predict next word probabilities
                    predictions = self.decoder.predict([features, padded_seq], verbose=0)
                    word_probs = predictions[0, len(sequence)-1, :]
                    
                    # Get top k words
                    top_k_indices = np.argsort(word_probs)[-self.beam_width:]
                    
                    # Expand beam
                    for idx in top_k_indices:
                        new_sequence = sequence + [idx]
                        # Log probability
                        new_score = score + np.log(word_probs[idx] + 1e-10)
                        candidates.append((new_sequence, new_score))
                
                # Sort by score và chọn top k
                # Apply length penalty: score / (len^alpha)
                candidates = sorted(
                    candidates,
                    key=lambda x: x[1] / (len(x[0]) ** self.alpha),
                    reverse=True
                )
                beams = candidates[:self.beam_width]
                
                # Early stopping nếu tất cả beams đã kết thúc
                if all(seq[-1] == self.word_to_idx.get(self.end_token, 2) 
                       for seq, _ in beams):
                    break
            
            # Chọn best sequence
            best_sequence, best_score = beams[0]
            
            # Convert indices to words (skip <start> và <end>)
            caption_words = []
            for idx in best_sequence[1:]:
                word = self.idx_to_word.get(idx, '<unk>')
                if word == self.end_token:
                    break
                caption_words.append(word)
            
            caption_text = ' '.join(caption_words)
            
            logger.info(f"Best caption (score={best_score:.4f}): {caption_text}")
            
            # Return top 3 captions nếu muốn
            all_captions = []
            for sequence, score in beams[:3]:
                words = []
                for idx in sequence[1:]:
                    word = self.idx_to_word.get(idx, '<unk>')
                    if word == self.end_token:
                        break
                    words.append(word)
                all_captions.append({
                    'caption': ' '.join(words),
                    'score': float(score),
                    'normalized_score': float(score / (len(sequence) ** self.alpha))
                })
            
            return caption_text, all_captions
            
        except Exception as e:
            logger.error(f"Error in beam search: {e}")
            # Fallback to greedy search
            logger.warning("Falling back to greedy search...")
            return self.greedy_search(features), []
    
    def generate_caption(self, image, method='beam_search'):
        """
        Main function để generate caption
        
        Args:
            image: Preprocessed image array
            method: 'beam_search' hoặc 'greedy'
        
        Returns:
            dict: {
                'caption': str,
                'all_captions': list (nếu beam search),
                'method': str
            }
        """
        logger.info("=" * 50)
        logger.info("GENERATING CAPTION")
        logger.info("=" * 50)
        
        try:
            # Extract features
            features = self.extract_features(image)
            
            # Generate caption
            if method == 'beam_search':
                caption, all_captions = self.beam_search(features)
                return {
                    'caption': caption,
                    'all_captions': all_captions,
                    'method': 'beam_search',
                    'beam_width': self.beam_width
                }
            else:
                caption = self.greedy_search(features)
                return {
                    'caption': caption,
                    'all_captions': [],
                    'method': 'greedy'
                }
                
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            raise


def get_caption_generator(model_loader):
    """
    Factory function để tạo CaptionGenerator
    
    Args:
        model_loader: ModelLoader instance
    
    Returns:
        CaptionGenerator instance
    """
    models = model_loader.get_models()
    
    return CaptionGenerator(
        encoder=models['encoder'],
        decoder=models['decoder'],
        word_to_idx=models['word_to_idx'],
        idx_to_word=models['idx_to_word'],
        max_length=models['max_length']
    )
