import requests 
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt

# Send a request to the API
response = requests.post("http://127.0.0.1:8000/generate", json={"num_samples": 2})
data = response.json()

# Convert base64-encoded images to PIL Images
images = [Image.open(io.BytesIO(base64.b64decode(img_b64))) for img_b64 in data["images"]]

# Display images using matplotlib
fig, axes = plt.subplots(1, len(images), figsize=(12, 4))

for ax, img in zip(axes, images):
    ax.imshow(img)
    ax.axis("off")

plt.show()
