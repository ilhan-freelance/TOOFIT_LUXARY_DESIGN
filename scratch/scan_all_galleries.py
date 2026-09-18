import os
from PIL import Image, ImageStat

gallery_base = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\assets\gallery"

deleted_files = []

for root, dirs, files in os.walk(gallery_base):
    for fname in sorted(files):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        fpath = os.path.join(root, fname)
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                rgb = img.convert('RGB')
                
                # Check bottom banner and top banner
                bot = rgb.crop((int(w * 0.1), int(h * 0.88), int(w * 0.9), int(h * 0.98)))
                bot_stat = ImageStat.Stat(bot)
                br, bg, bb = bot_stat.mean[:3]
                
                top = rgb.crop((int(w * 0.2), 0, int(w * 0.8), int(h * 0.15)))
                top_stat = ImageStat.Stat(top)
                tr, tg, tb = top_stat.mean[:3]
                
                # Also check specific PNG filename or dimensions
                if (br < 45 and bg < 50 and bb < 80 and tr > 180 and tg > 180 and tb > 175) or fname == 'wedding_001_sherwanis.png':
                    print(f"DELETING HIRING FLYER: {fpath}")
                    img.close()
                    os.remove(fpath)
                    deleted_files.append(fpath)
        except Exception as e:
            print(f"Error {fpath}: {e}")

print(f"\nSuccessfully deleted {len(deleted_files)} hiring flyer image(s).")
