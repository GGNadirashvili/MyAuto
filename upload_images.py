import boto3
from pathlib import Path

def upload_directory(directory_path, bucket_name):
    s3_client = boto3.client('s3')
    directory = Path(directory_path)

    print(f"📂 Uploading files from: {directory.resolve()} to S3 bucket: {bucket_name}")

    found_files = False
    for path in directory.rglob('*'):
        if path.is_file():
            found_files = True
            key = str(path.relative_to(directory))
            print(f"⏫ Uploading {key}...")
            s3_client.upload_file(
                Filename=str(path),
                Bucket=bucket_name,
                Key=key
            )
            print(f"✅ Uploaded to s3://{bucket_name}/{key}")

    if not found_files:
        print("⚠️ No files found to upload.")
