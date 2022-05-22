import typing
from database.sql_engine import SqlConnection
from database.sql_engine import SqlEngine
from database.models.process_tracker import ProcessTracker

def getNotStartedAlbums(batch_size, connection: SqlConnection) -> typing.List[ProcessTracker]:
    with SqlEngine(connection) as engine:
        processes = engine.select(ProcessTracker) \
            .filter(ProcessTracker.similarImagesStatus.is_('NotStarted')) \
            .limit(batch_size) \
            .all()

        yield processes


def markProcessAsCompleteForAlbum(albumId, connection: SqlConnection) -> ProcessTracker:
    processes: ProcessTracker
    with SqlEngine(connection) as engine:
        processes = engine.select(ProcessTracker) \
            .filter(ProcessTracker.albumId.is_(albumId)) \
            .first()

        if processes != None :
            processes.similarImagesStatus = "AllImagesLoaded"

        return processes

