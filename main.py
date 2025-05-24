from myauto_downloader import scrape_car_images
from upload_images import upload_directory
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🚗 Step 1: Scraping car images...")
    scrape_car_images() 

    print("\n☁️ Step 2: Uploading to S3...")
    upload_directory("images", "myauto-car-images1")

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
