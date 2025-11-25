# ⚡ 2-MINUTE SETUP

## Chạy Demo (Không cần model)

```bash
# 1. Cài đặt
pip install fastapi uvicorn python-multipart

# 2. Backend (terminal 1)
cd backend
python main.py

# 3. Frontend (terminal 2)
cd frontend
python -m http.server 5500
```

**Mở:** http://localhost:5500 ✅

---

## Với Model Thật

1. Download từ [Kaggle](https://www.kaggle.com/code/ctontrn/lstm-cnn-att)
2. Đặt 3 files vào `models/`
3. `cp backend/main_production.py backend/main.py`
4. `pip install tensorflow pillow numpy`
5. Restart backend

---

**Lỗi?** Xem [README_DEMO.md](README_DEMO.md)
