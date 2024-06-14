import numpy as np
from pygame import Rect

def vec(*args):
    return np.array((args)).astype(float)

def normalize(vector):
    """Normalize a numpy array."""
    mag = magnitude(vector)
    if mag == 0.0:
        return np.array((1,0,0)).astype(float)
    return vector / mag
   
def magnitude(vector):    
    """Give the magnitude of a vector."""
    return np.linalg.norm(vector)

def scale(vector, length):
   """Scales the magnitude of vec to the length.
      First normalizes then scales to appropriate size."""
   return normalize(vector) * length

def rectAdd(vector, rect):
   """Moves the pygame rect top left by vector.
      Returns a rect."""   
   newRect = Rect(rect.left + vector[0], rect.top + vector[1],
                  rect.width, rect.height)
   
   return newRect
   
