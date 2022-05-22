import sqlalchemy as db

from database.sql_engine import BASE

class ProcessTracker(BASE):
    __tablename__ = 'process_tracker'
    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    albumId = db.Column(db.String(50), nullable=False)

    similarImagesStatus = db.Column(db.String(20), nullable=False)

    def toString(self):
        return f"\nProcessTracker--" \
            + f"\n id: {self.id}" \
            + f"\n userId: {self.userId}" \
            + f"\n albumId: {self.albumId}" \
            + f"\n similarImageStatus: {self.similarImagesStatus}"
