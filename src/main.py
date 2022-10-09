import os
import sys
import traceback

import singer
import utils

from Database import Database
from utils import taplog
from tapstream import get_tap_stream

REQUIRED_CONFIG_KEYS = ['connection.conn_string', 'sync.include_streams']


def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    if args.discover:
        raise Exception("Discover mode is not supported")

    config = args.config
    state = args.state
    catalog = args.catalog

    # initialize db connection object
    con_str = config['connection.conn_string']
    database = Database(con_str)

    # read catalog document
    if catalog is None:
        raise Exception("Catalog document is not set")
        pass

    # for each included streams
    for stream_id in args.config['sync.include_streams']:
        catalog_entry = catalog.get_stream(stream_id)
        if catalog_entry is None:
            raise Exception(f"stream [{stream_id}] is included in Config document but not defined in Catalog document")

        tap_stream = get_tap_stream(catalog_entry, config, state, database, sql_dir=utils.sql_dir)
        tap_stream.sync()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        taplog.error(e)
        if os.environ.get('DEBUG', None):
            traceback.print_exception(e)
        sys.exit(1)
