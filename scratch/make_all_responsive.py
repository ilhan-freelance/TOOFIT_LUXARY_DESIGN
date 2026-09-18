import os
import re

base_dir = r"c:\Users\asus\Documents\TOOFIT_TRAILORS"

files_to_update = ['wedding.html', 'bespoke.html', 'corporate.html']

for fname in files_to_update:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Make <ul class="space-y-1 text-xs"> responsive horizontal scroll on mobile, vertical sidebar on desktop
    content = content.replace(
        '<ul class="space-y-1 text-xs">',
        '<ul class="flex lg:flex-col overflow-x-auto gap-2 lg:gap-1 text-xs pb-1 lg:pb-0 scrollbar-none max-w-full">'
    )
    
    # Make li flex-shrink-0 for horizontal scrolling
    content = content.replace('<li>\n              <button', '<li class="flex-shrink-0">\n              <button')
    content = content.replace('<li>\r\n              <button', '<li class="flex-shrink-0">\r\n              <button')
    
    # Make buttons whitespace-nowrap on mobile
    content = content.replace(
        'class="cat-item active w-full text-left',
        'class="cat-item active whitespace-nowrap lg:whitespace-normal w-auto lg:w-full text-left'
    )
    content = content.replace(
        'class="cat-item w-full text-left',
        'class="cat-item whitespace-nowrap lg:whitespace-normal w-auto lg:w-full text-left'
    )
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated category sidebar responsiveness for {fname}")
