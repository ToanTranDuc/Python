# 🖼️ Image Captioning - LSTM-CNN Deep Learning

Ứng dụng web tự động tạo chú thích cho ảnh sử dụng mô hình Deep Learning (EfficientNetB0 + Bidirectional LSTM).

![Demo](https://img.shields.io/badge/Status-Demo-yellow) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)

---

## ⚡ CHẠY NHANH (DEMO MODE)

**Không cần download model - chỉ test UI:**

```bash
# Cài đặt
pip install fastapi uvicorn python-multipart

# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend  
cd frontend
python -m http.server 5500
```

**Mở trình duyệt:** http://localhost:5500

---

## 🏗️ Công nghệ

- **Backend:** FastAPI, Python 3.13
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI Model:** EfficientNetB0 + BiLSTM (Flickr8k dataset)
- **Inference:** Beam Search (k=3)

## 📁 Cấu trúc

```
├── backend/           # FastAPI server
├── frontend/          # Web UI
├── models/           # Model files (không có trên GitHub)
└── README.md
```

---

## 🚀 PRODUCTION MODE (Với Model Thật)

### 1. Download Model

Từ Kaggle: https://www.kaggle.com/code/ctontrn/lstm-cnn-att

Tải 3 files vào `models/`:
- `best_model_captioning.h5` (73 MB)
- `tokenizer.pkl` (340 KB)
- `model_metadata.json`

### 2. Cài đặt đầy đủ

```bash
pip install tensorflow pillow numpy fastapi uvicorn python-multipart
```

### 3. Switch to Production

```bash
# Windows
copy backend\main_production.py backend\main.py

# Linux/Mac
cp backend/main_production.py backend/main.py
```

### 4. Chạy

```bash
cd backend && python main.py
```

---

## 📝 API Endpoints

- `GET /health` - Health check
- `POST /caption` - Upload ảnh, nhận captions
- `GET /models/info` - Model information
- `GET /docs` - API documentation (Swagger)

---

## ⚠️ Lưu ý

- Model files **KHÔNG** được commit lên GitHub (quá lớn)
- Demo mode dùng mock captions (random)
- Production mode cần TensorFlow 2.15-2.20

---

## 📚 Tài liệu

- [Hướng dẫn Demo](README_DEMO.md) - Chạy không cần model
- [Backend Source](backend/) - FastAPI code
- [Frontend Source](frontend/) - HTML/CSS/JS

---

## 👨‍💻 Tác giả

**Trần Đức Toàn**  
GitHub: [@ToanTranDuc](https://github.com/ToanTranDuc)

---

**⭐ Star nếu hữu ích!**
