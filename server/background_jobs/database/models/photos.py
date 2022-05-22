import sqlalchemy as db

from database.sql_engine import BASE


class Photo(BASE):
    __tablename__ = 'photos'
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

    def toString(self):
        return f"\n Photo" \
            + f"\n id: {self.id}" \
            + f"\n userId: {self.userId} " \
            + f"\n filename: {self.filename}"\
            + f"\n hash_chunk: {self.hash_chunk1}|{self.hash_chunk2}|{self.hash_chunk3}|{self.hash_chunk4}|{self.hash_chunk5}|{self.hash_chunk6}|{self.hash_chunk7}|{self.hash_chunk8}"

    def toString2(self):
        return f"\n Photo" \
            + f"\n id: {self.id}" \
            + f"\n userId: {self.userId} " \
            + f"\n albumId: {self.albumId}" \
            + f"\n baseUrl: {self.baseUrl}"\
            + f"\n filename: {self.filename}"\
            + f"\n hash_chunks: {self.hash_chunk1}|{self.hash_chunk2}|{self.hash_chunk3}|{self.hash_chunk4}|{self.hash_chunk5}|{self.hash_chunk6}|{self.hash_chunk7}|{self.hash_chunk8}"
