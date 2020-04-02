import asyncio
import logging
import sys
from os import environ
from watcher import PlexSQLiteBackupHandler
from hachiko.hachiko import AIOWatchdog



def get_environ():
    plex_sql_path = environ.get("PLEX_DB_PATH")
    if plex_sql_path is None:
        plex_sql_path = "/config/Library/Application Support/Plex Media Server/Plug-in Support/Databases"
    db_backup_path = environ.get("DB_BACKUP_PATH")
    if db_backup_path is None:
        db_backup_path = "/db_backup"

    return plex_sql_path, db_backup_path


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    return root


async def start_watcher(watcher):
    watcher.start()


def start_watching(plex_sql_path, backup_path):
    logger = setup_logging()
    loop = asyncio.get_event_loop()
    logger.info("Using PLEX_DB_PATH %s", plex_sql_path)
    logger.info("Using DB_BACKUP_PATH %s", backup_path)
    handler = PlexSQLiteBackupHandler(plex_sql_path, backup_path)
    watcher = AIOWatchdog(plex_sql_path, event_handler=handler)
    try:
        logger.info("Starting Watcher")
        loop.create_task(start_watcher(watcher))
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Stopping Watcher")
        watcher.stop()
    finally:
        loop.close()


if __name__ == "__main__":
    plex_sql_path, db_backup_path = get_environ()
    start_watching(plex_sql_path, db_backup_path)
