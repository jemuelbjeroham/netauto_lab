import os
import boto3

BUCKET_NAME = "netautomation-logging-dev"
BASE_FOLDERS = ["./logs", "./backups", "./interfaces", "./user_logins"]

def upload_files():
    s3_client = boto3.client("s3")
    for folder in BASE_FOLDERS:
        if not os.path.exists(folder):
            continue
        for file_name in os.listdir(folder):
            local_path = os.path.join(folder, file_name)
            s3_key = f"{folder.strip('./')}/{file_name}"
            try:
                s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
                print(f"Uploaded {local_path} to s3://{BUCKET_NAME}/{s3_key}")
            except Exception as e:
                print(f"Error uploading {local_path} -> {e}")

if __name__ == "__main__":
    upload_files()
