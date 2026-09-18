import os
from PIL import Image, ImageStat

assets_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\assets"

for fname in sorted(os.listdir(assets_dir)):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
    fpath = os.path.join(assets_dir, fname)
    try:
        with Image.open(fpath) as img:
            w, h = img.size
            if w > 800 and h > 500:
                rgb = img.convert('RGB')
                # Check right half vs left half
                left = rgb.crop((0, 0, int(w * 0.5), h))
                right = rgb.crop((int(w * 0.5), 0, w, h))
                
                l_stat = ImageStat.Stat(left)
                r_stat = ImageStat.Stat(right)
                
                # Screenshot 2 has dark suit model on the right half (darker right) and lighter wall/background on the left
                # Right half mean RGB vs Left half mean RGB
                lr, lg, lb = l_stat.mean[:3]
                rr, rg, rb = r_stat.mean[:3]
                
                if (rr + rg + rb) < (lr + lg + lb) - 30: # Right is significantly darker than left
                    print(f"MATCH CANDIDATE: {fname} ({w}x{h}) -> Left avg: {lr:.0f}, Right avg: {rr:.0f}")
    except Exception as e:
        pass
