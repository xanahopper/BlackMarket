from enum import Enum


class FileStatus(Enum):
    ready_to_upload = 0
    has_uploaded = 1
