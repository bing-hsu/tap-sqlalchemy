#!/usr/bin/env bash

wd="$(pwd)/$(dirname $0)"
py_path="$wd/.."
db_file=$wd/resource/test_db.db
config_file=$wd/command_test_config.json
sql_file=$wd/command_test_stream_1.sql
catalog_file=$wd/command_test_catalog.json

function prepare_db() {
  rm -f $db_file

  # see this https://stackoverflow.com/questions/18660798/here-document-gives-unexpected-end-of-file-error
  # indentation causing parsing trouble if use <<EOF
  # use <<-EOF and indent with TAB
  # closing EOF must not indent
  # and has no other word on the same line, including trailing space
  cat <<-EOF | sqlite3 $db_file
  create table test_table
  (a int, b text)
EOF

  cat <<EOF | sqlite3 $db_file
insert into test_table
values (1, 'a'), (2, 'b'), (3, 'c')
EOF
}

function prepare_work_space() {
  # tap test_table
  # config
  cat <<EOF >$config_file
{
  "connection.conn_string": "sqlite:///$db_file",
  "sync.include_streams": [ "1" ]
}
EOF

  # sql file
  cat <<EOF >$sql_file
select * from test_table
EOF

  # catalog
  cat <<EOF >$catalog_file
{
  "streams": [
    {
      "tap_stream_id": "1",
      "stream": "stream 1",
      "schema": {},
      "metadata": [
        {
          "breadcrumb": [],
          "metadata": {
            "replication-method": "CUSTOM_QUERY",
            "replication-sql-file": "$sql_file"
          }
        }
      ]
    }
  ]
}
EOF

}

prepare_db && prepare_work_space

PYTHONPATH=$py_path TAP_SQLALCHEMY_HOME=$wd python -m yw_etl_tap_sqlalchemy.main \
  -c $config_file \
  --catalog $catalog_file

rm -f $config_file $sql_file $catalog_file $db_file
