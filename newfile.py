import os
import sys
import time

# ==========================================
# PART 1: CLOUD INSTALLER
# ==========================================
def install_dependencies():
    print("⬇️ Downloading latest Google Chrome...")
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    
    print("🛠️ Installing Chrome...")
    os.system("apt-get update")
    os.system("apt-get install -y ./google-chrome-stable_current_amd64.deb")
    
    print("🔌 Installing Selenium & Managers...")
    os.system("pip install selenium webdriver-manager")

# Check for Colab
try:
    import google.colab
    IN_COLAB = True
    install_dependencies()
except ImportError:
    IN_COLAB = False

# ==========================================
# PART 2: THE LOGIC
# ==========================================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def solve_link(target_url):
    print("\n🚀 Launching Headless Browser...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"🔗 Visiting: {target_url}")
        driver.get(target_url)
        
        # Loop for multiple steps (Verify -> Next -> Get Link)
        for step in range(1, 5):
            print(f"\n--- STEP {step} ---")
            
            # 1. WAIT
            print("⏳ Waiting 15 seconds for timers...")
            time.sleep(15)
            
            # 2. SCAN
            keywords = [
                "verify", "next", "continue", "click here to continue", 
                "generate link", "get link", "go to link", "download", "i am not a robot"
            ]
            
            found_button = False
            all_elements = driver.find_elements(By.TAG_NAME, "button") + \
                           driver.find_elements(By.TAG_NAME, "a") + \
                           driver.find_elements(By.TAG_NAME, "div")
            
            print(f"🔎 Scanning {len(all_elements)} elements...")

            for element in all_elements:
                try:
                    text = element.text.lower().strip()
                    if any(key in text for key in keywords) and element.is_displayed():
                        if len(text) < 30:
                            print(f"🎯 FOUND TARGET: '{element.text}'")
                            driver.execute_script("arguments[0].scrollIntoView();", element)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", element)
                            print("✅ CLICKED IT!")
                            found_button = True
                            time.sleep(5)
                            break 
                except:
                    continue

            if not found_button:
                print("❌ No keywords found this step.")
            
            # Check if finished
            current = driver.current_url
            if "google" in current or "mediafire" in current or "drive" in current:
                print("🎉 Destination Reached!")
                break

        print(f"\n🏁 Final Page URL: {driver.current_url}")
        print(f"📄 Final Page Title: {driver.title}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

# ==========================================
# PART 3: USER INPUT (The Change)
# ==========================================
print("\n" + "="*40)
print("   🔗 LINK LIBERATOR - READY")
print("="*40 + "\n")

# This line will create a text box in Google Colab
user_link = input("👉 PASTE YOUR LINK HERE AND PRESS ENTER: ").strip()

if len(user_link) > 5:
    solve_link(user_link)
else:
    print("❌ Invalid link. Please try again.")