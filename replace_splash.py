import os
import re

template_dir = r"c:\Users\acer\Downloads\evslot_dj_pro-20260405T064951Z-3-001\evslot_dj_pro\templates"

# The exact old splash screen HTML (using regex to catch minor variations)
old_splash_regex = re.compile(
    r"<div id='ev-splash'.*?</script>", 
    re.DOTALL
)

# Also catch the one in maps.html which is split
old_splash_split_regex = re.compile(
    r"<div id=\"ev-splash\">.*?</div>.*?</div>.*?</div>",
    re.DOTALL
)
maps_script_regex = re.compile(
    r"<script>\s*setTimeout\(\(\) => \{ document\.getElementById\('ev-splash'\)\.classList\.add\('hide'\); \}, 1800\);\s*</script>",
    re.DOTALL
)

new_splash = """
<div id='ev-splash' style='position:fixed;top:0;left:0;width:100%;height:100%;background:#0f172a;z-index:99999;display:flex;align-items:center;justify-content:center;transition:opacity 0.4s ease, visibility 0.4s ease;'>
    <div style='position:relative; width:80px; height:80px;'>
        <div style='position:absolute; top:0; left:0; width:100%; height:100%; border-radius:50%; border:3px solid transparent; border-top-color:#38bdf8; border-right-color:#818cf8; animation: ev-spin 0.8s linear infinite;'></div>
        <div style='position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); font-size:24px;'>⚡</div>
    </div>
</div>
<style>
@keyframes ev-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
<script>
window.addEventListener('load', function() {
    setTimeout(function() {
        var s = document.getElementById('ev-splash');
        if(s) { s.style.opacity = '0'; setTimeout(()=>s.style.display='none', 400); }
    }, 200); // Super fast 0.2s delay for premium feel
});
</script>
"""

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the single line blocks
        new_content, count = old_splash_regex.subn(new_splash, content)
        
        # Replace the multi-line blocks (like maps.html, login.html)
        if "id=\"ev-splash\"" in new_content:
            new_content = old_splash_split_regex.sub(new_splash, new_content)
            new_content = maps_script_regex.sub("", new_content)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")

print("Done replacing splash screens.")
