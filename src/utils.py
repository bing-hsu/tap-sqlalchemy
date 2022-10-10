import logging.config
from pathlib import Path

import singer
from singer import CatalogEntry, metadata


# Project Structure
class ProjectStructure:
    PROJECT_DIR = Path(__file__).parent.parent
    CONF_DIR = PROJECT_DIR / 'conf'
    SQL_DIR = CONF_DIR / 'sql'

    @classmethod
    def print(cls):
        dir_list = [x for x in dir(cls) if not x.startswith('_') and isinstance(getattr(cls, x), Path)]
        print("# PROJECT STRUCTURE")
        print("#")
        for dir_str in dir_list:
            print(f"# {dir_str:13} = {getattr(cls, dir_str)}")
        print("#")


project_dir = ProjectStructure.PROJECT_DIR
conf_dir = ProjectStructure.CONF_DIR
sql_dir = ProjectStructure.SQL_DIR


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
