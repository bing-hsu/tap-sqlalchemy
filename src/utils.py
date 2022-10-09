import logging.config
from pathlib import Path

import singer
from singer import CatalogEntry, metadata

# Project Structure
project_dir = Path(__file__).parent.parent
conf_dir = project_dir / 'conf'
sql_dir = conf_dir / 'sql'


# Utility Routines
def get_stream_meta(catalog_entry: CatalogEntry):
    compiled = singer.metadata.to_map(catalog_entry.metadata)
    return compiled.get((), None)


# Logger
def _get_logger():
    logging_conf_file = project_dir / 'conf' / 'logging.conf'
    logging.config.fileConfig(logging_conf_file)
    return logging.getLogger()


taplog = _get_logger()
