import os.path
from datarec.io.frameworks.manager import Framework


class RecPack(Framework):

    def __init__(self, timestamp, path):
        self.timestamp = timestamp
        self.directory = os.path.abspath(os.path.dirname(path))
        if os.path.exists(self.directory) is False:
            os.makedirs(self.directory)
        self.file = os.path.basename(path)
        self.file_path = os.path.join(self.directory, self.file)

    FRAMEWORK_NAME = 'RecPack'

    REPOSITORY = 'https://github.com/LienM/recpack'

    PAPER = """RecPack: An(other) Experimentation Toolkit for Top-N Recommendation using Implicit Feedback Data"""

    DOI = "https://doi.org/10.1145/3523227.3551472"

    CITATION = """
            @inproceedings{DBLP:conf/recsys/MichielsVG22,
              author       = {Lien Michiels and
                              Robin Verachtert and
                              Bart Goethals},
              editor       = {Jennifer Golbeck and
                              F. Maxwell Harper and
                              Vanessa Murdock and
                              Michael D. Ekstrand and
                              Bracha Shapira and
                              Justin Basilico and
                              Keld T. Lundgaard and
                              Even Oldridge},
              title        = {RecPack: An(other) Experimentation Toolkit for Top-N Recommendation
                              using Implicit Feedback Data},
              booktitle    = {RecSys '22: Sixteenth {ACM} Conference on Recommender Systems, Seattle,
                              WA, USA, September 18 - 23, 2022},
              pages        = {648--651},
              publisher    = {{ACM}},
              year         = {2022},
              url          = {https://doi.org/10.1145/3523227.3551472},
              doi          = {10.1145/3523227.3551472},
              timestamp    = {Mon, 01 May 2023 13:01:24 +0200},
              biburl       = {https://dblp.org/rec/conf/recsys/MichielsVG22.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """

    """

    DOC = 'https://recpack.froomle.ai/'

    def info_code(self):
        self.CODE = """
            For using a dataset from DataRec you need to:
            1) copy/move the file 
            \'datarec/io/frameworks/recpack/datarec.py\'
            at \'recpack/datasets/datarec.py\'
            2) replace the content of the init file in RecPack
            \'datarec/io/frameworks/recpack/__init__.py\'
            with the content of
            \'datarec/io/frameworks/recpack/copy_me_in__init__.py\'
            Then you can use this code
            
            from recpack.datasets import DummyDataset
            dataset = (path={file}, filename={directory}, use_default_filters=False)
        """.format(file=self.file, directory=self.directory)

        super().info_code()


