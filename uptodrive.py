from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def upload_file_to_drive(drive, file_path, title=None):
    """
    Uploads a file to Google Drive.

    Args:
    - drive: A GoogleDrive instance.
    - file_path: The local path of the file to be uploaded.
    - title: (Optional) The title to be used for the uploaded file on Google Drive.

    Returns:
    - The uploaded file's metadata if successful, None otherwise.
    """
    try:
        file_metadata = {'title': title if title else file_path.split('/')[-1]}
        file_to_upload = drive.CreateFile(file_metadata)
        file_to_upload.SetContentFile(file_path)
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
local_file_path = "modelcpp.ipynb"

# Example: Title to be used for the uploaded file on Google Drive (optional)
uploaded_file_title = "modelcpp.ipynb"

# Upload the file to Google Drive
uploaded_file = upload_file_to_drive(drive, local_file_path, title=uploaded_file_title)

if uploaded_file is None:
    print("File upload failed.")
