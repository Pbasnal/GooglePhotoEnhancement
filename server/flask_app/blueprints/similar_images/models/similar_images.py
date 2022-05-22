from flask_app.sqldb.appdb import db


class SimilarImages(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    imageId = db.Column(db.String(50), nullable=False)
    similarImageId = db.Column(db.String(50), nullable=False)

    similarityScore = db.Column(db.Float(4), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "userId": self.userId,
            "imageId": self.imageId,
            "similarImageId": self.similarImageId,
            "similarityScore": self.similarityScore
        }

    def createSimilarImages(similarImages):
        return SimilarImages(
            imageId=similarImages["imageId"],
            userId=similarImages["userId"],
            similarImageId=similarImages["similarImageId"],
            similarImagesStatus=similarImages["similarityScore"]
        )

    def getImagesSimilarTo(imageId):
        return SimilarImages.query.filter((SimilarImages.imageId == imageId) | (SimilarImages.similarImageId == imageId)).all()

    def getImagesSimilarForUser(userId, page, perPage=10):
        return SimilarImages.query \
            .filter(SimilarImages.userId == userId) \
            .paginate(page, perPage, error_out=False) \
            .items
