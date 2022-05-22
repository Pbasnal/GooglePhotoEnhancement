import sqlalchemy as db

from database.sql_engine import BASE


class SimilarImages(BASE):
    __tablename__ = 'similar_images'
    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    imageId = db.Column(db.String(50), nullable=False)
    similarImageId = db.Column(db.String(50), nullable=False)

    similarityScore = db.Column(db.Float(4), nullable=False)

    def toString(self):
        return f"\SimilarImages--" \
            + f"\n id: {self.id}" \
            + f"\n userId: {self.userId}" \
            + f"\n imageId: {self.imageId}" \
            + f"\n similarImageId: {self.similarImageId}" \
            + f"\n similarityScore: {self.similarityScore}"
