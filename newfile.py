import os
import sys
import time

# ==========================================
# PART 1: CLOUD INSTALLER (The Engine Room)
# ==========================================
def install_dependencies():
    print("⬇️ Downloading latest Google Chrome...")
    # 1. Download official Chrome to fix version crashes
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    
    # 2. Install Chrome
    print("🛠️ Installing Chrome...")
    os.system("apt-get update")
    os.system("apt-get install -y ./google-chrome-stable_current_amd64.deb")
    
    # 3. Install Python Selenium Tools
    print("🔌 Installing Selenium & Managers...")
    os.system("pip install selenium webdriver-manager")

# Check if we are running in Google Colab
try:
    import google.colab
    IN_COLAB = True
    install_dependencies()
except ImportError:
    IN_COLAB = False

# ==========================================
# PART 2: THE AROLINKS CRUSHER LOGIC
# ==========================================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def solve_link(target_url):
    print("\n🚀 Launching Headless Browser...")
    
    # Configure Chrome to run invisibly (Headless)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080') # Full screen size helps find buttons
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36') # Fake being a real PC
    
    # Setup Driver
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"🔗 Visiting Target: {target_url}")
        driver.get(target_url)
        
        # Arolinks usually has multiple steps, so we loop 4 times
        for step in range(1, 5):
            print(f"\n--- STEP {step} ---")
            
            # 1. WAIT: Give the timer time to finish (Arolinks is usually 10-15s)
            print("⏳ Waiting 15 seconds for timers/ads...")
            time.sleep(15)
            
            # 2. SCAN: Look for these specific buttons
            # These are the exact words Arolinks uses in order
            keywords = [
                "verify", 
                "next", 
                "continue", 
                "click here to continue", 
                "generate link", 
                "get link", 
                "go to link",
                "download"
            ]
            
            found_button = False
            
            # Search for buttons, links (a), and divs (sometimes buttons are fake divs)
            all_elements = driver.find_elements(By.TAG_NAME, "button") + \
                           driver.find_elements(By.TAG_NAME, "a") + \
                           driver.find_elements(By.TAG_NAME, "div")
            
            print(f"🔎 Scanning {len(all_elements)} elements...")

            for element in all_elements:
                try:
                    # Get text and clean it up
                    text = element.text.lower().strip()
                    
                    # Check if text matches keywords AND element is actually visible
                    if any(key in text for key in keywords) and element.is_displayed():
                        # Filter out huge paragraphs, we only want short button text
                        if len(text) < 30:
                            print(f"🎯 FOUND TARGET: '{element.text}'")
                            
                            # Scroll directly to it
                            driver.execute_script("arguments[0].scrollIntoView();", element)
                            time.sleep(1)
                            
                            # FORCE CLICK (JavaScript Click is stronger than normal click)
                            driver.execute_script("arguments[0].click();", element)
                            print("✅ CLICKED IT!")
                            
                            found_button = True
                            
                            # Wait a moment for page reload
                            time.sleep(5)
                            break 
                except:
                    continue # Skip elements that cause errors

            if not found_button:
                print("❌ No keywords found this step.")
            
            # Check if we have left the ad site (Success Check)
            current = driver.current_url
            if "arolinks" not in current and "google" not in current:
                print("🎉 URL Changed! We might be free.")
                # We don't break immediately just in case it's another redirect step

        # 3. FINAL REPORT
        print(f"\n🏁 Final Page URL: {driver.current_url}")
        print(f"📄 Final Page Title: {driver.title}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
    finally:
        driver.quit()

# ==========================================
# PART 3: YOUR LINK
# ==========================================
# Replace the URL inside the quotes with your Arolinks URL
solve_link("PASTE_YOUR_AROLINKS_URL_HERE")