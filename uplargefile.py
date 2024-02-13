from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import zipfile
import os

def zip_file(source_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(source_path, arcname=os.path.basename(source_path))

def upload_zipped_file_to_drive(drive, zipped_file_path, title=None, chunk_size=None):
    try:
        file_metadata = {'title': title if title else os.path.basename(zipped_file_path)}
        file_to_upload = drive.CreateFile(file_metadata)
        
        # Set content and chunk size before uploading
        file_to_upload.SetContentFile(zipped_file_path)
        
        if chunk_size:
            file_to_upload.Upload(param={'uploadType': 'resumable'})
            
            # Manually set the Content-Range header
            headers = {'Content-Range': 'bytes 0-' + str(chunk_size - 1) + '/' + str(os.path.getsize(zipped_file_path))}
            file_to_upload._BuildMultipleUploadParam({}, headers)
        else:
            file_to_upload.Upload()
        
        print(f"File uploaded successfully to Google Drive: {file_to_upload['title']}")
        return file_to_upload
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# Assuming gauth is your authenticated GoogleAuth instance
gauth = GoogleAuth()
gauth.CommandLineAuth()  # Creates a link for authentication
drive = GoogleDrive(gauth)

# Example: Local path of the file to be uploaded
original_file_path = "merged.bin"
zipped_file_path = "merged.zip"

# Zip the file
zip_file(original_file_path, zipped_file_path)

# Example: Title to be used for the uploaded file on Google Drive (optional)
uploaded_file_title = "config_merged.zip"

# Upload the zipped file to Google Drive with optional chunk size
# Example chunk size: 10 MB (10 * 1024 * 1024 bytes)
uploaded_file = upload_zipped_file_to_drive(drive, zipped_file_path, title=uploaded_file_title, chunk_size=10*1024*1024)

if uploaded_file is None:
    print("File upload failed.")
else:
    print("File uploaded successfully.")
