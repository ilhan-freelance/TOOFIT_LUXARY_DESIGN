import os
from PIL import Image

candidates = [
    r"c:\Users\asus\Documents\TOOFIT_TRAILORS\Toofit data\2 piece suit\1c9e6fbd6958a0c672a4f69216ce1d59.jpg",
    r"c:\Users\asus\Documents\TOOFIT_TRAILORS\Toofit data\2 piece suit\1cfdac64a0ed03c074ac03413d856e9d.jpg"
]

for p in candidates:
    if os.path.exists(p):
        img = Image.open(p)
        print(f"File: {os.path.basename(p)} | Size: {img.size} | Mode: {img.mode} | Bytes: {os.path.getsize(p)}")
