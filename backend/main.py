"""
FastAPI Backend - DEMO MODE (không cần model)
Dùng mock data để test Frontend
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time
import random
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Image Captioning API - DEMO",
    description="Demo API với mock data (không cần model)",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock captions cho demo
MOCK_CAPTIONS = [
    [
        {"text": "a dog playing on the beach", "score": 0.95},
        {"text": "a brown dog running on sand", "score": 0.89},
        {"text": "a happy dog enjoying the beach", "score": 0.82}
    ],
    [
        {"text": "a cat sitting on a chair", "score": 0.93},
        {"text": "a white cat resting indoors", "score": 0.87},
        {"text": "a fluffy cat on furniture", "score": 0.81}
    ],
    [
        {"text": "a person riding a bicycle", "score": 0.91},
        {"text": "someone cycling on the road", "score": 0.85},
        {"text": "a cyclist in the city", "score": 0.79}
    ],
    [
        {"text": "a beautiful sunset over mountains", "score": 0.94},
        {"text": "sunset with mountain silhouette", "score": 0.88},
        {"text": "colorful sky at dusk", "score": 0.83}
    ],
    [
        {"text": "a group of people at a party", "score": 0.92},
        {"text": "friends celebrating together", "score": 0.86},
        {"text": "people enjoying a social event", "score": 0.80}
    ]
]

@app.get("/")
def read_root():
    """Home endpoint"""
    return {
        "message": "Image Captioning API - DEMO MODE",
        "status": "running",
        "mode": "demo",
        "note": "Using mock data. Upload model files to enable real predictions."
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "demo",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": False,
        "message": "Demo mode - no model required"
    }

@app.post("/caption")
async def generate_caption(file: UploadFile = File(...)):
    """
    Generate caption cho ảnh upload (DEMO - dùng mock data)
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (jpg, png, etc.)"
            )
        
        # Simulate processing time
        start_time = time.time()
        time.sleep(random.uniform(0.5, 1.5))  # Giả lập xử lý
        
        # Random mock caption
        captions = random.choice(MOCK_CAPTIONS)
        
        processing_time = time.time() - start_time
        
        return JSONResponse(content={
            "success": True,
            "captions": captions,
            "processing_time": round(processing_time, 2),
            "image_name": file.filename,
            "mode": "demo",
            "note": "These are demo captions. Add model files for real predictions."
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/caption/batch")
async def generate_captions_batch(files: list[UploadFile] = File(...)):
    """
    Generate captions cho nhiều ảnh (DEMO)
    """
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 images per request"
        )
    
    results = []
    for file in files:
        try:
            # Validate
            if not file.content_type.startswith('image/'):
                continue
            
            # Mock caption
            captions = random.choice(MOCK_CAPTIONS)
            
            results.append({
                "filename": file.filename,
                "success": True,
                "captions": captions
            })
        except:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "Processing failed"
            })
    
    return JSONResponse(content={
        "success": True,
        "total": len(files),
        "processed": len(results),
        "results": results,
        "mode": "demo"
    })

@app.get("/models/info")
def get_model_info():
    """Thông tin về model (DEMO)"""
    return {
        "mode": "demo",
        "model_loaded": False,
        "message": "Demo mode - using mock captions",
        "instructions": {
            "step_1": "Download model files from Kaggle",
            "step_2": "Place in models/ folder: best_model_captioning.h5, tokenizer.pkl, model_metadata.json",
            "step_3": "Replace backend/main.py with production version",
            "step_4": "Restart server"
        },
        "demo_info": {
            "available_mock_captions": len(MOCK_CAPTIONS),
            "features": [
                "Image upload validation",
                "Random caption selection",
                "Simulated processing time",
                "Batch processing support"
            ]
        }
    }

if __name__ == "__main__":
    print("=" * 70)
    print("  🚀 IMAGE CAPTIONING API - DEMO MODE")
    print("=" * 70)
    print()
    print("  ⚠️  Running in DEMO mode with mock data")
    print("  📝 Captions are randomly generated for testing")
    print()
    print("  🌐 API URL: http://localhost:8000")
    print("  📚 API Docs: http://localhost:8000/docs")
    print()
    print("  💡 To enable real predictions:")
    print("     1. Download model files from Kaggle")
    print("     2. Place in models/ folder")
    print("     3. Use backend/main_production.py")
    print()
    print("=" * 70)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
