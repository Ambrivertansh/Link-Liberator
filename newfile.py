import os
import sys
import time

# ==========================================
# PART 1: CLOUD INSTALLER (Stealth Edition)
# ==========================================
def install_dependencies():
    print("⬇️ Downloading latest Google Chrome...")
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    
    print("🛠️ Installing Chrome...")
    os.system("apt-get update")
    os.system("apt-get install -y ./google-chrome-stable_current_amd64.deb")
    
    print("🔌 Installing Selenium & Stealth...")
    os.system("pip install selenium webdriver-manager selenium-stealth")

# Check for Colab
try:
    import google.colab
    IN_COLAB = True
    install_dependencies()
except ImportError:
    IN_COLAB = False

# ==========================================
# PART 2: THE BOT LOGIC
# ==========================================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth 

def solve_link(target_url):
    print("\n🚀 Launching Stealth Browser...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # 🎭 Activate Stealth Mode (Bypasses Cloudflare)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        print(f"🔗 Visiting: {target_url}")
        driver.get(target_url)
        
        # Cloudflare Check
        print("🛡️ Checking for Cloudflare...")
        time.sleep(10)
        
        # Cloudflare Bypass Logic
        if "Attention Required" in driver.title or "Just a moment" in driver.title:
            print("⚠️ Cloudflare Detected! Attempting bypass...")
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for frame in iframes:
                try:
                    driver.switch_to.frame(frame)
                    checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
                    checkbox.click()
                    print("✅ Clicked Cloudflare Checkbox!")
                    driver.switch_to.default_content()
                    time.sleep(5)
                except:
                    driver.switch_to.default_content()

        # Arolinks Button Logic
        for step in range(1, 6):
            print(f"\n--- STEP {step} ---")
            print("⏳ Waiting 12 seconds for ads...")
            time.sleep(12)
            
            keywords = [
                "verify", "next", "continue", "click here to continue", 
                "generate link", "get link", "go to link", "download"
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
                            time.sleep(8) # Wait for reload
                            break 
                except:
                    continue

            if not found_button:
                print("❌ No keywords found this step.")
            
            # CHECK IF WE REACHED THE GOAL
            current = driver.current_url
            if "herokuapp" in current or "code=" in current:
                print("\n🎉 DESTINATION REACHED!")
                print(f"🏁 Full URL: {current}")
                
                # --- THIS EXTRACTS THE CODE FOR YOU ---
                if "code=" in current:
                    extracted_code = current.split("code=")[1]
                    print(f"\n💎 YOUR CODE IS: {extracted_code}")
                    print(f"   (You can copy this directly!)")
                break

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

# ==========================================
# PART 3: USER INPUT
# ==========================================
print("\n" + "="*40)
print("   🔗 LINK LIBERATOR (STEALTH MODE)")
print("="*40 + "\n")

# This box will appear in Colab for you to paste your link
user_link = input("👉 PASTE YOUR AROLINKS URL: ").strip()

if len(user_link) > 5:
    solve_link(user_link)
else:
    print("❌ Invalid link.")