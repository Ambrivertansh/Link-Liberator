import os
import sys
import time

# --- PART 1: CLOUD SETUP (The Engine Room) ---
def install_dependencies():
    print("⬇️ Downloading latest Google Chrome...")
    # 1. Download official Chrome (to fix the 'SessionNotCreated' error)
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    
    # 2. Install Chrome
    print("🛠️ Installing Chrome...")
    os.system("apt-get update")
    os.system("apt-get install -y ./google-chrome-stable_current_amd64.deb")
    
    # 3. Install Python tools
    print("🔌 Installing Selenium & Managers...")
    os.system("pip install selenium webdriver-manager")

# Check if we are running in Google Colab
try:
    import google.colab
    IN_COLAB = True
    install_dependencies()
except ImportError:
    IN_COLAB = False

# --- PART 2: THE BOT LOGIC (The Brain) ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def solve_link(target_url):
    print("\n🚀 Launching Headless Browser...")
    
    # Configure Chrome to run without a screen (Headless)
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080') # Fake a full screen size
    
    # Auto-install the driver that matches the new Chrome
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"🔗 Visiting: {target_url}")
        driver.get(target_url)
        
        # 1. WAIT (Give the site time to load ads/timers)
        print("⏳ Waiting 8 seconds for page load...")
        time.sleep(8)
        
        # 2. SCAN FOR BUTTONS
        # Words we look for in buttons
        keywords = ["skip", "continue", "next", "get link", "download", "verify", "english"]
        
        found_button = False
        
        # Grab every button and link on the page
        all_elements = driver.find_elements(By.TAG_NAME, "button") + driver.find_elements(By.TAG_NAME, "a")
        print(f"🔎 Scanned {len(all_elements)} clickable items.")

        for element in all_elements:
            try:
                # Get the text on the button (convert to lowercase)
                text = element.text.lower().strip()
                
                # If the button text matches our keywords...
                if any(key in text for key in keywords) and len(text) < 20:
                    print(f"🎯 FOUND TARGET: '{element.text}'")
                    
                    # Scroll to it (crucial for mobile/hidden buttons)
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    time.sleep(1)
                    
                    # Click!
                    element.click()
                    print("✅ CLICKED IT!")
                    found_button = True
                    break # We clicked one, so stop searching
            except:
                continue # If a button causes an error, skip to the next one

        if not found_button:
            print("❌ No 'Skip' buttons found this time.")

        # 3. REPORT RESULT
        time.sleep(5) # Wait for redirect
        print(f"🏁 Final Page URL: {driver.current_url}")
        print(f"📄 Final Page Title: {driver.title}")

    except Exception as e:
        print(f"❌ Crash Error: {e}")
    finally:
        driver.quit()

# --- PART 3: TEST IT ---
# Try it on Wikipedia first because it has predictable buttons
solve_link("https://www.python.org/downloads/")