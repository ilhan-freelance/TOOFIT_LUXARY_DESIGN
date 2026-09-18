import os
from PIL import Image, ImageStat
import pytesseract

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

print("Searching for the 3 target images...")

found_targets = []

for root, dirs, files in os.walk(base_dir):
    if '.git' in root:
        continue
    for fname in sorted(files):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        fpath = os.path.join(root, fname)
        
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                rgb = img.convert('RGB')
                
                # Check OCR text if fast
                ocr_text = ""
                try:
                    ocr_text = pytesseract.image_to_string(rgb).upper()
                except Exception:
                    pass

                # Target 1: Navy double breasted suit + grey pants (AMANIQUEATTIRE)
                t1_match = False
                if "AMANI" in ocr_text or "QUEATTIRE" in ocr_text or "AMANIQUE" in ocr_text:
                    t1_match = True
                else:
                    # Color check: upper crop navy blue, lower crop grey
                    upper = rgb.crop((int(w * 0.2), int(h * 0.1), int(w * 0.8), int(h * 0.45)))
                    lower = rgb.crop((int(w * 0.3), int(h * 0.5), int(w * 0.7), int(h * 0.9)))
                    
                    u_stat = ImageStat.Stat(upper)
                    l_stat = ImageStat.Stat(lower)
                    
                    ur, ug, ub = u_stat.mean[:3]
                    lr, lg, lb = l_stat.mean[:3]
                    
                    # Navy blue top: R<50, G<60, B>40 (dark navy), Grey bottom: R~140, G~140, B~140
                    if ur < 60 and ug < 65 and ub > 40 and (100 < lr < 190 and 100 < lg < 190 and 100 < lb < 190) and abs(lr-lg)<25 and abs(lg-lb)<25:
                        t1_match = True
                
                # Target 2: Pink/red striped shirt + beige pants (ITALIAN VEGA)
                t2_match = False
                if "VEGA" in ocr_text or "ITALIAN" in ocr_text or "TALIAN" in ocr_text:
                    t2_match = True
                else:
                    upper = rgb.crop((int(w * 0.2), int(h * 0.1), int(w * 0.8), int(h * 0.6)))
                    lower = rgb.crop((int(w * 0.2), int(h * 0.65), int(w * 0.8), int(h * 0.95)))
                    
                    u_stat = ImageStat.Stat(upper)
                    l_stat = ImageStat.Stat(lower)
                    
                    ur, ug, ub = u_stat.mean[:3]
                    lr, lg, lb = l_stat.mean[:3]
                    
                    # Pink/red top (ur > 180, ug < 160, ub < 170), beige bottom (lr > 170, lg > 165, lb > 130)
                    if ur > 175 and ug < 160 and ub < 170 and (lr > 165 and lg > 155 and lb > 120):
                        t2_match = True

                # Target 3: White Jodhpuri suit + gold VR background (VR DESIGNER)
                t3_match = False
                if "VR" in ocr_text or "DESIGNER" in ocr_text:
                    t3_match = True
                else:
                    # White suit center
                    center = rgb.crop((int(w * 0.35), int(h * 0.1), int(w * 0.65), int(h * 0.85)))
                    c_stat = ImageStat.Stat(center)
                    cr, cg, cb = c_stat.mean[:3]
                    
                    # Left & Right background (gold/brown VR circles)
                    left_bg = rgb.crop((0, int(h * 0.1), int(w * 0.2), int(h * 0.8)))
                    lb_stat = ImageStat.Stat(left_bg)
                    lbr, lbg, lbb = lb_stat.mean[:3]
                    
                    # Center is very bright white (cr>210, cg>210, cb>210), sides are gold/yellow-brown (lbr>150, lbg>100, lbb<100)
                    if cr > 200 and cg > 200 and cb > 200 and (lbr > 130 and lbg > 80 and lbb < 100):
                        t3_match = True

                if t1_match:
                    found_targets.append((fpath, "Target 1 (Navy double-breasted suit AMANIQUEATTIRE)"))
                elif t2_match:
                    found_targets.append((fpath, "Target 2 (Pink striped shirt ITALIAN VEGA)"))
                elif t3_match:
                    found_targets.append((fpath, "Target 3 (White Jodhpuri VR DESIGNER)"))
                    
        except Exception as e:
            pass

print(f"\nFound {len(found_targets)} matching image files:")
for fpath, label in found_targets:
    print(f"MATCH: {label} -> {fpath}")
