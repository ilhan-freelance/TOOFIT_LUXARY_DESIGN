import os
import re

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

cat_titles = {
    # Wedding
    'sherwanis': 'Sherwani / Achkan',
    'jodhpuris': 'Royal Jodhpuri Bandgala',
    'designer-coat': 'Designer Coat & Velvet Blazer',
    'wedding-wear': 'Grand Wedding Ceremony Outfit',
    'engagement': 'Engagement & Sagan Ensemble',
    'haldi-mehndi': 'Haldi & Mehndi Silk Set',
    'indo-western': 'Indo-Western Set',
    'hand-painted-shirt': 'Hand Painted Shirt',
    
    # Bespoke
    '3piece': 'Bespoke 3-Piece Suit',
    '2button': 'Classic 2-Button Italian Cut Suit',
    'tuxedo': 'Bespoke Tuxedo',
    'gurkha-pant': 'Pleated Gurkha Trousers',
    'bell-bottom': 'Retro Flare Bell Bottom Pants',
    'embroidered-shirt': 'Luxury Formal Shirt',
    
    # Corporate
    'executive-3piece': 'Executive 3-Piece Power Suit',
    'boardroom-2piece': 'Boardroom 2-Button Suit',
    'power-blazers': 'Executive Power Blazer',
    'formal-shirts': 'Business Formal Shirt',
    'executive-trousers': 'Precision Executive Trousers'
}

def generate_grid_html(dest_folder, prefix, page_type):
    folder_path = os.path.join(base_dir, "assets", "gallery", dest_folder)
    files = sorted(os.listdir(folder_path))
    
    cards_html = []
    for idx, fname in enumerate(files):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        parts = fname.split('_')
        category = parts[2].split('.')[0] if len(parts) >= 3 else 'all'
        title = cat_titles.get(category, f"{page_type.capitalize()} Item {idx+1}")
        img_src = f"assets/gallery/{dest_folder}/{fname}"
        
        # Responsive 2-column mobile card layout
        card = f'''            <!-- Card {idx+1} -->
            <div class="product-card group bg-white rounded-xl border border-[#E5DFD5] p-1.5 sm:p-2 shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer overflow-hidden" data-category="{category}" onclick="openLightbox('{img_src}', '{title}', '{category.replace('-', ' ').title()}')">
              <div class="h-60 sm:h-80 md:h-96 rounded-lg overflow-hidden bg-slate-100 relative">
                <img src="{img_src}" alt="{title}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <span class="bg-white/90 text-slate-900 text-[10px] sm:text-xs font-semibold px-3 py-1.5 sm:px-4 sm:py-2 rounded-full shadow-md tracking-wider uppercase">View Photo</span>
                </div>
              </div>
            </div>'''
        cards_html.append(card)
        
    return "\n\n".join(cards_html)

lightbox_html = '''
  <!-- LIGHTBOX MODAL FOR HIGH-RES VIEW -->
  <div id="lightbox-modal" class="fixed inset-0 z-[2000] bg-black/90 backdrop-blur-md hidden flex items-center justify-center p-3 sm:p-4">
    <button onclick="closeLightbox()" class="absolute top-4 right-4 sm:top-6 sm:right-6 text-white hover:text-[#C59B27] text-3xl font-bold transition-colors z-10">&times;</button>
    <div class="max-w-4xl max-h-[90vh] flex flex-col items-center justify-center text-center space-y-3 p-2">
      <img id="lightbox-img" src="" alt="Enlarged Garment View" class="max-h-[70vh] sm:max-h-[75vh] w-auto max-w-full rounded-lg shadow-2xl object-contain">
      <h3 id="lightbox-title" class="text-white font-serif text-lg sm:text-2xl tracking-wide"></h3>
      <span id="lightbox-category" class="text-[#C59B27] text-[10px] sm:text-xs font-semibold uppercase tracking-[0.25em]"></span>
    </div>
  </div>

  <script>
    function openLightbox(src, title, category) {
      document.getElementById('lightbox-img').src = src;
      document.getElementById('lightbox-title').innerText = title;
      document.getElementById('lightbox-category').innerText = category;
      document.getElementById('lightbox-modal').classList.remove('hidden');
    }

    function closeLightbox() {
      document.getElementById('lightbox-modal').classList.add('hidden');
    }

    document.getElementById('lightbox-modal').addEventListener('click', function(e) {
      if (e.target === this) closeLightbox();
    });
  </script>'''

def update_file(filename, dest_folder, prefix, page_type):
    file_path = os.path.join(base_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_grid_html = generate_grid_html(dest_folder, prefix, page_type)
    
    # Update product-grid wrapper to grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-6
    grid_start_pattern = r'<div id="product-grid"[^>]*>'
    grid_start_replacement = '<div id="product-grid" class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-6 min-h-[300px]">'
    content = re.sub(grid_start_pattern, grid_start_replacement, content)

    # Replace grid content between <div id="product-grid"...> and </div>
    pattern = r'(<div id="product-grid"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)'
    replacement = r'\1\n' + new_grid_html + r'\n          \3'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Add lightbox before </body> if not present
    if 'id="lightbox-modal"' not in updated_content:
        updated_content = updated_content.replace('</body>', lightbox_html + '\n</body>')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Updated {filename} with 2-column responsive cards.")

if __name__ == "__main__":
    update_file('wedding.html', 'wedding', 'wedding', 'wedding')
    update_file('bespoke.html', 'bespoke', 'bespoke', 'bespoke')
    update_file('corporate.html', 'corporate', 'corporate', 'corporate')
