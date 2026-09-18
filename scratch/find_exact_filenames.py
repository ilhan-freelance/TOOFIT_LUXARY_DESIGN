import os
from PIL import Image, ImageStat

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

def analyze_folder(folder_path):
    print(f"\n--- Analyzing: {folder_path} ---")
    if not os.path.exists(folder_path):
        return
    for fname in sorted(os.listdir(folder_path)):
        fpath = os.path.join(folder_path, fname)
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                rgb = img.convert('RGB')
                # Top half stat
                top = rgb.crop((int(w * 0.1), int(h * 0.05), int(w * 0.9), int(h * 0.5)))
                st = ImageStat.Stat(top)
                r, g, b = st.mean[:3]
                print(f"{fname} ({w}x{h}): Top RGB=({r:.0f},{g:.0f},{b:.0f})")
        except Exception as e:
            print(f"Error {fname}: {e}")

analyze_folder(os.path.join(base_dir, "Toofit data", "Formal shirts"))
analyze_folder(os.path.join(base_dir, "Toofit data", "Jodhpuri"))
analyze_folder(os.path.join(base_dir, "Toofit data", "2 piece suit"))
