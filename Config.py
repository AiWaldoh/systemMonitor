import os


# Static variables
PATHS = [
    "/etc/",
    "/var/log/",
    os.path.expanduser("~/.config"),
    "/var/spool/cron/",
    "/tmp/",
    "/var/tmp/",
]

FILE_FILTERS = [
    ".conf",
    ".log",
    ".ini",
    ".yml",
    ".yaml",
]

EXCLUDE_DIRS = [
    os.path.expanduser("~/.config/Code"),
]

LOG_FORMAT = "%(asctime)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Database configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "file_events")
DB_USER = os.environ.get("DB_USER", "username")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

# Event details
EVENT_TYPE = "event_type"
FILE_PATH = "file_path"
EVENT_TIMESTAMP = "event_timestamp"

# File metadata
FILE_SIZE = "file_size"
FILE_PERMISSIONS = "file_permissions"
FILE_OWNER = "file_owner"
FILE_GROUP = "file_group"
FILE_MTIME = "file_mtime"
FILE_EXTENSION = "file_extension"

# Process information
PROCESS_ID = "process_id"
PROCESS_NAME = "process_name"
PROCESS_USER = "process_user"
PROCESS_CMDLINE = "process_cmdline"
PROCESS_CWD = "process_cwd"
# Static variables
PATHS = [
    "/etc/",
    "/var/log/",
    os.path.expanduser("~/.config"),
    "/var/spool/cron/",
    "/tmp/",
    "/var/tmp/",
]

FILE_FILTERS = [
    ".conf",
    ".log",
    ".ini",
    ".yml",
    ".yaml",
]

EXCLUDE_DIRS = [
    os.path.expanduser("~/.config/Code"),
]

LOG_FORMAT = "%(asctime)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Database configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "file_events")
DB_USER = os.environ.get("DB_USER", "username")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
