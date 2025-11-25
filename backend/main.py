

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import time
from pathlib import Path
import sys

# Import config
sys.path.append(str(Path(__file__).parent.parent))
from config import API_CONFIG, CORS_CONFIG, LOGGING_CONFIG

# Import các modules
from src.model_loader import get_model_loader
from src.image_processor import get_image_processor
from src.caption_generator import get_caption_generator

# Setup logging
logging.basicConfig(
    level=LOGGING_CONFIG["level"],
    format=LOGGING_CONFIG["format"]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["allow_origins"],
    allow_credentials=CORS_CONFIG["allow_credentials"],
    allow_methods=CORS_CONFIG["allow_methods"],
    allow_headers=CORS_CONFIG["allow_headers"],
)

# Global instances - load models khi startup
model_loader = None
image_processor = None
caption_generator = None


# Pydantic models cho request/response
class HealthResponse(BaseModel):
    status: str
    message: str
    models_loaded: bool


class CaptionResponse(BaseModel):
    success: bool
    caption: str
    all_captions: list = []
    method: str
    inference_time: float
    message: str = ""


# Startup event - Load models vào bộ nhớ
@app.on_event("startup")
async def startup_event():
    """
    Load tất cả models vào bộ nhớ khi khởi động server
    Giảm thiểu độ trễ inference
    """
    global model_loader, image_processor, caption_generator
    
    logger.info("=" * 70)
    logger.info("STARTING IMAGE CAPTIONING API SERVER")
    logger.info("=" * 70)
    
    try:
        # Initialize image processor
        logger.info("Initializing Image Processor...")
        image_processor = get_image_processor()
        
        # Load models
        logger.info("Loading models into memory...")
        model_loader = get_model_loader()
        
        # Initialize caption generator
        logger.info("Initializing Caption Generator...")
        caption_generator = get_caption_generator(model_loader)
        
        logger.info("=" * 70)
        logger.info("✓ SERVER READY - All models loaded successfully!")
        logger.info(f"✓ API running at http://{API_CONFIG['host']}:{API_CONFIG['port']}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        logger.error("Server will start but models may not be available")


# Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """
    Root endpoint - Health check
    """
    return {
        "status": "online",
        "message": "Image Captioning API - LSTM-CNN Model",
        "models_loaded": model_loader is not None
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    models_loaded = all([
        model_loader is not None,
        image_processor is not None,
        caption_generator is not None
    ])
    
    return {
        "status": "healthy" if models_loaded else "degraded",
        "message": "All systems operational" if models_loaded else "Models not loaded",
        "models_loaded": models_loaded
    }


@app.post("/caption", response_model=CaptionResponse)
async def generate_caption(
    file: UploadFile = File(...),
    method: str = "beam_search"
):
    """
    Main endpoint để generate caption cho ảnh
    
    Quy trình Inference Chi tiết:
    1. Tiếp nhận Request: Nhận file ảnh qua HTTP POST
    2. Tiền xử lý Ảnh: Resize 299x299, normalize [-1, 1]
    3. Trích xuất Đặc trưng: CNN Encoder (InceptionV3) -> features (8x8x2048)
    4. Giải mã Chuỗi: LSTM Decoder với Beam Search (k=3)
    5. Phản hồi: Trả về caption dưới dạng JSON
    
    Args:
        file: UploadFile - Ảnh đầu vào (JPEG/PNG)
        method: str - 'beam_search' (default, k=3) hoặc 'greedy'
    
    Returns:
        CaptionResponse với caption và metadata
    """
    start_time = time.time()
    
    logger.info("=" * 70)
    logger.info(f"NEW REQUEST: Generate caption for {file.filename}")
    logger.info("=" * 70)
    
    # Validate models loaded
    if not all([model_loader, image_processor, caption_generator]):
        raise HTTPException(
            status_code=503,
            detail="Models not loaded. Please try again later."
        )
    
    # Validate file type
    if file.content_type not in API_CONFIG["allowed_image_types"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {API_CONFIG['allowed_image_types']}"
        )
    
    try:
        # Step 1: Tiếp nhận Request
        logger.info(f"Step 1: Receiving image - {file.filename} ({file.content_type})")
        image_bytes = await file.read()
        file_size_mb = len(image_bytes) / (1024 * 1024)
        
        if file_size_mb > API_CONFIG["max_image_size_mb"]:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {API_CONFIG['max_image_size_mb']}MB"
            )
        
        logger.info(f"Image size: {file_size_mb:.2f} MB")
        
        # Step 2: Tiền xử lý Ảnh
        logger.info("Step 2: Preprocessing image (resize 299x299, normalize)")
        preprocessed_image = image_processor.preprocess_from_bytes(image_bytes)
        logger.info(f"Preprocessed shape: {preprocessed_image.shape}")
        
        # Step 3 + 4: Trích xuất đặc trưng và Giải mã với Beam Search
        logger.info(f"Step 3-4: Feature extraction + LSTM decoding (method: {method})")
        result = caption_generator.generate_caption(
            preprocessed_image,
            method=method
        )
        
        # Step 5: Phản hồi
        inference_time = time.time() - start_time
        logger.info(f"Step 5: Response generated in {inference_time:.2f}s")
        logger.info(f"Generated caption: '{result['caption']}'")
        logger.info("=" * 70)
        
        return {
            "success": True,
            "caption": result['caption'],
            "all_captions": result.get('all_captions', []),
            "method": result['method'],
            "inference_time": round(inference_time, 3),
            "message": "Caption generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating caption: {str(e)}"
        )


@app.post("/caption/batch")
async def generate_captions_batch(files: list[UploadFile] = File(...)):
    """
    Batch processing - Generate captions cho nhiều ảnh
    
    Args:
        files: List of UploadFile
    
    Returns:
        List of CaptionResponse
    """
    logger.info(f"Batch request: {len(files)} images")
    
    results = []
    for file in files:
        try:
            result = await generate_caption(file)
            results.append(result)
        except Exception as e:
            results.append({
                "success": False,
                "caption": "",
                "message": str(e),
                "inference_time": 0
            })
    
    return {"results": results, "total": len(files)}


@app.get("/models/info")
async def get_model_info():
    """
    Get thông tin về models đang được load
    """
    if not model_loader:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    models = model_loader.get_models()
    
    return {
        "encoder_loaded": models['encoder'] is not None,
        "decoder_loaded": models['decoder'] is not None,
        "vocab_size": len(models['word_to_idx']) if models['word_to_idx'] else 0,
        "max_length": models['max_length'],
        "image_size": image_processor.image_size if image_processor else None,
        "beam_width": caption_generator.beam_width if caption_generator else None
    }


# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=True,  # Auto-reload khi code thay đổi (dev only)
        log_level="info"
    )
