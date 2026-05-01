import os

template_dir = r"c:\Users\acer\Downloads\evslot_dj_pro-20260405T064951Z-3-001\evslot_dj_pro\templates"

old_script = """window.addEventListener('load', function() {
    setTimeout(function() {
        var s = document.getElementById('ev-splash');
        if(s) { s.style.opacity = '0'; setTimeout(()=>s.style.display='none', 400); }
    }, 200); // Super fast 0.2s delay for premium feel
});"""

new_script = """// Run immediately instead of waiting for window.load which gets blocked by heavy iframes
setTimeout(function() {
    var s = document.getElementById('ev-splash');
    if(s) { s.style.opacity = '0'; setTimeout(()=>s.style.display='none', 400); }
}, 600);"""

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if old_script in content:
            content = content.replace(old_script, new_script)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed {filename}")

print("Done fixing splash scripts.")
