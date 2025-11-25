#!/bin/bash
# Script chạy Frontend (Linux/Mac)

echo "=========================================="
echo "  LSTM-CNN Image Captioning - Frontend"
echo "=========================================="
echo ""

# Check if Python installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "   Install Python3 first: https://www.python.org/"
    exit 1
fi

echo "✓ Python3 found"
echo ""

# Navigate to frontend
cd "$(dirname "$0")/frontend" || exit

echo "Starting frontend server..."
echo "Frontend URL: http://localhost:5500"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Start server
python3 -m http.server 5500
