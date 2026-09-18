import os
from PIL import Image

assets_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\assets"

print("Listing all images in assets directory...")

for fname in sorted(os.listdir(assets_dir)):
    fpath = os.path.join(assets_dir, fname)
    if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        try:
            with Image.open(fpath) as img:
                print(f"{fname} -> Size: {img.size}, Mode: {img.mode}")
        except Exception as e:
            print(f"Error reading {fname}: {e}")
