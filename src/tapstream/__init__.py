from pathlib import Path

from singer import CatalogEntry

from Database import Database
from utils import get_stream_meta
from .CustomQueryTapStream import CustomQueryTapStream
from .ReplicationMethod import ReplicationMethod


def get_tap_stream(catalog_entry: CatalogEntry, config, state, db: Database, sql_dir: Path):
    stream_meta = get_stream_meta(catalog_entry)
    match stream_meta.get('replication-method'):
        case ReplicationMethod.CUSTOM_QUERY.name:
            return CustomQueryTapStream(catalog_entry, config, state, db, sql_dir)
        case ReplicationMethod.FULL_TABLE.name | ReplicationMethod.INCREMENTAL.name as x:
            raise Exception(f"replication-method [{x}] not implemented")
        case _ as x:
            raise Exception(f"unknown replication-method [{x}]")
