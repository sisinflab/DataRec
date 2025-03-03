import os.path
from datarec.io.frameworks.manager import Framework


class Recommenders(Framework):

    def __init__(self, timestamp, path):
        self.timestamp = timestamp
        self.directory = os.path.abspath(os.path.dirname(path))
        if os.path.exists(self.directory) is False:
            os.makedirs(self.directory)
        self.file = os.path.basename(path)
        self.file_path = os.path.join(self.directory, self.file)

    FRAMEWORK_NAME = 'Recommenders'

    REPOSITORY = 'https://github.com/recommenders-team/recommenders?tab=readme-ov-file'

    PAPER = """Microsoft recommenders: tools to accelerate developing recommender systems"""

    DOI = "https://doi.org/10.1145/3298689.3346967"

    CITATION = """
            @inproceedings{DBLP:conf/recsys/GrahamMW19,
              author       = {Scott Graham and
                              Jun{-}Ki Min and
                              Tao Wu},
              editor       = {Toine Bogers and
                              Alan Said and
                              Peter Brusilovsky and
                              Domonkos Tikk},
              title        = {Microsoft recommenders: tools to accelerate developing recommender
                              systems},
              booktitle    = {Proceedings of the 13th {ACM} Conference on Recommender Systems, RecSys
                              2019, Copenhagen, Denmark, September 16-20, 2019},
              pages        = {542--543},
              publisher    = {{ACM}},
              year         = {2019},
              url          = {https://doi.org/10.1145/3298689.3346967},
              doi          = {10.1145/3298689.3346967},
              timestamp    = {Wed, 09 Oct 2019 14:20:04 +0200},
              biburl       = {https://dblp.org/rec/conf/recsys/GrahamMW19.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """

    """

    DOC = 'https://recommenders-team.github.io/recommenders'

    def info_code(self):
        if self.timestamp:
            self.CODE = """
                import pandas as pd

                data = pd.read_csv({file}, sep="\\t", names=['user', 'item', 'rating', 'timestamp'])
                """.format(file=self.file_path)
        else:
            self.CODE = """
                import pandas as pd
                
                data = pd.read_csv({file}, sep="\\t", names=['user', 'item', 'rating'])
                """.format(file=self.file_path)

        super().info_code()
