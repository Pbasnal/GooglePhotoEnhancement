import typing
from database.models.similar_images import SimilarImages
from database.models.photos import Photo
from database.sql_engine import SqlConnection
from database.sql_engine import SqlEngine

def getPhotosWhichDontHaveSimilarImages(batch_size, connection: SqlConnection) -> typing.List[Photo]:
    with SqlEngine(connection) as engine:
        photos = engine.select(Photo) \
            .filter(Photo.have_found_similar_images.is_(False)) \
            .limit(batch_size) \
            .all()

        for photo in photos:
            yield photo

def storeSimilarPhoto(photo, similarPhoto, connection: SqlConnection):
    with SqlEngine(connection) as engine:
        similarPhoto: SimilarImages
        engine.add(similarPhoto)


def getPhotosSimilarTo(photo: Photo, connection: SqlConnection) -> typing.List[Photo]:
    with SqlEngine(connection) as engine:
        photos = engine.select(Photo) \
            .filter(Photo.hash_chunk1.is_(photo.hash_chunk1),
                    Photo.hash_chunk2.is_(photo.hash_chunk2),
                    Photo.hash_chunk3.is_(photo.hash_chunk3)) \
            .all()

        for photo in photos:
            yield photo
        
        photos = engine.select(Photo) \
            .filter(Photo.hash_chunk2.is_(photo.hash_chunk2),
                    Photo.hash_chunk3.is_(photo.hash_chunk3),
                    Photo.hash_chunk4.is_(photo.hash_chunk4)) \
            .all()

        for photo in photos:
            yield photo

        photos = engine.select(Photo) \
            .filter(Photo.hash_chunk1.is_(photo.hash_chunk1),
                    Photo.hash_chunk2.is_(photo.hash_chunk2),
                    Photo.hash_chunk4.is_(photo.hash_chunk4)) \
            .all()

        for photo in photos:
            yield photo
        
        photos = engine.select(Photo) \
            .filter(Photo.hash_chunk1.is_(photo.hash_chunk1),
                    Photo.hash_chunk4.is_(photo.hash_chunk4),
                    Photo.hash_chunk3.is_(photo.hash_chunk3)) \
            .all()

        for photo in photos:
            yield photo

        photos = engine.select(Photo) \
            .filter(Photo.hash_chunk2.is_(photo.hash_chunk2),
                    Photo.hash_chunk4.is_(photo.hash_chunk4),
                    Photo.hash_chunk3.is_(photo.hash_chunk3)) \
            .all()

        for photo in photos:
            yield photo
