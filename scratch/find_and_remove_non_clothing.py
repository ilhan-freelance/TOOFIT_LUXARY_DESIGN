import os
import glob
from PIL import Image, ImageStat

toofit_data = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\Toofit data"

subdirs = [
    os.path.join(toofit_data, "Wedding 1"),
    os.path.join(toofit_data, "202609_a"),
    os.path.join(toofit_data, "202609_b")
]

non_clothing_files = []

for sdir in subdirs:
    for fname in os.listdir(sdir):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        fpath = os.path.join(sdir, fname)
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                
                # Convert to RGB
                rgb = img.convert('RGB')
                
                # Check for "WE'RE HIRING" or gate/house image characteristics:
                # 1. Gates/House image often has grey concrete top, dark metal bars in middle, green grass/grey floor at bottom
                # 2. Hiring poster has dark header with large gold text block, top left logo, call phone block
                
                # Sample colors
                stat = ImageStat.Stat(rgb)
                r_avg, g_avg, b_avg = stat.mean[:3]
                
                # Top crop & Bottom crop
                top = rgb.crop((0, 0, w, int(h * 0.2)))
                bot = rgb.crop((0, int(h * 0.8), w, h))
                
                top_stat = ImageStat.Stat(top)
                bot_stat = ImageStat.Stat(bot)
                
                # If image contains gate/house or hiring poster text:
                # Let's inspect size & path to log it
                print(f"Path: {fpath} | Size: {w}x{h} | RGB: ({r_avg:.0f}, {g_avg:.0f}, {b_avg:.0f})")
                
        except Exception as e:
            print(f"Error opening {fpath}: {e}")
