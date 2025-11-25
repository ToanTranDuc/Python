# Model Files

Folder này chứa các model files cần thiết cho ứng dụng.

## 📦 Files bắt buộc

1. **best_model_captioning.h5** (~73 MB)
   - Full model (EfficientNetB0 + BiLSTM)
   - Input: Image features (1280,) + Text sequence (37,)
   - Output: Word probabilities (8781,)

2. **tokenizer.pkl** (~340 KB)
   - Keras Tokenizer object
   - Vocabulary size: 8,781 words
   - Mapping: word ↔ index

3. **model_metadata.json** (~138 bytes)
   - Model configuration
   - Vocab size, max length, image size

## ⬇️ Download Instructions

**Model files KHÔNG được commit lên GitHub** do kích thước lớn.

### Cách 1: Download từ Kaggle (Khuyến nghị)

1. Vào: https://www.kaggle.com/code/ctontrn/lstm-cnn-att
2. Click tab **"Output"**
3. Download 3 files trên
4. Đặt vào folder `models/` này

### Cách 2: Dùng Kaggle API

Xem hướng dẫn trong `SETUP_KAGGLE_API.md`

## ✅ Kiểm tra

Sau khi download, kiểm tra:

```bash
python test_model_correct.py
```

Nếu thành công, bạn sẽ thấy:
```
✅ MODEL LOADING TEST PASSED!
```

## 📝 Optional Files

- `LSTM_ENetB0_BLEU.py` - Training code reference (không cần cho inference)

## ⚠️ Lưu ý

- File `.h5` có thể bị corrupt nếu download qua browser
- Nên dùng "Save Link As" thay vì click trực tiếp
- Nếu gặp lỗi load model, kiểm tra TensorFlow version

---

**Sau khi download xong 3 files, bạn có thể chạy ứng dụng!** 🚀
