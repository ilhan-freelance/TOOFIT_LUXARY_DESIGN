import os
from PIL import Image, ImageOps

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
src_folder = os.path.join(base_dir, "Toofit data", "Jodhpuri")
dest_dir = os.path.join(base_dir, "assets", "gallery", "wedding")

os.makedirs(dest_dir, exist_ok=True)

# Remove old jodhpuris images in assets/gallery/wedding/
for f in os.listdir(dest_dir):
    if f.endswith("_jodhpuris.jpg") or f.endswith("_jodhpuris.png"):
        try:
            os.remove(os.path.join(dest_dir, f))
        except Exception:
            pass

files = sorted(os.listdir(src_folder))
saved_count = 0

for fname in files:
    ext = os.path.splitext(fname)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        continue
        
    src_path = os.path.join(src_folder, fname)
    try:
        img = Image.open(src_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img_fitted = ImageOps.fit(img, (600, 800), Image.Resampling.LANCZOS)
        
        saved_count += 1
        out_name = f"wedding_{saved_count:02d}_jodhpuris.jpg"
        out_path = os.path.join(dest_dir, out_name)
        
        img_fitted.save(out_path, "JPEG", quality=92, optimize=True)
        print(f"[{saved_count}] Processed: {fname} -> {out_name}")
    except Exception as e:
        print(f"Error processing {fname}: {e}")

print(f"\nSuccessfully added {saved_count} Jodhpuri images to assets/gallery/wedding/")
