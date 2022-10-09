import enum


class ReplicationMethod(enum.Enum):
    CUSTOM_QUERY = 'CUSTOM_QUERY'
    FULL_TABLE = 'FULL_TABLE'
    INCREMENTAL = 'INCREMENTAL'
