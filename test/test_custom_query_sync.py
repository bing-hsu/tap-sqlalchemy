import contextlib
import json
import unittest
from pathlib import Path

from singer import Catalog
from sqlalchemy import create_engine

from tap_sqlalchemy.Database import Database
from tap_sqlalchemy.tapstream import get_tap_stream
from testutils import test_resource_dir, test_dir


class TestCustomQuerySync(unittest.TestCase):

    @staticmethod
    def prepare_db():
        db_path = Path(__file__).parent / 'test_db.db'
        db_path.unlink(missing_ok=True)
        db_path.touch(exist_ok=True)
        conn_str = f"sqlite:///{db_path}"

        engine = create_engine(conn_str)
        with engine.connect() as conn:
            # create table
            ddl = """
            create table test_table(
                a int,
                b text
            )
            """
            conn.execute(ddl)

            # populate data
            data = [(1, 'A'), (2, 'B'), (3, 'C')]
            temp_sql = "insert into test_table values(:a, :b)"
            for a, b in data:
                conn.execute(temp_sql, {"a": a, "b": b})

        return conn_str

    def test_sync(self):
        conn_str = self.prepare_db()
        sql_dir = test_resource_dir / 'sql'
        config = json.loads((test_resource_dir / 'config.json').read_text())
        state = json.loads((test_resource_dir / 'state.json').read_text())
        catalog = Catalog.load(test_resource_dir / 'catalog.json')

        # redirect stdout to file
        with (
            open(test_dir / 'actual_stdout.txt', 'w') as out,
            contextlib.redirect_stdout(out)
        ):
            for stream_id in config['sync.include_streams']:
                catalog_entry = catalog.get_stream(stream_id)
                database = Database(conn_str)
                tap_stream = get_tap_stream(catalog_entry, config, state, database, sql_dir=sql_dir)
                tap_stream.sync()

        exp = (test_dir / 'expect_stdout.txt').read_text()
        actual = (test_dir / 'actual_stdout.txt').read_text()
        self.assertEqual(exp, actual)
