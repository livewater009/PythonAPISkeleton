import mediapipe as mp
from typing import Dict, List, Tuple, Any
from tools import *

class PalmDetector:
  def __init__(self):
    """Initialize the palm detector with MediaPipe hands model"""
    self.mp_hands = mp.solutions.hands
    self.hands = self.mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=1,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
    )
    self.mp_drawing = mp.solutions.drawing_utils
    
  def detect_palm_features(self, base64_image: str) -> Dict[str, Any]:
    """Detect palm features from a base64 encoded image."""
    try:
      # Detect palm line positions
      palm_line_positions = palm_line_position(base64_image)
      
      # Detect fingertips
      decoded_img = base64_to_image(self, base64_image)
      fingertips_position = detect_fingertips(self, decoded_img)
      
      result = {
        "success": True,
        "fingertips": fingertips_position,
        "palm_lines": palm_line_positions,
        "image_shape": {
          "width": int(decoded_img.shape[1]),
          "height": int(decoded_img.shape[0])
        }
      }
     
      return result
      
    except Exception as e:
      return {
        "success": False,
        "error": str(e),
        "fingertips": [],
        "palm_lines": {},
        "image_shape": {"width": 0, "height": 0}
      }
