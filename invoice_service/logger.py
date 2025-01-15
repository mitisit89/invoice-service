import os
import logging

log_level = os.getenv("LOGLEVEL", "INFO").upper()
numeric_log_level = logging.getLevelName(log_level)
if not isinstance(numeric_log_level, int):
    numeric_log_level = logging.INFO

log_format = os.getenv("LOGFORMAT", "[%(asctime)s] %(levelname)s | %(name)s | %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(numeric_log_level)
console_handler.setFormatter(logging.Formatter(log_format))


class ExcludeSQLAlchemyFilter(logging.Filter):
    def filter(self, record):
        return not record.name.startswith("sqlalchemy")


console_handler.addFilter(ExcludeSQLAlchemyFilter())

logging.getLogger().addHandler(console_handler)

logging.getLogger().setLevel(numeric_log_level)
