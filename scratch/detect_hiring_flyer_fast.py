import os
from PIL import Image, ImageStat

gallery_base = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\assets\gallery"

target_files = []

for root, dirs, files in os.walk(gallery_base):
    for fname in files:
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        fpath = os.path.join(root, fname)
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                rgb = img.convert('RGB')
                
                # Check bottom 10% (the dark navy "PREMIUM WEDDING WEAR SOLUTIONS" bar)
                bot_bar = rgb.crop((0, int(h * 0.90), w, h))
                stat_bot = ImageStat.Stat(bot_bar)
                b_r, b_g, b_b = stat_bot.mean[:3]
                
                # Check top left 30% x 20% (the off-white header background behind "WE'RE HIRING")
                top_left = rgb.crop((0, 0, int(w * 0.4), int(h * 0.2)))
                stat_tl = ImageStat.Stat(top_left)
                tl_r, tl_g, tl_b = stat_tl.mean[:3]
                
                # The hiring poster has dark navy bottom bar (R<20, G<35, B<60) and off-white top-left (R>220, G>220, B>220)
                if (b_r < 30 and b_g < 40 and b_b < 70) and (tl_r > 200 and tl_g > 200 and tl_b > 200):
                    # Check if there is a golden phone button in bottom middle
                    apply_btn = rgb.crop((int(w * 0.1), int(h * 0.7), int(w * 0.6), int(h * 0.85)))
                    stat_btn = ImageStat.Stat(apply_btn)
                    btn_r, btn_g, btn_b = stat_btn.mean[:3]
                    
                    print(f"MATCHED HIRING FLYER: {fpath} | Dimensions: {w}x{h}")
                    target_files.append(fpath)
        except Exception as e:
            print(f"Error checking {fpath}: {e}")

print(f"\nFound {len(target_files)} hiring flyers.")
