from constants import *
from inference_sdk import InferenceHTTPClient
from typing import Dict, List, Any
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

def detect_fingertips(self, image: np.ndarray) -> List[Dict[str, Any]]:  
  # Fingertip landmark indices
  FINGERTIP_IDS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
  """Detect fingertips using MediaPipe hands"""
  # Convert BGR to RGB
  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  with self.mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.7) as hands:
    results = hands.process(rgb_image)

    if not results.multi_hand_landmarks:
      print("No hands detected.")
      return []

    fingertips = []

    for hand_landmarks in results.multi_hand_landmarks:
      for idx in FINGERTIP_IDS:
        landmark = hand_landmarks.landmark[idx]
        h, w, _ = image.shape
        x, y = int(landmark.x * w), int(landmark.y * h)
        fingertips.append({
            "position": [x, y],
        })

    return fingertips

def palm_line_position(base64_img: str):
  try:
    CLIENT = InferenceHTTPClient(
      api_url=PALM_POS_DETECTION_API_URL,
      api_key=PALM_POS_DETECTION_API_KEY
    )

    result = CLIENT.infer(
      base64_img,
      model_id=PALM_POS_DETECTION_MODEL_ID
    )
    
    # Get the predictions list
    predictions = result.get("predictions", [])
    
    # Extract only x and y coordinates of keypoints for each prediction
    all_keypoints = []

    for pred in predictions:
      keypoints = pred.get("keypoints", [])
      xy_points = [{"x": kp["x"], "y": kp["y"]} for kp in keypoints]
      all_keypoints.append({
        "class": pred.get("class"),
        "keypoints": xy_points,
        "center": {"x": pred.get("x"), "y": pred.get("y")},
      })
  
    return all_keypoints
    
  except Exception as e:
    raise ValueError(f"Error processing palm line position from API: {str(e)}")