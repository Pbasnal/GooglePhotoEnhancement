from flask_app.sqldb.appdb import db


class PhotoAlbum(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    productUrl = db.Column(db.String(200), nullable=False)
    mediaItemsCount = db.Column(db.Integer(), nullable=False)
    coverPhotoBaseUrl = db.Column(db.String(2000), nullable=False)
    coverPhotoMediaItemId = db.Column(db.String(200), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "userId": self.userId,
            "title": self.title,
            "productUrl": self.productUrl,
            "mediaItemsCount": self.mediaItemsCount,
            "coverPhotoBaseUrl": self.coverPhotoBaseUrl,
            "coverPhotoMediaItemId": self.coverPhotoMediaItemId
        }

    def createAlbumObject(userId, album):
        return PhotoAlbum(
            id=album["id"],
            userId=userId,
            title=album["title"],
            productUrl=album["productUrl"],
            mediaItemsCount=album["mediaItemsCount"],
            coverPhotoBaseUrl=album["coverPhotoBaseUrl"],
            coverPhotoMediaItemId=album["coverPhotoMediaItemId"]
        )

    def getAlbum(albumId):
        getAlbumQuery = PhotoAlbum.query.filter(PhotoAlbum.id == albumId)

        if getAlbumQuery.first() is None:
            return None

        return getAlbumQuery.one()

    def getAlbumsOfUser(userId):
        return PhotoAlbum.query.filter(PhotoAlbum.userId == userId).all()

    def getAlbumsWithTitle(userId, albumTitle):
        return PhotoAlbum.query.filter(PhotoAlbum.userId == userId,
                                       PhotoAlbum.title.ilike(albumTitle)).all()
