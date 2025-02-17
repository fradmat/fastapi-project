# import torch
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from PIL import Image
import io
import base64
# from awesomedemo import generate_images

# Initialize FastAPI app
app = FastAPI()



class DummyImageModel():
    def forward(self, num_samples: int):
        images = []
        for _ in range(num_samples):
            img_array = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)  # Simulated image
            images.append(img_array)
        return images

# Define request schema
class ImageRequest(BaseModel):
    num_samples: int  # Number of images to generate

def convert_image_to_bytes(img_array: np.ndarray) -> str:
    """Converts a NumPy array to a base64-encoded PNG byte stream."""
    try:
        # Convert NumPy array to a PIL Image
        img = Image.fromarray(img_array)  # Ensure it's a valid format

        # Save the image to a byte stream
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")  # Ensure PNG format is specified
        img_bytes.seek(0)  # Move pointer to the beginning

        # Encode as base64 for transport
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
        return img_base64
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

def generate_random_image(size=(64, 64)):
    img_array = np.random.randint(0, 256, (size[0], size[1], 3), dtype=np.uint8)
    return img_array
    
# API endpoint to generate images
@app.post("/generate")
def generate(request: ImageRequest):
    try:
        if request.num_samples <= 0:
            raise HTTPException(status_code=400, detail="Number of samples must be greater than 0")
        
        # images = generate_images(request.num_samples)
        # images_base64 = [convert_image_to_bytes(img) for img in images]

        # # return {"images": images_base64}
        # images = []
        # for _ in range(request.num_samples):
        #     images.append(DummyImageModel.forward())
        images = DummyImageModel().forward(request.num_samples)

        images_base64 = [convert_image_to_bytes(img) for img in images]
        return {"images": images_base64}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
