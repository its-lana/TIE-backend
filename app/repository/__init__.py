import os
import sys
from pymongo import MongoClient
from config import CONN_STRING

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "../..")))


# client = MongoClient(CONN_STRING)
client = MongoClient("mongodb://localhost:27017")
db = client["table_information_extraction_db"]

from repository import tableRepo, documentTypeRepo, htmlRepo
