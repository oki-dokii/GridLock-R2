import glob

# Files to process
html_files = glob.glob('*.html')

nav_link = """      <a href="methodology_and_assumptions.html" class="flex items-center gap-1.5 px-2 py-1.5 rounded bg-slate-800 border border-slate-700 text-[10px] font-medium text-slate-300 hover:text-white shrink-0">
        <i class="fa-solid fa-scale-balanced text-[11px] opacity-80"></i>
        <span>Methodology</span>
      </a>"""

for file in html_files:
    if file == 'methodology_and_assumptions.html' or file == 'math_foundation.html':
        continue
    
    with open(file, 'r') as f:
        content = f.read()
    
    # We will search for the monthly_report.html link block
    target = 'href="monthly_report.html"'
    if target in content:
        # Find the end of that anchor tag
        start_idx = content.find(target)
        end_idx = content.find('</a>', start_idx) + 4
        
        # Insert the new link right after it with a newline
        new_content = content[:end_idx] + '\n' + nav_link + content[end_idx:]
        
        with open(file, 'w') as f:
            f.write(new_content)
        print(f"Updated nav in {file}")

