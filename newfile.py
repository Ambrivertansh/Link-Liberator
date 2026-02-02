import os
import sys

def install_dependencies():
    print("⬇️ Downloading latest Google Chrome...")
    # 1. Download the official .deb file for Chrome
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    
    # 2. Install it (and fix any missing tools automatically)
    print("🛠️ Installing Chrome...")
    os.system("apt-get update")
    os.system("apt-get install -y ./google-chrome-stable_current_amd64.deb")
    
    # 3. Install the Selenium Driver Manager (The "Matchmaker")
    print("🔌 Installing Selenium Driver Manager...")
    os.system("pip install selenium webdriver-manager")

# Check if we are in Colab
try:
    import google.colab
    IN_COLAB = True
    install_dependencies()
except ImportError:
    IN_COLAB = False

# --- THE ACTUAL BOT ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def solve_link(target_url):
    print("\n🚀 Launching Headless Browser...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # This automatically finds the correct driver for the Chrome we just installed
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"🔗 Visiting: {target_url}")
        driver.get(target_url)
        
        # Verify it works
        print(f"✅ Success! Page Title: {driver.title}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

# Test it
solve_link("https://www.google.com")