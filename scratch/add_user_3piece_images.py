import os
import shutil
import subprocess
from PIL import Image, ImageOps, ImageEnhance

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
src_dir = os.path.join(base_dir, "Toofit data", "3 Piece suit")
dest_dir = os.path.join(base_dir, "assets", "gallery", "bespoke")

os.makedirs(dest_dir, exist_ok=True)

files = sorted(os.listdir(src_dir))

saved_count = 0
for fname in files:
    ext = os.path.splitext(fname)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        continue
        
    src_path = os.path.join(src_dir, fname)
    try:
        img = Image.open(src_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Fit nicely to 600x800 portrait card
        img_fitted = ImageOps.fit(img, (600, 800), Image.Resampling.LANCZOS)
        
        saved_count += 1
        out_name = f"bespoke_{saved_count:02d}_3piece.jpg"
        out_path = os.path.join(dest_dir, out_name)
        
        img_fitted.save(out_path, "JPEG", quality=92, optimize=True)
        print(f"Processed [{saved_count}]: {fname} -> {out_name}")
    except Exception as e:
        print(f"Error processing {fname}: {e}")

print(f"\nTotal {saved_count} images added to assets/gallery/bespoke/ for 3-Piece Suits.")
