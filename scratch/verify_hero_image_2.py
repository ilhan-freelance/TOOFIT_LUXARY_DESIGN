import os
from PIL import Image, ImageStat

fpath = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\assets\hero_corporate_banner.jpg"
with Image.open(fpath) as img:
    w, h = img.size
    print(f"File: {fpath}")
    print(f"Size: {w}x{h}")
    rgb = img.convert('RGB')
    
    # Model face crop around (x: 65%-85%, y: 0%-35%)
    face_crop = rgb.crop((int(w * 0.65), int(h * 0.05), int(w * 0.85), int(h * 0.35)))
    st = ImageStat.Stat(face_crop)
    print(f"Face area RGB stat: {st.mean[:3]}")
