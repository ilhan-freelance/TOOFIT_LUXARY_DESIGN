import os
import re
import json
import io
import time
import urllib.parse
import requests
from PIL import Image, ImageOps, ImageEnhance

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
output_dir = os.path.join(base_dir, "assets", "gallery", "bespoke")

os.makedirs(output_dir, exist_ok=True)
# Clear out old images to populate fresh 50 images per category
for f in os.listdir(output_dir):
    if f.startswith("bespoke_"):
        try:
            os.remove(os.path.join(output_dir, f))
        except Exception:
            pass

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
}

def search_bing_image_urls(query, max_count=60):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        urls = re.findall(r'&quot;murl&quot;:&quot;(.*?)&quot;', resp.text)
        clean_urls = []
        seen = set()
        for u in urls:
            if u not in seen and not u.lower().endswith(('.svg', '.gif', '.ico')):
                seen.add(u)
                clean_urls.append(u)
        return clean_urls[:max_count]
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
        return []

def download_and_crop_garment(url, target_size=(600, 800)):
    try:
        resp = requests.get(url, headers=headers, timeout=7)
        if resp.status_code != 200 or len(resp.content) < 5000:
            return None
        
        img = Image.open(io.BytesIO(resp.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        w, h = img.size
        if w < 220 or h < 250:
            return None
            
        # Crop top 22% off to strictly remove model face/head if present
        aspect = h / float(w)
        if aspect >= 1.15:
            crop_top = int(h * 0.22)
            img = img.crop((0, crop_top, w, h))
            w, h = img.size

        # Fit into crisp 600x800 portrait card
        img_fitted = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)
        
        # Subtle contrast enhancement for crisp studio feel
        enhancer = ImageEnhance.Contrast(img_fitted)
        img_final = enhancer.enhance(1.05)
        
        return img_final
    except Exception:
        return None

queries_config = {
    '3piece': [
        'mens 3 piece suit mannequin flat lay studio',
        'bespoke 3 piece suit ghost mannequin product photo',
        'mens 3 piece tweed suit hanger studio',
        'luxury 3 piece suit clothing photography studio',
        'mens 3 piece navy suit flat lay detail',
        'mens 3 piece grey check suit mannequin',
        'mens pinstripe 3 piece suit ghost mannequin',
        'mens double breasted 3 piece suit flat lay',
        'mens wedding 3 piece suit hanger studio',
        'mens wool 3 piece suit mannequin photoshoot',
        'mens charcoal 3 piece suit clothing photography',
        'mens houndstooth 3 piece suit flat lay studio'
    ],
    '2button': [
        'mens 2 button suit ghost mannequin studio',
        'classic 2 button suit jacket flat lay menswear',
        'mens bespoke suit jacket hanger studio photography',
        'mens double breasted suit jacket flat lay studio',
        'mens navy blue 2 button suit mannequin',
        'mens charcoal suit jacket product photography',
        'mens Italian wool 2 button suit mannequin',
        'mens linen suit jacket flat lay studio',
        'mens blazer jacket clothing photography hanger',
        'mens beige 2 button suit flat lay studio',
        'mens windowpane suit jacket ghost mannequin',
        'mens slim fit 2 button suit jacket mannequin'
    ],
    'tuxedo': [
        'mens black tie tuxedo ghost mannequin studio',
        'mens tuxedo jacket flat lay luxury menswear',
        'velvet tuxedo jacket hanger studio photo',
        'mens dinner suit jacket product photography',
        'mens shawl lapel tuxedo jacket mannequin',
        'mens midnight blue tuxedo flat lay',
        'mens white tuxedo jacket dinner jacket mannequin',
        'mens peak lapel tuxedo jacket clothing photography',
        'mens double breasted tuxedo flat lay studio',
        'mens burgundy velvet tuxedo jacket hanger',
        'mens jacquard tuxedo jacket ghost mannequin',
        'mens satin lapel tuxedo jacket flat lay'
    ],
    'gurkha-pant': [
        'mens gurkha trousers flat lay studio',
        'pleated gurkha pants clothing photography',
        'mens gurkha trousers hanger product photography',
        'tailored gurkha trousers menswear detail',
        'mens high waisted gurkha trousers flat lay',
        'mens cotton linen gurkha pants mannequin',
        'mens wool gurkha trousers clothing photo',
        'mens double pleat gurkha trousers studio',
        'mens beige gurkha trousers flat lay',
        'mens navy gurkha pants hanger photography',
        'mens khaki gurkha trousers product photo',
        'mens olive green gurkha trousers flat lay'
    ],
    'bell-bottom': [
        'mens bell bottom trousers studio photography',
        'flared mens suit pants flat lay studio',
        'retro mens flared trousers clothing photo',
        'mens wide leg trousers hanger studio',
        'mens 70s flare trousers flat lay menswear',
        'mens tailored flared pants product photography',
        'mens bootcut suit pants flat lay studio',
        'mens flared trousers hanger product photo',
        'mens vintage bell bottom pants mannequin',
        'mens wool flared trousers flat lay',
        'mens pinstripe flared pants clothing photo',
        'mens wide leg flared trousers studio photo'
    ],
    'embroidered-shirt': [
        'mens formal dress shirt flat lay studio',
        'mens luxury dress shirt ghost mannequin',
        'mens tailored shirt folded product photography',
        'mens white formal shirt hanger studio photo',
        'mens cotton formal dress shirt flat lay',
        'mens french cuff formal shirt mannequin',
        'mens oxford formal dress shirt folded',
        'mens blue formal shirt flat lay studio',
        'mens tuxedo dress shirt bib front mannequin',
        'mens spread collar formal shirt hanger photo',
        'mens pin point cotton dress shirt flat lay',
        'mens herringbone formal shirt ghost mannequin'
    ]
}

TARGET_COUNT_PER_CAT = 50

print("Starting garment download & processing pipeline for 50 images per category...")

for category, q_list in queries_config.items():
    print(f"\n==========================================")
    print(f"Processing Category: {category} (Target: 50 unique images)")
    print(f"==========================================")
    
    saved_count = 0
    candidate_urls = []
    
    for q in q_list:
        urls = search_bing_image_urls(q, max_count=50)
        for u in urls:
            if u not in candidate_urls:
                candidate_urls.append(u)
                
    print(f"Found {len(candidate_urls)} candidate URLs for category '{category}'")
    
    for idx, url in enumerate(candidate_urls):
        if saved_count >= TARGET_COUNT_PER_CAT:
            break
            
        img = download_and_crop_garment(url)
        if img is not None:
            saved_count += 1
            filename = f"bespoke_{saved_count:02d}_{category}.jpg"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, "JPEG", quality=90, optimize=True)
            print(f"[{saved_count}/{TARGET_COUNT_PER_CAT}] Saved: {filename}")
            
    print(f"Category '{category}' complete! Total saved: {saved_count}/{TARGET_COUNT_PER_CAT}")

print("\nFinished downloading 50 images for all 6 bespoke categories!")
