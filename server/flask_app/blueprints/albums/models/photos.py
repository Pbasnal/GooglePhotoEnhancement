import sqlalchemy as db
from flask_app.sqldb.appdb import db


class Photos(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    albumId = db.Column(db.String(50), nullable=False)
    baseUrl = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(50), nullable=False)

    hash_chunk1 = db.Column(db.String(20), nullable=False)
    hash_chunk2 = db.Column(db.String(20), nullable=False)
    hash_chunk3 = db.Column(db.String(20), nullable=False)
    hash_chunk4 = db.Column(db.String(20), nullable=False)
    hash_chunk5 = db.Column(db.String(20), nullable=False)
    hash_chunk6 = db.Column(db.String(20), nullable=False)
    hash_chunk7 = db.Column(db.String(20), nullable=False)
    hash_chunk8 = db.Column(db.String(20), nullable=False)

    have_found_similar_images = db.Column(db.Boolean(), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "userId": self.userId,
            "albumId": self.albumId,
            "baseUrl": self.baseUrl,
            "filename": self.filename,
            "hash_chunk1": self.hash_chunk1,
            "hash_chunk2": self.hash_chunk2,
            "hash_chunk3": self.hash_chunk3,
            "hash_chunk4": self.hash_chunk4,
            "hash_chunk5": self.hash_chunk5,
            "hash_chunk6": self.hash_chunk6,
            "hash_chunk7": self.hash_chunk7,
            "hash_chunk8": self.hash_chunk8,
            "have_found_similar_images": self.have_found_similar_images,
        }

    def getPhotosOfAlbum(albumId):
        return Photos.query.filter(Photos.albumId == albumId).all()

    def getPhotosWithIds(ids):
        return Photos.query\
            .filter(Photos.id.in_(ids)).all()
