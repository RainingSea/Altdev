import sys, os
import logging
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

# invoke example
# from utils.log import loggers
# log = loggers(path="store the log file location")
# lg.info("My dream come true")
# --------- example ----------
# lg = loggers(path="./log/finallog.log")
# lg.info("My dream come true")


# Define a custom timezone for Beijing(UTC+8 timezone)
# def beijing(sec, what):
#     beijing_time = datetime.now() + timedelta(hours=8)
#     return beijing_time.replace(microsecond=0).timetuple()


class Log(BaseModel):
    log_path: str = Field(...)

    @classmethod
    def validate_log_path(cls, v):
        # Validate that the parent directory exists
        parent_dir = os.path.dirname(v)
        if not os.path.exists(parent_dir):
            raise ValueError(f"Parent directory '{parent_dir}' does not exist.")
        return v

    def setup_logger(self):
        # Configure the logger
        # logging.Formatter.converter = beijing
        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format="%(asctime)s %(filename)s : %(levelname)s  %(message)s",
            datefmt="%Y-%m-%d %A %H:%M:%S",
            filemode="a",
        )
        return logging.getLogger()
