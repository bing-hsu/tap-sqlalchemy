# tap-sqlalchemy

# Roadmap

### Supported RDBMS

- [x] SQLite, see [SQLite with SQLAlchemy](https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#connect-strings)
- [x] SQL Server, see [PyODBC with SQLAlchemy](https://docs.sqlalchemy.org/en/14/dialects/mssql.html#module-sqlalchemy.dialects.mssql.pyodbc)
- [x] Impala
  > Impala connection string is not natively supported by SQLAlchemy, but
  tap-sqlalchemy provides a familiar connection string format as that of SQLite or SQL Server, and the 
  connection capability is supported by [impyla](https://github.com/cloudera/impyla)
  > Example: 
  > Impala "connection.conn_string" format:
  > 
  > impala+pyodbc://[username][:][password][@]host:port[/default_db]?auth_mechanism=LDAP
  > 
  > - auth_mechanism is required, and supports only one value: LDAP
  > - <host> and <port> are required

# Guide

### Tap Installation & Quick Start

1. Create a python virtual environment
2. install tap-sqlalchemy, `pip install yw-etl-tap-sqlalchemy`
3. invoke tap

```shell
$ <venv-bin>/tap-sqlalchemy -c '<config-json>' --catalog '<catalog-json>'
```

### Tap Configuration

Tap Configuration is a JSON document containing entries that will impact the behaviors of data extraction work load.

```json5
{
  // mandatory
  "connection.conn_string": "<SQLAlchemy compatible connection string>",
  // mandatory
  "sync.include_streams": [ 
    "<tap_stream_id>", 
    /* refer to a stream described in Catalog*/ 
  ],
  // optional
  "sync.working_directory": "..."
}
```
* see SQLAlchemy: [Database URLs](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)
* see [Working Directory](https://github.com/YiwenData/tap-sqlalchemy/issues/2) 

### Tap Catalog

Tap Catalog is a JSON document of one object containing definitions of data stream. 

```json5
{
  "streams": [
    {
      // mandatory, unique identifier, used in [sync.include_streams] of Tap Configuration
      "tap_stream_id": "...",
      // mandatory, human-friendly identifier, possible to have duplicates inside on Catalog Document
      "stream": "...",
      // mandatory
      // JSON Schema Object describing the shape of this data stream,
      // used for data verification
      // 
      // Empty Object means that schema check will be skipped
      "schema": {},
      // mandatory
      // a list of metadata entries about the whole stream or about one field
      "metadata": [
        {
          // mandatory
          // breadcrumb points to a field to which this metadata entry applies.
          // an array of string, like '["a", "b", "c"]', that is evaluated against this stream's JSON Schema document
          // 
          // Empty List means this is the metadata about the whole stream
          "breadcrumb": [],
          // mandatory
          // specific meta data entry, key value pair
          "metadata": {
            // Two special Keys that are of special interests
            // for SQL-based replication
            "replication-method": "CUSTOM_QUERY", 
            // relative path is resolved against
            // <working-directory/sql
            // absolute path is treated as it is
            "replication-sql-file": "query.sql"
          }
        }
      ]
    }
  ]
}
```

* see [JSON Schema](http://json-schema.org/)
