import logging
import os

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

# Formato general del log
log_format = "[%(asctime)s] [%(levelname)s] %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Handler para logs de INFO y DEBUG
info_handler = logging.FileHandler("logs/api-debug.log")
info_handler.setLevel(logging.DEBUG)
info_handler.setFormatter(logging.Formatter(log_format, date_format))

# Handler para logs de WARNING y ERROR
error_handler = logging.FileHandler("logs/api-error.log")
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(logging.Formatter(log_format, date_format))

# Consola (útil para systemd/journalctl)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format, date_format))

# Logger principal
logger = logging.getLogger("sktcod-api")
logger.setLevel(logging.DEBUG)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

# Evita duplicado si se importa varias veces
logger.propagate = False

