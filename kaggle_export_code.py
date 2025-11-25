"""
CODE NÀY DÙNG ĐỂ THÊM VÀO CUỐI NOTEBOOK KAGGLE
Copy toàn bộ code dưới đây và paste vào cuối file training trên Kaggle
"""

# ============================================================
# EXPORT MODELS CHO ỨNG DỤNG DEPLOYMENT
# Thêm đoạn code này vào CUỐI file training trên Kaggle
# ============================================================

print("\n" + "="*60)
print("📦 XUẤT MODELS ĐỂ SỬ DỤNG TRONG ỨNG DỤNG PRODUCTION")
print("="*60)

import pickle
import json
from tensorflow.keras.applications import EfficientNetB0

# --- 1. LƯU TOKENIZER ---
print("\n1️⃣ Đang lưu Tokenizer...")
tokenizer_path = '/kaggle/working/tokenizer.pkl'
with open(tokenizer_path, 'wb') as f:
    pickle.dump(tokenizer, f)
print(f"   ✓ Đã lưu: {tokenizer_path}")
print(f"   ✓ Vocab size: {len(tokenizer.word_index)}")

# --- 2. KIỂM TRA FULL MODEL ---
print("\n2️⃣ Kiểm tra Full Model...")
# Model này đã được lưu tự động trong quá trình training
model_path = '/kaggle/working/best_model_captioning.h5'
if os.path.exists(model_path):
    print(f"   ✓ Full model đã có: {model_path}")
    print(f"   ✓ File size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
else:
    print("   ⚠️ Không tìm thấy model, đang lưu model hiện tại...")
    model.save(model_path)
    print(f"   ✓ Đã lưu: {model_path}")

# --- 3. TẠO ENCODER RIÊNG (CNN Feature Extractor) ---
print("\n3️⃣ Đang tạo CNN Encoder riêng...")
encoder_path = '/kaggle/working/efficientnet_encoder.h5'
try:
    # Load EfficientNetB0 giống như trong training
    encoder_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        pooling='avg'  # Output: (None, 1280)
    )
    encoder_model.save(encoder_path)
    print(f"   ✓ Đã lưu encoder: {encoder_path}")
    print(f"   ✓ Output shape: {encoder_model.output_shape}")
    print(f"   ✓ File size: {os.path.getsize(encoder_path) / (1024*1024):.2f} MB")
except Exception as e:
    print(f"   ⚠️ Lỗi khi lưu encoder: {e}")

# --- 4. LƯU METADATA (Thông tin quan trọng) ---
print("\n4️⃣ Đang lưu Metadata...")
metadata = {
    # Model architecture
    'model_type': 'EfficientNetB0 + Bidirectional LSTM',
    'encoder': 'EfficientNetB0',
    'decoder': 'Bidirectional LSTM',
    
    # Parameters
    'vocab_size': vocab_size,
    'max_length': max_length,
    'image_size': IMG_SIZE,  # 224
    'feature_dim': 1280,  # EfficientNetB0 output
    'lstm_units': 512,  # BiLSTM(256) * 2
    'embedding_dim': 256,
    
    # Tokens
    'start_token': 'startseq',
    'end_token': 'endseq',
    'pad_token': '<pad>',
    
    # Training info
    'dataset': 'Flickr8k',
    'epochs_trained': EPOCHS,
    'batch_size': BATCH_SIZE,
    
    # Usage info
    'preprocessing': 'ImageNet normalization (mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])',
    'inference_method': 'Beam Search (k=3)'
}

metadata_path = '/kaggle/working/model_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"   ✓ Đã lưu metadata: {metadata_path}")

# --- 5. TẠO README CHO MODELS ---
print("\n5️⃣ Đang tạo README...")
readme_content = f"""# Image Captioning Models - Export từ Kaggle

## Thông tin Models

### 1. Tokenizer (tokenizer.pkl)
- Vocab size: {vocab_size}
- Max length: {max_length}
- Start token: 'startseq'
- End token: 'endseq'

### 2. Full Model (best_model_captioning.h5)
- Architecture: EfficientNetB0 + Bidirectional LSTM
- Input: Image features (1280,) + Text sequence
- Output: Word probabilities (vocab_size,)

### 3. CNN Encoder (efficientnet_encoder.h5)
- Architecture: EfficientNetB0 (pretrained ImageNet)
- Input: Image (224, 224, 3)
- Output: Features (1280,)

### 4. Metadata (model_metadata.json)
- Chứa tất cả thông tin cấu hình

## Cách sử dụng

### Bước 1: Download files
Download tất cả 4 files từ Kaggle Output:
1. tokenizer.pkl
2. best_model_captioning.h5
3. efficientnet_encoder.h5
4. model_metadata.json

### Bước 2: Đặt vào thư mục models/
```
models/
├── tokenizer.pkl
├── decoder_model.h5 (rename từ best_model_captioning.h5)
├── encoder_model.h5 (rename từ efficientnet_encoder.h5)
└── model_metadata.json
```

### Bước 3: Chạy ứng dụng
```bash
cd backend
python main.py
```

## Preprocessing Image

```python
from tensorflow.keras.applications.efficientnet import preprocess_input
import numpy as np

# Load và resize
image = load_img(path, target_size=(224, 224))
image = img_to_array(image)

# Normalize
image = preprocess_input(image)  # ImageNet normalization
image = np.expand_dims(image, axis=0)

# Extract features
features = encoder.predict(image)  # Shape: (1, 1280)
```

## Inference (Beam Search)

Xem code trong `backend/src/caption_generator.py`

---
Created: {pd.Timestamp.now()}
Dataset: Flickr8k
Training epochs: {EPOCHS}
"""

readme_path = '/kaggle/working/MODELS_README.md'
with open(readme_path, 'w') as f:
    f.write(readme_content)
print(f"   ✓ Đã tạo README: {readme_path}")

# --- 6. TỔNG KẾT ---
print("\n" + "="*60)
print("✅ HOÀN TẤT EXPORT!")
print("="*60)
print("\n📦 CÁC FILE CẦN DOWNLOAD:")
print("   1. tokenizer.pkl")
print("   2. best_model_captioning.h5")
print("   3. efficientnet_encoder.h5")
print("   4. model_metadata.json")
print("   5. MODELS_README.md (optional)")

print("\n📍 VỊ TRÍ:")
print("   → Kaggle → Output section → Click Download")

print("\n📝 SAU KHI DOWNLOAD:")
print("   1. Đặt vào thư mục: d:\\LSTM_APP\\models\\")
print("   2. Rename best_model_captioning.h5 → decoder_model.h5")
print("   3. Rename efficientnet_encoder.h5 → encoder_model.h5")
print("   4. Chạy: python test_models.py")
print("   5. Chạy app: python backend/main.py")

print("\n🎉 Sẵn sàng để deploy!")
print("="*60)

# Hiển thị chi tiết files
print("\n📊 CHI TIẾT FILES:")
for filename in ['tokenizer.pkl', 'best_model_captioning.h5', 
                 'efficientnet_encoder.h5', 'model_metadata.json', 
                 'MODELS_README.md']:
    filepath = f'/kaggle/working/{filename}'
    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"   ✓ {filename:30s} - {size_mb:6.2f} MB")
    else:
        print(f"   ✗ {filename:30s} - NOT FOUND")
