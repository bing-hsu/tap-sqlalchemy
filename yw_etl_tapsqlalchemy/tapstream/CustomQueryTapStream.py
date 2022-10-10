from pathlib import Path

import singer
from singer import CatalogEntry

from yw_etl_tapsqlalchemy.Database import Database
from .helpers import get_stream_meta


class CustomQueryTapStream:
    def __init__(self, catalog_entry: CatalogEntry, config, state, db: Database, sql_dir: Path):
        self.db = db
        self.state = state
        self.config = config
        self.catalog_entry = catalog_entry

        self.stream_name = self.catalog_entry.stream

        query_file = self.stream_meta.get('replication-sql-file', None)
        if query_file is None:
            raise Exception(
                f"{self} : replication-sql-file is not set")
        self._query = (sql_dir / query_file).read_text(encoding='utf8')

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.catalog_entry.stream}, id={self.catalog_entry.tap_stream_id})"

    @property
    def stream_meta(self):
        return get_stream_meta(self.catalog_entry)

    def sync(self):
        singer.write_schema(self.catalog_entry.stream, self.catalog_entry.schema.to_dict(), [])
        with self.db as conn:
            cur = conn.execute(self._query)
            for row in cur:
                record = {k: row[k] for k in row.keys()}
                singer.write_record(self.stream_name, record)
