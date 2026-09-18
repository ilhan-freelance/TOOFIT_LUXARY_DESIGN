import os
from PIL import Image, ImageStat

wedding_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\assets\gallery\wedding"

files = sorted(os.listdir(wedding_dir))
print(f"Total files in wedding gallery: {len(files)}")

matches = []

for fname in files:
    fpath = os.path.join(wedding_dir, fname)
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    
    try:
        with Image.open(fpath) as img:
            w, h = img.size
            rgb = img.convert('RGB')
            
            # Hiring poster aspect ratio is approx 1.48 (e.g. 700x1036 or similar portrait)
            # Center top contains light background
            # Center mid-bottom (y=0.75 to 0.85) contains navy button with phone icon
            # Bottom (y=0.88 to 0.98) contains dark blue footer banner with suit icons
            
            # Sample bottom banner: y from 0.88*h to 0.98*h, x from 0.1*w to 0.9*w
            bot = rgb.crop((int(w * 0.1), int(h * 0.88), int(w * 0.9), int(h * 0.98)))
            bot_stat = ImageStat.Stat(bot)
            br, bg, bb = bot_stat.mean[:3]
            
            # Sample top banner: y from 0 to 0.15*h, x from 0.2*w to 0.8*w
            top = rgb.crop((int(w * 0.2), 0, int(w * 0.8), int(h * 0.15)))
            top_stat = ImageStat.Stat(top)
            tr, tg, tb = top_stat.mean[:3]

            # The bottom banner of hiring poster is dark navy (r<30, g<40, b<70)
            # The top banner is off-white (r>200, g>200, b>200)
            if br < 45 and bg < 50 and bb < 80 and tr > 180 and tg > 180 and tb > 175:
                print(f"MATCH: {fname} | Dimensions: {w}x{h} | Bot RGB: ({br:.0f},{bg:.0f},{bb:.0f}) | Top RGB: ({tr:.0f},{tg:.0f},{tb:.0f})")
                matches.append(fpath)
            else:
                pass
    except Exception as e:
        print(f"Error {fname}: {e}")

print(f"Found {len(matches)} matching hiring flyer files in wedding gallery.")
