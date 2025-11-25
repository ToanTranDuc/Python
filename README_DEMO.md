# 🚀 HƯỚNG DẪN CHẠY ỨNG DỤNG

## ⚡ CHẠY DEMO (2 PHÚT - KHÔNG CẦN MODEL)

### Bước 1: Cài đặt
```bash
pip install fastapi uvicorn python-multipart
```

### Bước 2: Chạy Backend
```bash
cd backend
python main.py
```

Backend: **http://localhost:8000**

### Bước 3: Chạy Frontend (terminal mới)
```bash
cd frontend  
python -m http.server 5500
```

Frontend: **http://localhost:5500**

### Bước 4: Test
Mở trình duyệt: **http://localhost:5500** → Upload ảnh → Xem kết quả!

---

## 🎯 DEMO vs PRODUCTION

**DEMO MODE** (hiện tại):
- ✅ Frontend hoạt động 100%
- ✅ Captions ngẫu nhiên (mock data)
- ⚠️ Không cần model files

**PRODUCTION MODE** (cần model):
1. Download model từ Kaggle: https://www.kaggle.com/code/ctontrn/lstm-cnn-att
2. Đặt 3 files vào `models/`: `best_model_captioning.h5`, `tokenizer.pkl`, `model_metadata.json`
3. Copy `backend/main_production.py` → `backend/main.py`
4. Cài thêm: `pip install tensorflow pillow numpy`
5. Restart backend

---

## ❓ LỖI THƯỜNG GẶP

**"Không vào được http://0.0.0.0:8000"**
→ Dùng **http://localhost:8000** thay vì 0.0.0.0

**"Port đã được dùng"**
→ Đổi port trong `main.py`: `uvicorn.run(app, port=8001)`

**"CORS error"**  
→ Phải mở frontend qua http://localhost:5500 (không phải file://)

---

Xem chi tiết trong `README.md`
