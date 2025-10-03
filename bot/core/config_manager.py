from importlib import import_module
from ast import literal_eval


class Config:
    AS_DOCUMENT = False
    AUTHORIZED_CHATS = ""
    BASE_URL = ""
    BASE_URL_PORT = 80
    BOT_TOKEN = ""
    CMD_SUFFIX = ""
    DATABASE_URL = ""
    DEFAULT_UPLOAD = "rc"
    EQUAL_SPLITS = False
    EXCLUDED_EXTENSIONS = ""
    FFMPEG_CMDS = {}
    FILELION_API = ""
    GDRIVE_ID = ""
    INCOMPLETE_TASK_NOTIFIER = False
    INDEX_URL = ""
    IS_TEAM_DRIVE = False
    JD_EMAIL = ""
    JD_PASS = ""
    LEECH_DUMP_CHAT = ""
    LEECH_FILENAME_PREFIX = ""
    LEECH_SPLIT_SIZE = 2097152000
    MEDIA_GROUP = False
    HYBRID_LEECH = False
    HYDRA_IP = ""
    HYDRA_API_KEY = ""
    NAME_SUBSTITUTE = ""
    OWNER_ID = 0
    QUEUE_ALL = 0
    QUEUE_DOWNLOAD = 0
    QUEUE_UPLOAD = 0
    RCLONE_FLAGS = ""
    RCLONE_PATH = ""
    RCLONE_SERVE_URL = ""
    RCLONE_SERVE_USER = ""
    RCLONE_SERVE_PASS = ""
    RCLONE_SERVE_PORT = 8080
    RSS_CHAT = ""
    RSS_DELAY = 600
    RSS_SIZE_LIMIT = 0
    SEARCH_API_LINK = ""
    SEARCH_LIMIT = 0
    SEARCH_PLUGINS = []
    STATUS_LIMIT = 4
    STATUS_UPDATE_INTERVAL = 15
    STOP_DUPLICATE = False
    STREAMWISH_API = ""
    SUDO_USERS = ""
    TELEGRAM_API = 0
    TELEGRAM_HASH = ""
    TG_PROXY = {}
    THUMBNAIL_LAYOUT = ""
    TORRENT_TIMEOUT = 0
    UPLOAD_PATHS = {}
    UPSTREAM_REPO = ""
    UPSTREAM_BRANCH = "master"
    USENET_SERVERS = []
    USER_SESSION_STRING = ""
    USER_TRANSMISSION = False
    USE_SERVICE_ACCOUNTS = False
    WEB_PINCODE = False
    YT_DLP_OPTIONS = {}

    @classmethod
    def _convert(cls, key, value):
        expected_type = type(getattr(cls, key))
        if value is None:
            return None
        if isinstance(value, expected_type):
            return value

        if expected_type == bool:
            return str(value).strip().lower() in {"true", "1", "yes"}

        if expected_type in [list, dict]:
            if not isinstance(value, str):
                raise TypeError(
                    f"{key} should be {expected_type.__name__}, got {type(value).__name__}"
                )

            if not value:
                return expected_type()

            try:
                evaluated = literal_eval(value)
                if isinstance(evaluated, expected_type):
                    return evaluated
                else:
                    raise TypeError
            except (ValueError, SyntaxError, TypeError) as e:
                raise TypeError(
                    f"{key} should be {expected_type.__name__}, got invalid string: {value}"
                ) from e
        try:
            return expected_type(value)
        except (ValueError, TypeError) as exc:
            raise TypeError(
                f"Invalid type for {key}: expected {expected_type}, got {type(value)}"
            ) from exc

    @classmethod
    def get(cls, key):
        return getattr(cls, key) if hasattr(cls, key) else None

    @classmethod
    def set(cls, key, value):
        if hasattr(cls, key):
            value = cls._convert(key, value)
            setattr(cls, key, value)
        else:
            raise KeyError(f"{key} is not a valid configuration key.")

    @classmethod
    def get_all(cls):
        return {
            key: getattr(cls, key)
            for key in cls.__dict__.keys()
            if not key.startswith("__") and not callable(getattr(cls, key))
        }

    @classmethod
    def load(cls):
        settings = import_module("config")
        for attr in dir(settings):
            if (
                not attr.startswith("__")
                and not callable(getattr(settings, attr))
                and hasattr(cls, attr)
            ):
                value = getattr(settings, attr)
                if not value:
                    continue
                value = cls._convert(attr, value)
                if isinstance(value, str):
                    value = value.strip()
                if attr == "DEFAULT_UPLOAD" and value != "gd":
                    value = "rc"
                elif attr in [
                    "BASE_URL",
                    "RCLONE_SERVE_URL",
                    "INDEX_URL",
                    "SEARCH_API_LINK",
                ]:
                    if value:
                        value = value.strip("/")
                elif attr == "USENET_SERVERS":
                    try:
                        if not value[0].get("host"):
                            continue
                    except:
                        continue
                setattr(cls, attr, value)
        for key in ["BOT_TOKEN", "OWNER_ID", "TELEGRAM_API", "TELEGRAM_HASH"]:
            value = getattr(cls, key)
            if isinstance(value, str):
                value = value.strip()
            if not value:
                raise ValueError(f"{key} variable is missing!")

    @classmethod
    def load_dict(cls, config_dict):
        for key, value in config_dict.items():
            if hasattr(cls, key):
                value = cls._convert(key, value)
                if key == "DEFAULT_UPLOAD" and value != "gd":
                    value = "rc"
                elif key in [
                    "BASE_URL",
                    "RCLONE_SERVE_URL",
                    "INDEX_URL",
                    "SEARCH_API_LINK",
                ]:
                    if value:
                        value = value.strip("/")
                elif key == "USENET_SERVERS":
                    try:
                        if not value[0].get("host"):
                            value = []
                    except:
                        value = []
                setattr(cls, key, value)
        for key in ["BOT_TOKEN", "OWNER_ID", "TELEGRAM_API", "TELEGRAM_HASH"]:
            value = getattr(cls, key)
            if isinstance(value, str):
                value = value.strip()
            if not value:
                raise ValueError(f"{key} variable is missing!")
