import os
from .rawdata import RawData
from .readers import read_tabular, read_json
from .writers import write_tabular, write_json
from .frameworks import FrameworkExporter

FILE_PATH = os.path.abspath(__file__)
DATAREC_MODULE_FOLDER = '../../'
PROJECT_PATH = os.path.abspath(os.path.join(DATAREC_MODULE_FOLDER, FILE_PATH, os.pardir, os.pardir))
PROJECT_DIRECTORY = os.path.dirname(PROJECT_PATH)


