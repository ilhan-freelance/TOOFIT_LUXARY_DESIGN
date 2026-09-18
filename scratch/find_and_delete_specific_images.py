import os
import pytesseract
from PIL import Image, ImageStat

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

deleted_files = []

def check_hiring_poster_2(img, fpath):
    # 1. OCR check
    try:
        rgb = img.convert('RGB')
        text = pytesseract.image_to_string(rgb).upper()
        keywords = ['HIRING', 'URGENT', 'BUSINESS DEVELOPMENT', 'REQUIREMENT', 'SHOWROOM', 'GROWTH JOURNEY', 'APPLY NOW']
        for kw in keywords:
            if kw in text:
                return True, f"OCR matched: '{kw}'"
    except Exception:
        pass

    # 2. Visual fingerprint check for Flyer 2 ("URGENT REQUIREMENT WE ARE HIRING"):
    # Has a dark blue starburst at top left (x:5%-30%, y:0%-10%)
    w, h = img.size
    top_left = img.crop((int(w * 0.05), int(h * 0.01), int(w * 0.35), int(h * 0.12)))
    stat_tl = ImageStat.Stat(top_left.convert('RGB'))
    r, g, b = stat_tl.mean[:3]
    
    # If top left has dark blue starburst badge (r<40, g<50, b>60 or dark blue)
    if (r < 50 and g < 60 and b > 50) and h > w:
        return True, "Visual match: Blue URGENT badge top-left"
        
    return False, "Clean"

def check_gate_rendering(img, fpath):
    w, h = img.size
    rgb = img.convert('RGB')
    
    # Check filename
    fname_lower = os.path.basename(fpath).lower()
    if 'mansion' in fname_lower or 'gate' in fname_lower or 'fence' in fname_lower:
        return True, "Filename matches gate/mansion"
        
    # Check bottom center metal gate bars (y: 60%-95%, x: 10%-90%)
    # Gate image has horizontal dark grey frame top with warm yellow LED line
    top_strip = rgb.crop((int(w * 0.1), int(h * 0.05), int(w * 0.9), int(h * 0.25)))
    top_stat = ImageStat.Stat(top_strip)
    tr, tg, tb = top_stat.mean[:3]
    
    # Gate image top overhang is grey ~ (80-120, 80-120, 80-120) with bright yellow LED streak
    # Bottom gate bars are dark grey ~ (40-75, 40-75, 40-75)
    bot_gate = rgb.crop((int(w * 0.2), int(h * 0.7), int(w * 0.8), int(h * 0.95)))
    bot_stat = ImageStat.Stat(bot_gate)
    br, bg, bb = bot_stat.mean[:3]
    
    if (65 < tr < 140 and 65 < tg < 140 and 65 < tb < 140) and (30 < br < 95 and 30 < bg < 95 and 30 < bb < 95):
        # Additional check: color stddev across gate vertical bars
        if bot_stat.stddev[0] > 35 or top_stat.stddev[0] > 35:
            return True, "Visual match: Gate/Fence architectural rendering"

    return False, "Clean"

print("Scanning all directories in workspace for poster and gate images...")

for root, dirs, files in os.walk(base_dir):
    if '.git' in root or 'node_modules' in root:
        continue
    for fname in sorted(files):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        fpath = os.path.join(root, fname)
        
        try:
            with Image.open(fpath) as img:
                is_poster, p_reason = check_hiring_poster_2(img, fpath)
                is_gate, g_reason = check_gate_rendering(img, fpath)
                
                if is_poster or is_gate:
                    reason = p_reason if is_poster else g_reason
                    print(f"DELETING: {fpath} -> {reason}")
                    img.close()
                    try:
                        os.remove(fpath)
                        deleted_files.append((fpath, reason))
                    except Exception as err:
                        print(f"Failed to remove {fpath}: {err}")
        except Exception as e:
            pass

print(f"\nDone! Deleted {len(deleted_files)} non-garment image files.")
