import os
from PIL import Image, ImageStat

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

print("Scanning all directories for the 3 target images by color and visual structure...")

candidates_img1 = [] # Navy suit + grey pants
candidates_img2 = [] # Pink striped shirt + tan pants
candidates_img3 = [] # White suit + gold VR background

for root, dirs, files in os.walk(base_dir):
    if '.git' in root or 'node_modules' in root:
        continue
    for fname in sorted(files):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        fpath = os.path.join(root, fname)
        
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                if w < 50 or h < 50:
                    continue
                rgb = img.convert('RGB')
                
                # Image 1 Check: Navy Top (R<60, G<60, B>45) & Grey Bottom (100<R<190, 100<G<190, 100<B<190)
                top1 = rgb.crop((int(w * 0.2), int(h * 0.05), int(w * 0.8), int(h * 0.4)))
                bot1 = rgb.crop((int(w * 0.3), int(h * 0.55), int(w * 0.7), int(h * 0.9)))
                
                st_top1 = ImageStat.Stat(top1)
                st_bot1 = ImageStat.Stat(bot1)
                
                tr1, tg1, tb1 = st_top1.mean[:3]
                br1, bg1, bb1 = st_bot1.mean[:3]
                
                if tr1 < 75 and tg1 < 75 and tb1 > 45 and (100 < br1 < 190 and 100 < bg1 < 190 and 100 < bb1 < 190) and abs(br1-bg1) < 20 and abs(bg1-bb1) < 20:
                    candidates_img1.append((fpath, f"Top: ({tr1:.1f},{tg1:.1f},{tb1:.1f}), Bot: ({br1:.1f},{bg1:.1f},{bb1:.1f})"))

                # Image 2 Check: Pink/Red Top (tr2>170, tg2<160) & Tan/Khaki Bottom (br2>170, bg2>165, bb2>120)
                top2 = rgb.crop((int(w * 0.15), int(h * 0.1), int(w * 0.85), int(h * 0.6)))
                bot2 = rgb.crop((int(w * 0.2), int(h * 0.65), int(w * 0.8), int(h * 0.95)))
                
                st_top2 = ImageStat.Stat(top2)
                st_bot2 = ImageStat.Stat(bot2)
                
                tr2, tg2, tb2 = st_top2.mean[:3]
                br2, bg2, bb2 = st_bot2.mean[:3]
                
                if tr2 > 165 and tg2 < 165 and tb2 < 175 and (br2 > 160 and bg2 > 150 and bb2 > 115) and (br2 - bb2 > 25):
                    candidates_img2.append((fpath, f"Top: ({tr2:.1f},{tg2:.1f},{tb2:.1f}), Bot: ({br2:.1f},{bg2:.1f},{bb2:.1f})"))

                # Image 3 Check: White suit center (cr3>200, cg3>200, cb3>200) & Gold/brown sides (lbr3>130, lbg3>80, lbb3<110)
                center3 = rgb.crop((int(w * 0.3), int(h * 0.05), int(w * 0.7), int(h * 0.85)))
                side3 = rgb.crop((0, int(h * 0.2), int(w * 0.18), int(h * 0.8)))
                
                st_center3 = ImageStat.Stat(center3)
                st_side3 = ImageStat.Stat(side3)
                
                cr3, cg3, cb3 = st_center3.mean[:3]
                sr3, sg3, sb3 = st_side3.mean[:3]
                
                if cr3 > 195 and cg3 > 195 and cb3 > 195 and (sr3 > 120 and sg3 > 70 and sb3 < 110) and (sr3 - sb3 > 40):
                    candidates_img3.append((fpath, f"Center: ({cr3:.1f},{cg3:.1f},{cb3:.1f}), Side: ({sr3:.1f},{sg3:.1f},{sb3:.1f})"))

        except Exception as e:
            pass

print("\n--- Candidate Image 1 (Navy Suit + Grey Pants) ---")
for c in candidates_img1:
    print(f"{c[0]} | {c[1]}")

print("\n--- Candidate Image 2 (Pink Striped Shirt + Tan Pants) ---")
for c in candidates_img2:
    print(f"{c[0]} | {c[1]}")

print("\n--- Candidate Image 3 (White Suit + Gold VR Background) ---")
for c in candidates_img3:
    print(f"{c[0]} | {c[1]}")
