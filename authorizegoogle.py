from gphotospy import authorize

DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"
PROCESSED_FOLDER = "DPED/dped/iphone/test_data"
CLIENT_SECRET_FILE = "google_secret_desktop.json"

def getAuthorizedService():    
    return authorize.init(CLIENT_SECRET_FILE)
