import os
from PIL import Image, ImageStat
import collections

toofit_data = r"c:\Users\asus\Documents\TOOFIT_TRAILORS\Toofit data"

subdirs = {
    'wedding': os.path.join(toofit_data, "Wedding 1"),
    'folder_a': os.path.join(toofit_data, "202609_a"),
    'folder_b': os.path.join(toofit_data, "202609_b"),
}

def analyze_image(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
            aspect = h / w if w > 0 else 1.0
            
            # Convert to RGB for color analysis
            rgb_img = img.convert('RGB')
            
            # Crop top 30% (neck/collar area) and middle 40% (torso) and bottom 30% (legs/trousers)
            top_crop = rgb_img.crop((0, 0, w, int(h * 0.3)))
            mid_crop = rgb_img.crop((0, int(h * 0.3), w, int(h * 0.7)))
            bot_crop = rgb_img.crop((0, int(h * 0.7), w, h))
            
            stat_top = ImageStat.Stat(top_crop)
            stat_mid = ImageStat.Stat(mid_crop)
            stat_bot = ImageStat.Stat(bot_crop)
            
            # Average RGB values
            r_avg, g_avg, b_avg = stat_mid.mean[:3]
            
            # Brightness & Saturation estimate
            brightness = (r_avg + g_avg + b_avg) / 3.0
            
            # Red/Gold dominance (high R, medium G, low B)
            is_gold_red = (r_avg > 1.2 * b_avg) and (r_avg > 80)
            
            # Dark formal (Navy/Black/Charcoal)
            is_dark = brightness < 90
            
            # White/Cream/Light
            is_light_cream = brightness > 160 and abs(r_avg - g_avg) < 30
            
            return {
                'width': w, 'height': h, 'aspect': aspect,
                'brightness': brightness,
                'r': r_avg, 'g': g_avg, 'b': b_avg,
                'is_gold_red': is_gold_red,
                'is_dark': is_dark,
                'is_light_cream': is_light_cream
            }
    except Exception as e:
        return None

print("Analyzing sample images...")

wedding_files = os.listdir(subdirs['wedding'])[:10]
for f in wedding_files:
    p = os.path.join(subdirs['wedding'], f)
    info = analyze_image(p)
    if info:
        print(f"Wedding {f}: aspect={info['aspect']:.2f}, bright={info['brightness']:.1f}, RGB=({info['r']:.0f},{info['g']:.0f},{info['b']:.0f})")

folder_a_files = os.listdir(subdirs['folder_a'])[:10]
for f in folder_a_files:
    p = os.path.join(subdirs['folder_a'], f)
    info = analyze_image(p)
    if info:
        print(f"FolderA {f}: aspect={info['aspect']:.2f}, bright={info['brightness']:.1f}, RGB=({info['r']:.0f},{info['g']:.0f},{info['b']:.0f})")
