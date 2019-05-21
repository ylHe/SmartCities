from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import csv

uploaded_file_names_dict = {}

def download_csv_content():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        #LocalWebserverAuth will fire up your browser and navigate to a google login page,
        #choose the account you want to access in your program, authorize the app,
        #and you will be sent to a page saying that
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    #The last line creates a Google Drive object to handle creating files
    #and uploading them to drive, we need to pass the g_login object
    #to the constructor to check if authentication was successful.
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for drive_file in file_list:
        uploaded_file_names_dict[drive_file['title']] = drive_file['id']

    file_to_download = 'traffic_data.csv'
    if file_to_download in uploaded_file_names_dict:
        #open google drive file with existing file's id
        g_drive_file = drive.CreateFile({'id': uploaded_file_names_dict[file_to_download]})
        #g_drive_file.GetContentFile(file_to_download) # Download file as with same title.
        csv_content = g_drive_file.GetContentString()

    return csv_content
