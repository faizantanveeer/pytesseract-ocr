from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
import numpy as np
import cv2

app = FastAPI()

def preprocess_image(image_bytes):
    # Open image and convert to grayscale
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    return image

@app.get("/")
def home():
    return {"message": "OCR API is working. Use /ocr/ to POST an image."}

@app.post("/ocr/")
async def ocr(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        processed_image = preprocess_image(contents)

        # Use Tesseract with optimized config
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        

        return {"text": text.strip()}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
