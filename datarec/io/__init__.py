import os
from .rawdata import RawData
from .frameworks import FrameworkExporter

FILE_PATH = os.path.abspath(__file__)
DATAREC_MODULE_FOLDER = '../../'
PROJECT_PATH = os.path.abspath(os.path.join(DATAREC_MODULE_FOLDER, FILE_PATH, os.pardir, os.pardir))
PROJECT_DIRECTORY = os.path.dirname(PROJECT_PATH)


