import json
from flask_app.sqldb.appdb import db

class ProcessTracker(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    albumId = db.Column(db.String(50), nullable=False)

    similarImagesStatus = db.Column(db.String(20), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "userId": self.userId,
            "albumId": self.albumId,
            "similarImagesStatus": self.similarImagesStatus
        }

    def createAlbumProcessObject(similarImageProcess):
        return ProcessTracker(
            userId=similarImageProcess["userId"],
            albumId=similarImageProcess["albumId"],
            similarImagesStatus = similarImageProcess["status"]
        )

    def getSimilarImageProcess(processId):
        getProcessQuery = ProcessTracker.query.filter(ProcessTracker.id == processId)

        if getProcessQuery.first() is None:
            return None

        return getProcessQuery.one()

    def getProcessesOfUser(userId):
        return ProcessTracker.query.filter(ProcessTracker.userId == userId).all()

    def getProcessesOfAlbum(albumId):
        return ProcessTracker.query.filter(ProcessTracker.albumId == albumId).all()
