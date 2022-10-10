import logging.config
import os
from pathlib import Path

_pwd = Path(os.getcwd())


class WorkingDirectory:

    @staticmethod
    def get_sql_dir() -> Path:
        return WorkingDirectory.get_directory() / 'sql'

    @staticmethod
    def get_directory() -> Path:
        """
        Working Directory of this tap
        1. current directory
        2. env "TAP_SQLALCHEMY_HOME"
        3. "$HOME/.tap-sqlalchemy"
        """
        ok, p = WorkingDirectory._check_pwd()
        if ok:
            return p

        ok, p = WorkingDirectory._check_env()
        if ok:
            return p

        return WorkingDirectory._check_home_dir()

    @staticmethod
    def _check_home_dir() -> Path:
        p = Path(os.path.expanduser("~")) / '.tap-sqlalchemy'
        if p.is_file():
            raise Exception(f"{p} already exists and is a file")
        p.mkdir(exist_ok=True)
        return p

    @staticmethod
    def _check_env() -> (bool, Path):
        v = os.environ.get("TAP_SQLALCHEMY_HOME", None)
        return (v is not None and Path(v).is_dir()), Path(v)

    @staticmethod
    def _check_pwd() -> (bool, Path):
        return WorkingDirectory._has_sql_dir(_pwd), _pwd

    @staticmethod
    def _has_sql_dir(wd: Path) -> bool:
        return (wd / 'sql').is_dir()


# Logger
def _get_logger():
    logging_conf_file = Path(__file__).parent / 'logging.conf'
    logging.config.fileConfig(logging_conf_file)
    return logging.getLogger()


taplog = _get_logger()
