import os
import shutil

DIST_DIR = "frontend_dist"
STATIC_DIR = "app/static"

def prepare_netlify():
    # 1. Create Dist Dir
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)
    
    # 2. Copy/Modify index.html
    with open(f"{STATIC_DIR}/index.html", "r") as f:
        html = f.read()
    
    # Fix paths for root deployment
    html = html.replace('/static/style.css', 'style.css')
    html = html.replace('/static/app.js', 'app.js')
    
    with open(f"{DIST_DIR}/index.html", "w") as f:
        f.write(html)
        
    # 3. Copy/Modify style.css
    shutil.copy(f"{STATIC_DIR}/style.css", f"{DIST_DIR}/style.css")
    
    # 4. Copy/Modify app.js
    with open(f"{STATIC_DIR}/app.js", "r") as f:
        js = f.read()
    
    # Prepend Backend Configuration
    config_header = """
const API_BASE_URL = "http://localhost:8000"; // TODO: UPDATE THIS TO YOUR PRODUCTION BACKEND URL
"""
    # Replace relative API calls with absolute
    js = js.replace("fetch('/api/v1", "fetch(API_BASE_URL + '/api/v1")
    js = js.replace("window.open('/api/v1", "window.open(API_BASE_URL + '/api/v1")
    
    final_js = config_header + js
    
    with open(f"{DIST_DIR}/app.js", "w") as f:
        f.write(final_js)
        
    print(f"✅ Netlify build complete! Folder: {os.path.abspath(DIST_DIR)}")
    print("👉 Drag and drop this folder to https://app.netlify.com/drop")

if __name__ == "__main__":
    prepare_netlify()
