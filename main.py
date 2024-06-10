import os
import psutil
import pwd
import grp
import stat
import time
from datetime import datetime
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Config import (
    PATHS,
    FILE_FILTERS,
    EXCLUDE_DIRS,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_LEVEL,
    EVENT_TYPE,
    FILE_PATH,
    EVENT_TIMESTAMP,
    FILE_SIZE,
    FILE_PERMISSIONS,
    FILE_OWNER,
    FILE_GROUP,
    FILE_MTIME,
    FILE_EXTENSION,
    PROCESS_ID,
    PROCESS_NAME,
    PROCESS_USER,
    PROCESS_CMDLINE,
    PROCESS_CWD,
)


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_any_event(self, event):
        if not event.is_directory and event.event_type != "opened":
            self.callback(event)


class FileMonitor:
    def __init__(self, paths, callback, file_filters, exclude_dirs):
        self.observer = Observer()
        self.paths = paths
        self.callback = callback
        self.file_filters = file_filters
        self.exclude_dirs = exclude_dirs

    def should_monitor(self, event):
        event_path = event.src_path
        if any(
            os.path.commonpath([event_path, exclude_dir]) == exclude_dir
            for exclude_dir in self.exclude_dirs
        ):
            return False
        return any(event_path.endswith(ext) for ext in self.file_filters)

    def start(self):
        event_handler = FileEventHandler(self.handle_event)
        for path in self.paths:
            self._schedule_path(event_handler, path)
        self.observer.start()

    def _schedule_path(self, event_handler, path):
        if os.path.exists(path):
            self.observer.schedule(event_handler, path, recursive=True)
        else:
            logging.warning(f"Path does not exist: {path}")

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def handle_event(self, event):
        if self.should_monitor(event):
            self.callback(event)


class FileMetadataExtractor:
    @staticmethod
    def extract_metadata(file_path):
        try:
            file_stat = os.stat(file_path)
            return {
                FILE_SIZE: file_stat.st_size,
                FILE_PERMISSIONS: stat.filemode(file_stat.st_mode),
                FILE_OWNER: pwd.getpwuid(file_stat.st_uid).pw_name,
                FILE_GROUP: grp.getgrgid(file_stat.st_gid).gr_name,
                FILE_MTIME: time.ctime(file_stat.st_mtime),
                FILE_EXTENSION: os.path.splitext(file_path)[1].lower(),
            }
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return {}


class ProcessInfoExtractor:
    @staticmethod
    def extract_process_info(file_path):
        try:
            for proc in psutil.process_iter(
                ["pid", "name", "username", "cmdline", "cwd"]
            ):
                if any(file_path == file.path for file in proc.open_files()):
                    return {
                        PROCESS_ID: proc.pid,
                        PROCESS_NAME: proc.name(),
                        PROCESS_USER: proc.username(),
                        PROCESS_CMDLINE: " ".join(proc.cmdline()),
                        PROCESS_CWD: proc.cwd(),
                    }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            logging.exception(f"Failed to get process info for file: {file_path}")
        return None


class EventLogger:
    @staticmethod
    def log_event(event, file_metadata, process_info):
        event_log = {
            EVENT_TYPE: event.event_type,
            FILE_PATH: event.src_path,
            EVENT_TIMESTAMP: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **file_metadata,
            "process_info": process_info or "Process info not available",
        }
        logging.info(f"Event: {event_log}")


class App:
    def __init__(self):
        self.monitor = None

    def start_monitoring(self):
        self.monitor = FileMonitor(PATHS, self.handle_event, FILE_FILTERS, EXCLUDE_DIRS)
        self.monitor.start()
        logging.info("File monitoring started.")

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop()
        logging.info("File monitoring stopped.")

    def handle_event(self, event):
        file_metadata = FileMetadataExtractor.extract_metadata(event.src_path)
        process_info = ProcessInfoExtractor.extract_process_info(event.src_path)
        EventLogger.log_event(event, file_metadata, process_info)

    def run(self):
        logging.basicConfig(
            level=LOG_LEVEL,
            format=LOG_FORMAT,
            datefmt=LOG_DATE_FORMAT,
        )
        self.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()


if __name__ == "__main__":
    app = App()
    app.run()
