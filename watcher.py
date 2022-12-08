import boto3
import os
from time import sleep

# Create an S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])

bucket_name = os.environ["AWS_S3_BUCKET"]
folder_path = os.environ["AWS_RECORDING_DIR"]

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# The prefix to use for the keys of the uploaded files
key_prefix = 'folder/'

while True:
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Upload any new files to S3
    for file in files:
        file_path = os.path.join(folder_path, file)

        # Check if the file is a regular file (not a directory or symlink, etc.)
        if os.path.isfile(file_path):
            # Upload the file to S3
            with open(file_path, 'rb') as data:
                s3.upload_fileobj(data, bucket_name, file)

            # Delete the file from the local filesystem
            os.remove(file_path)

    # Sleep for 1 second before checking for new files again
    sleep(1)
