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

    # Resize to half (faster processing)
    image = image.resize((image.width // 2, image.height // 2))

    # Convert to OpenCV format
    image_cv = np.array(image)

    # Apply binary threshold
    _, thresh = cv2.threshold(image_cv, 150, 255, cv2.THRESH_BINARY)

    # Convert back to PIL Image
    processed_image = Image.fromarray(thresh)
    return processed_image

@app.get("/")
def home():
    return {"message": "OCR API is working. Use /ocr/ to POST an image."}

@app.post("/ocr/")
async def ocr(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        processed_image = preprocess_image(contents)

        # Use Tesseract with optimized config
        custom_config = r'--oem 1 --psm 6'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        

        return {"text": text.strip()}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
