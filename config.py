from os import environ

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_IMAGE_PATH = ".\img"
MAX_CONTENT_LENGTH = 16 * 1000 * 1000  # max 16 mb
EXTRACT_RESULT_PATH = ".\output"
JSON_DIR = ".\output\json"
CONN_STRING = environ.get("CONNSTRING_MONGO")
