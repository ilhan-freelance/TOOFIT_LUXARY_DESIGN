import os
import shutil
from PIL import Image, ImageOps

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
toofit_data_dir = os.path.join(base_dir, "Toofit data")
dest_dir = os.path.join(base_dir, "assets", "gallery", "bespoke")

os.makedirs(dest_dir, exist_ok=True)

# Folder name mapping to category keys
folder_to_cat = {
    '3 piece suit': '3piece',
    '3piece': '3piece',
    '2 piece suit': '2button',
    '2piece': '2button',
    '2button': '2button',
    'tuxedo': 'tuxedo',
    'tuxedos': 'tuxedo',
    'gurkha': 'gurkha-pant',
    'gurkha pant': 'gurkha-pant',
    'gurkha pants': 'gurkha-pant',
    'gurkha trousers': 'gurkha-pant',
    'bell bottom': 'bell-bottom',
    'bellbottom': 'bell-bottom',
    'bell bottom pants': 'bell-bottom',
    'formal shirt': 'embroidered-shirt',
    'formal shirts': 'embroidered-shirt',
    'shirt': 'embroidered-shirt',
    'shirts': 'embroidered-shirt'
}

print("Scanning 'Toofit data' directory for category images...")

# We clear old category images for folders that are being updated
subfolders = os.listdir(toofit_data_dir)

for folder_name in subfolders:
    src_folder = os.path.join(toofit_data_dir, folder_name)
    if not os.path.isdir(src_folder):
        continue
        
    cat_key = folder_to_cat.get(folder_name.lower().strip())
    if not cat_key:
        print(f"Skipping unknown folder: {folder_name}")
        continue
        
    print(f"\nProcessing '{folder_name}' -> Category: '{cat_key}'")
    
    # Remove existing gallery images for this specific category before processing
    for f in os.listdir(dest_dir):
        if f.endswith(f"_{cat_key}.jpg"):
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
            out_name = f"bespoke_{saved_count:02d}_{cat_key}.jpg"
            out_path = os.path.join(dest_dir, out_name)
            
            img_fitted.save(out_path, "JPEG", quality=92, optimize=True)
            print(f"[{saved_count}] Processed: {fname} -> {out_name}")
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    print(f"Category '{cat_key}' updated with {saved_count} images.")

print("\nDone processing all user data folders.")
