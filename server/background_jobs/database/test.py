from database.sql_engine import SqlEngine
from database.models.process_tracker import ProcessTracker

if __name__ == "__main__":
    with SqlEngine('sqlite:////tmp/test.db') as engine:
        processes = engine.select(ProcessTracker) \
            .filter(ProcessTracker.similarImagesStatus.is_('NotStarted')) \
            .limit(3) \
            .all()

        for pro in processes:
            print(pro.toString())
            print()
