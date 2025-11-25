#!/bin/bash
# Script chạy Backend (Linux/Mac)

echo "=========================================="
echo "  LSTM-CNN Image Captioning - Backend"
echo "=========================================="
echo ""

# Check if Python installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "   Install Python3 first: https://www.python.org/"
    exit 1
fi

echo "✓ Python3 found"

# Check if dependencies installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo ""
    echo "⚠️  Dependencies not installed!"
    echo "   Installing now..."
    pip3 install -r requirements.txt
fi

echo "✓ Dependencies ready"
echo ""

# Check model files
if [ ! -f "models/best_model_captioning.h5" ]; then
    echo "❌ Model file not found!"
    echo ""
    echo "   Download from: https://www.kaggle.com/code/ctontrn/lstm-cnn-att"
    echo "   Or run: python3 setup_models.py"
    echo ""
    exit 1
fi

echo "✓ Model files found"
echo ""

# Navigate to backend
cd "$(dirname "$0")/backend" || exit

echo "Starting backend server..."
echo "API URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Start server
python3 main.py
