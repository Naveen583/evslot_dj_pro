import os

base_dir = r"c:\Users\acer\Downloads\evslot_dj_pro-20260405T064951Z-3-001\evslot_dj_pro\templates"

with open(os.path.join(base_dir, "userhome.html"), "r", encoding="utf-8") as f:
    lines = f.readlines()

# The header ends right after the nav tag (around line 72)
header = "".join(lines[:72])
# The footer starts around line 171
footer = "".join(lines[171:])

def fix_template(filename):
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "{% block content %}" in content:
        inner = content.split("{% block content %}")[1].split("{% endblock %}")[0]
        
        # Wrap inner with a dark background section to match the premium theme
        wrapper = f"""
<section style="background-color: #0f172a; min-height: 100vh; padding: 50px 0;">
    {inner}
</section>
"""
        new_content = header + wrapper + footer
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {filename}")

fix_template("ai_trip_planner.html")
fix_template("upgrade_prime.html")
