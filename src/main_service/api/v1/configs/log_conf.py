import logging
import os
from logging.handlers import RotatingFileHandler
name_dir = "src/main_service/main_logs"
os.makedirs(name_dir, exist_ok=True)

# Общий формат логов
formatter = logging.Formatter("%(asctime)s "
                              "[%(levelname)s] "
                              "%(name)s:"
                              " %(message)s")

# 🔸 Handler для business логики
business_handler = RotatingFileHandler(f"{name_dir}/business.log",
                                       maxBytes=5_000_000,
                                       backupCount=3)
business_handler.setLevel(logging.INFO)
business_handler.setFormatter(formatter)

# 🔸 Handler для ошибок
errors_handler = RotatingFileHandler(f"{name_dir}/errors.log",
                                     maxBytes=5_000_000,
                                     backupCount=3)
errors_handler.setLevel(logging.ERROR)
errors_handler.setFormatter(formatter)

# Root обработчик
root_handler = RotatingFileHandler(f"{name_dir}/common.log",
                                   maxBytes=5_000_000,
                                   backupCount=3)
root_handler.setLevel(logging.DEBUG)
root_handler.setFormatter(formatter)

# Логгер бизнес-логики
business_logger = logging.getLogger("business")
business_logger.setLevel(logging.DEBUG)
business_logger.addHandler(business_handler)

# Логгер ошибок
errors_logger = logging.getLogger("errors")
errors_logger.setLevel(logging.ERROR)
errors_logger.addHandler(errors_handler)

# (Не давать логгерам пробрасывать логи выше)
business_logger.propagate = False
errors_logger.propagate = False

# Root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(root_handler)

# Отключаем спам от сторонних библиотек
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
