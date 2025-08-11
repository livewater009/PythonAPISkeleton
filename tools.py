from constants import *
import cv2
import numpy as np
import base64
from PIL import Image
import io

def base64_to_image(self, base64_string: str) -> np.ndarray:
  """Convert base64 encoded string to OpenCV image"""
  try:
    # Remove data URL prefix if present
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]
    
    # Decode base64 string
    image_data = base64.b64decode(base64_string)
    
    # Convert to PIL Image
    pil_image = Image.open(io.BytesIO(image_data))
    
    # Convert to OpenCV format (BGR)
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    return opencv_image
  
  except Exception as e:
    raise ValueError(f"Error decoding base64 image: {str(e)}")