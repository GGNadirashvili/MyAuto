MyAuto Car Image Scraper

This project scrapes car listing preview images from the first page of myauto.ge using Selenium, and uploads them to an AWS S3 bucket.

Features:

  Headless Chrome scraping via Selenium

  Collects preview images and saves with car ID and image number

  Uploads images to a specified AWS S3 bucket

  Handles timeouts and prevents duplicate downloads

Requirements:

Python 3.8+

Google Chrome browser

ChromeDriver matching your Chrome version

Install dependencies:

pip install -r requirements.txt

Usage:

Configure AWS credentials
Ensure your environment is configured to access your AWS S3 bucket (e.g., via ~/.aws/credentials or environment variables).

Set your bucket name
In main.py, set your bucket name:

upload_directory("images", "myauto-car-images")

Run the scraper

python main.py

This will:

Launch the browser

Scrape car preview images

Save them in the images/ directory

Upload them to your S3 bucket

Output Structure:

images/ – contains files named like 114607383_1.jpg, where the number is the car ID.

Uploaded to s3://<your-bucket>/ with the same filenames.
