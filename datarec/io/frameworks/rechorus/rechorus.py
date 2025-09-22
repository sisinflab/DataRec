import os.path

from datarec.io.frameworks.manager import Framework


class ReChorus(Framework):
    """
    ReChorus framework adapter.

    Provide metadata, citation, and usage examples for ReChorus framework.
    """

    def __init__(self, timestamp, path):
        """
        Initialize ReChorus adapter.
        Args:
            timestamp (bool): Whether timestamps are included.
            path (str): Path where the ReChorus-compatible dataset is stored.
        """
        self.timestamp = timestamp
        directory = os.path.dirname(path)
        self.directory = os.path.abspath(os.path.join(directory, 'DataRec2ReChorus'))
        print('RecBole requires a directory named as the the dataset.\n'
              f'Based on your path the directory that will be used is \'{self.directory}\'')
        if os.path.exists(self.directory) is False:
            os.makedirs(self.directory)

    FRAMEWORK_NAME = 'ReChorus'

    REPOSITORY = 'https://github.com/THUwangcy/ReChorus'

    PAPER = """Make It a Chorus: Knowledge- and Time-aware Item Modeling for Sequential Recommendation"""

    DOI = "https://doi.org/10.1145/3397271.3401131"

    CITATION = """
            @inproceedings{DBLP:conf/sigir/WangZMLM20,
              author       = {Chenyang Wang and
                              Min Zhang and
                              Weizhi Ma and
                              Yiqun Liu and
                              Shaoping Ma},
              editor       = {Jimmy X. Huang and
                              Yi Chang and
                              Xueqi Cheng and
                              Jaap Kamps and
                              Vanessa Murdock and
                              Ji{-}Rong Wen and
                              Yiqun Liu},
              title        = {Make It a Chorus: Knowledge- and Time-aware Item Modeling for Sequential
                              Recommendation},
              booktitle    = {Proceedings of the 43rd International {ACM} {SIGIR} conference on
                              research and development in Information Retrieval, {SIGIR} 2020, Virtual
                              Event, China, July 25-30, 2020},
              pages        = {109--118},
              publisher    = {{ACM}},
              year         = {2020},
              url          = {https://doi.org/10.1145/3397271.3401131},
              doi          = {10.1145/3397271.3401131},
              timestamp    = {Mon, 31 Oct 2022 08:39:18 +0100},
              biburl       = {https://dblp.org/rec/conf/sigir/WangZMLM20.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """

    """

    DOC = None

    def info_code(self):
        """
        Provide the code to use in RecBole to run experiments.
        """
        self.CODE = """
            Dataset must be split and provided in a single folder within the \'data\' folder of the project.\n
            This data will be supported by ReChorus models that adopt a dataset \'BaseModel.Dataset\' \n
            DataRec created this directory here \'{directory}\'.
        """.format(directory=self.directory)

        super().info_code()


