from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_and_get_drive():
    """
    Authenticates with Google and returns a GoogleDrive instance.

    Returns:
    - A GoogleDrive instance if authentication is successful, None otherwise.
    """
    try:
        gauth = GoogleAuth()
        gauth.CommandLineAuth()  # Creates a link for authentication
        drive = GoogleDrive(gauth)
        print("Authentication successful.")
        return drive
    except Exception as e:
        print(f"Error authenticating: {e}")
        return None

def download_file_from_drive(drive, file_id, destination_path):
    """
    Downloads a file from Google Drive.

    Args:
    - drive: A GoogleDrive instance.
    - file_id: The ID of the file to be downloaded.
    - destination_path: The local path where the file will be downloaded to.

    Returns:
    - True if download is successful, False otherwise.
    """
    try:
        file_to_download = drive.CreateFile({'id': file_id})
        file_to_download.GetContentFile(destination_path)
        print(f"File downloaded successfully from Google Drive: {destination_path}")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

# Authenticate with Google
drive = authenticate_and_get_drive()

if drive:
    # Example: File ID of the file to be downloaded from Google Drive
    file_id_to_download = "1-0Cz3ctbeGBYxUub0Z1QmDmGE7HTfYDA"

    # Example: Local path where the file will be downloaded to
    downloaded_file_path = "filed.bin"

    # Download the file from Google Drive
    download_success = download_file_from_drive(drive, file_id_to_download, downloaded_file_path)

    if not download_success:
        print("File download failed.")
else:
    print("Authentication failed. Cannot download file.")
