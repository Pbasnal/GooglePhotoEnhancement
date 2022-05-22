from googleapiclient.discovery import build
import google
import requests
from gphotospy.media import *

from loguru import logger

service_name = "photoslibrary"
version = "v1"
token_file = f'{service_name}_{version}.token'
scopes_arr = [
    'https://www.googleapis.com/auth/photoslibrary',
    'https://www.googleapis.com/auth/photoslibrary.sharing'
]


class GooglePhotoService:
    googleService = {}

    def fromCredentialDictionary(credentials):
        return google.oauth2.credentials.Credentials(
            credentials["token"],
            refresh_token=credentials["refresh_token"],
            token_uri=credentials["token_uri"],
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"])

    def getGoogleService(self, credentials):
        service_object = {
            "secrets": None
        }

        google_cred = GooglePhotoService.fromCredentialDictionary(credentials)

        service = build(service_name,
                        version,
                        static_discovery=False,
                        credentials=google_cred)

        logger.debug('service created successfully: {}'.format(service_name))

        service_object["service"] = service
        return service_object

    def getGoogleServiceForUser(self, userId):
        creds_dictionary = self.getTokenFromApi(userId)
        self.googleService = self.getGoogleService(creds_dictionary)

        return self

    def photosOfAlbum(self, albumId) -> MediaItem:
        media_manager = Media(self.googleService)
        photo_iterator = media_manager.search_album(albumId)
            
        for photo in photo_iterator:
            photoMedia = MediaItem(photo)
            if not photoMedia.is_photo():
                continue
            logger.debug("Raw photo from google")
            logger.debug(photo)
            yield photoMedia

    def getTokenFromApi(self, user_id):
        user_auth_response = requests.get(f'https://localhost:8080/user_auth/{user_id}',
                                          verify='../server.pem')

        if user_auth_response.status_code != 200:
            return dict()
        return self.credentialsToDict(user_auth_response.json())

    def credentialsToDict(self, credentials):
        scope_prefix = 'https://www.googleapis.com/auth/'
        scopes = [scope_prefix +
                  scope for scope in credentials['scopes'].split(',')]

        return {
            'token': credentials['token'],
            'refresh_token': credentials['refresh_token'],
            'token_uri': credentials['token_uri'],
            'client_id': credentials['client_id'],
            'client_secret': credentials['client_secret'],
            'scopes': scopes
        }
