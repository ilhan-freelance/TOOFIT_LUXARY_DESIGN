import os
from PIL import Image, ImageOps, ImageStat
import pytesseract

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

# ==========================================
# 1. PROCESS & ADD HAND PAINTED SHIRTS
# ==========================================
src_folder = os.path.join(base_dir, "Toofit data", "Hand painted shirts")
dest_dir = os.path.join(base_dir, "assets", "gallery", "wedding")

os.makedirs(dest_dir, exist_ok=True)

# Remove old hand-painted-shirt images in assets/gallery/wedding/
for f in os.listdir(dest_dir):
    if f.endswith("_hand-painted-shirt.jpg") or f.endswith("_hand-painted-shirt.png"):
        try:
            os.remove(os.path.join(dest_dir, f))
        except Exception as e:
            print(f"Error deleting old file {f}: {e}")

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
        out_name = f"wedding_{saved_count:02d}_hand-painted-shirt.jpg"
        out_path = os.path.join(dest_dir, out_name)
        
        img_fitted.save(out_path, "JPEG", quality=92, optimize=True)
        print(f"[{saved_count}] Processed Hand-Painted Shirt: {fname} -> {out_name}")
    except Exception as e:
        print(f"Error processing {fname}: {e}")

print(f"\nSuccessfully added {saved_count} Hand-Painted Shirt images to assets/gallery/wedding/")

# ==========================================
# 2. SEARCH & REMOVE THE 3 SPECIFIC IMAGES
# ==========================================
print("\nChecking for the 3 target images to remove...")
removed_count = 0

for root, dirs, files_in_dir in os.walk(base_dir):
    if '.git' in root:
        continue
    for fname in sorted(files_in_dir):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        fpath = os.path.join(root, fname)
        
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                rgb = img.convert('RGB')
                
                text = ""
                try:
                    text = pytesseract.image_to_string(rgb).upper()
                except Exception:
                    pass
                
                # Check for Image 1: AMANIQUEATTIRE
                is_img1 = "AMANI" in text or "QUEATTIRE" in text
                
                # Check for Image 2: ITALIAN VEGA pink striped shirt
                is_img2 = "VEGA" in text or "ITALIAN" in text
                
                # Check for Image 3: VR DESIGNER white suit
                is_img3 = "VR" in text and "DESIGNER" in text
                
                if is_img1 or is_img2 or is_img3:
                    print(f"REMOVING TARGET IMAGE: {fpath} (Matched watermark)")
                    img.close()
                    try:
                        os.remove(fpath)
                        removed_count += 1
                    except Exception as err:
                        print(f"Failed to remove {fpath}: {err}")
        except Exception:
            pass

print(f"Removed {removed_count} target watermarked images.")

# ==========================================
# 3. REBUILD WEDDING GALLERY GRID
# ==========================================
from update_html_galleries import update_file
update_file('wedding.html', 'wedding', 'wedding', 'wedding')
print("Updated wedding.html gallery grid successfully!")
