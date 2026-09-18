import os
import shutil
import re

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

files = ['bespoke.html', 'wedding.html', 'corporate.html']

placeholder_html = '''          <div id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5 sm:gap-6 min-h-[350px] flex items-center justify-center">
            <div class="col-span-full text-center py-20 bg-white/70 rounded-2xl border border-dashed border-[#C59B27]/40 p-8 shadow-sm space-y-3">
              <div class="w-12 h-12 mx-auto rounded-full bg-[#FAF6EF] flex items-center justify-center text-[#C59B27]">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              </div>
              <h3 class="font-serif font-semibold text-lg text-[#0A192F]">Curated Collection Gallery</h3>
              <p class="text-xs text-slate-500 max-w-md mx-auto uppercase tracking-wider">Category filtering ready &bull; Select a category from the sidebar or upload raw images to populate this gallery</p>
            </div>
          </div>'''

for fname in files:
    fpath = os.path.join(base_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match <div id="product-grid"...> ... </div> (the grid section inside <div class="lg:col-span-3">)
    pattern = r'<div id="product-grid"[^>]*>.*?</div>\s*</div>\s*</div>\s*</section>'
    
    # We replace product-grid with the clean placeholder state
    replacement = placeholder_html + '\n        </div>\n      </div>\n    </section>'
    
    updated = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(updated)

    print(f"Removed all product grid images from {fname}.")

# Clear out assets/gallery/ folder
gallery_dir = os.path.join(base_dir, "assets", "gallery")
if os.path.exists(gallery_dir):
    shutil.rmtree(gallery_dir, ignore_errors=True)
    os.makedirs(gallery_dir, exist_ok=True)
    print("Cleared assets/gallery directory.")
