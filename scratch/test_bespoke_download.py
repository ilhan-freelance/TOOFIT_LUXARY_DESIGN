import os
import re
import json
import io
import urllib.parse
import requests
from PIL import Image, ImageOps

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"
output_dir = os.path.join(base_dir, "assets", "gallery", "bespoke")
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_bing_image_urls(query, max_count=40):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        urls = re.findall(r'&quot;murl&quot;:&quot;(.*?)&quot;', resp.text)
        # Deduplicate
        seen = set()
        clean_urls = []
        for u in urls:
            if u not in seen and not u.endswith('.svg') and not u.endswith('.gif'):
                seen.add(u)
                clean_urls.append(u)
        return clean_urls[:max_count]
    except Exception as e:
        print(f"Search failed for '{query}': {e}")
        return []

def download_and_crop_garment(url, target_size=(600, 800)):
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code != 200:
            return None
        
        img = Image.open(io.BytesIO(resp.content)).convert('RGB')
        w, h = img.size
        
        if w < 250 or h < 300:
            return None
            
        # Check aspect ratio. If tall portrait (likely model standing), crop top 20% to remove face
        aspect = h / float(w)
        if aspect >= 1.2:
            # Crop top 20% off to guarantee no face
            crop_top = int(h * 0.20)
            img = img.crop((0, crop_top, w, h))
            w, h = img.size

        # Fit image to 600x800
        img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        return None

queries_map = {
    '3piece': [
        'mens 3 piece suit ghost mannequin studio photography',
        'bespoke 3 piece suit flat lay menswear',
        'mens 3 piece tweed suit hanger photoshoot',
        'luxury 3 piece suit clothing detail studio'
    ],
    '2button': [
        'mens 2 button suit ghost mannequin studio',
        'classic 2 button suit jacket flat lay menswear',
        'mens tailored suit jacket hanger studio',
        'mens formal 2 piece suit clothing photography'
    ],
    'tuxedo': [
        'black tie tuxedo ghost mannequin studio',
        'mens tuxedo jacket flat lay luxury menswear',
        'velvet tuxedo jacket hanger studio photo',
        'mens dinner suit jacket product photography'
    ],
    'gurkha-pant': [
        'mens gurkha trousers flat lay studio',
        'pleated gurkha pants clothing photography',
        'mens gurkha trousers hanger product photography',
        'tailored gurkha trousers menswear detail'
    ],
    'bell-bottom': [
        'mens bell bottom trousers studio photography',
        'flared mens suit pants flat lay studio',
        'retro mens flared trousers clothing photo',
        'mens wide leg trousers hanger studio'
    ],
    'embroidered-shirt': [
        'mens formal dress shirt flat lay studio',
        'mens luxury dress shirt ghost mannequin',
        'mens tailored shirt folded product photography',
        'mens white formal shirt hanger studio photo'
    ]
}

print("Testing download pipeline...")
for cat, q_list in queries_map.items():
    print(f"\n--- Category: {cat} ---")
    urls = []
    for q in q_list:
        urls.extend(search_bing_image_urls(q, max_count=15))
    print(f"Total candidate URLs found for {cat}: {len(urls)}")
