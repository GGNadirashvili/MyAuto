import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    # Set up Chrome driver - try without headless first
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Comment out for debugging
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def create_images_folder():
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

def download_image(url, filename):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def scrape_car_images():
    driver = setup_driver()
    create_images_folder()
    
    try:
        # Navigate to myauto.ge
        print("🚗 Loading myauto.ge...")
        driver.get("https://www.myauto.ge/ka/s/autos/")
        time.sleep(5)  # Initial wait
        
        # Accept cookies if the popup appears
        try:
            cookie_accept = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'დახურვა') or contains(text(), 'Close')]"))
            )
            cookie_accept.click()
            print("✅ Cookies accepted")
            time.sleep(2)
        except:
            print("ℹ️ No cookie popup found")
        
        # Scroll to load more content
        print("🔄 Scrolling to load images...")
        for _ in range(3):  # Scroll 3 times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Find all car image containers
        print("🔍 Finding car images...")
        image_containers = driver.find_elements(By.CSS_SELECTOR, "div.list-item__thumbnail__items")
        
        if not image_containers:
            print("⚠️ No image containers found. Taking screenshot for debugging...")
            driver.save_screenshot("debug_screenshot.png")
            print("📸 Saved screenshot as debug_screenshot.png")
        
        print(f"Found {len(image_containers)} car listings")
        
        image_count = 0
        for i, container in enumerate(image_containers):
            try:
                # Find all images within this container
                images = container.find_elements(By.TAG_NAME, "img")
                
                for j, img in enumerate(images):
                    img_url = img.get_attribute('src')
                    if not img_url:
                        img_url = img.get_attribute('data-src')
                    
                    if img_url and 'myauto/photos' in img_url:
                        # Clean URL
                        clean_url = img_url.split('?')[0]
                        file_ext = os.path.splitext(clean_url)[1] or '.jpg'
                        filename = f"images/car_{i+1}_{j+1}{file_ext}"
                        
                        if download_image(clean_url, filename):
                            image_count += 1
                            print(f"✅ Saved {filename}")
                        else:
                            print(f"⚠️ Failed to download image {i+1}_{j+1}")
            except Exception as e:
                print(f"⚠️ Error processing container {i+1}: {e}")
        
        print(f"\n🎉 Successfully saved {image_count} images")
                
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🚗 Step 1: Scraping car images...\n")
    scrape_car_images()
    print("\n✅ Done!")