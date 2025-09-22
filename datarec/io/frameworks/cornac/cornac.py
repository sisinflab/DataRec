from datarec.io.frameworks.manager import Framework


class Cornac(Framework):
    """
    Cornac framework adapter.

    Provide metadata, citation, and usage examples for Cornac framework.
    """

    def __init__(self, timestamp, path):
        """
        Initialize Cornac adapter.
        Args:
            timestamp (bool): Whether timestamps are included.
            path (str): Path where the Cornac-compatible dataset is stored.
        """
        self.timestamp = timestamp
        self.path = path

    FRAMEWORK_NAME = 'Cornac'

    REPOSITORY = 'https://github.com/PreferredAI/cornac/tree/master'

    PAPER = """Cornac: A Comparative Framework for Multimodal Recommender Systems"""

    DOI = None

    CITATION = """
            @article{DBLP:journals/jmlr/SalahTL20,
              author       = {Aghiles Salah and
                              Quoc{-}Tuan Truong and
                              Hady W. Lauw},
              title        = {Cornac: {A} Comparative Framework for Multimodal Recommender Systems},
              journal      = {J. Mach. Learn. Res.},
              volume       = {21},
              pages        = {95:1--95:5},
              year         = {2020},
              url          = {http://jmlr.org/papers/v21/19-805.html},
              timestamp    = {Wed, 18 Nov 2020 15:58:12 +0100},
              biburl       = {https://dblp.org/rec/journals/jmlr/SalahTL20.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """
        from cornac.data import Reader
        
        reader = Reader()
        train_data = reader.read(fpath='{path}', fmt="{frmt}")
    """

    DOC = 'https://cornac.preferred.ai/'

    def info_code(self):
        """
        Provide the code to use in Cornac to run experiments.
        """
        if self.timestamp:
            self.CODE = """
        from cornac.data import Reader

        reader = Reader()
        train_data = reader.read(fpath='{path}', fmt="{frmt}")
    """.format(path=self.path, frmt='UIRT')
        else:
            self.CODE = """
                from cornac.data import Reader

                reader = Reader()
                train_data = reader.read(fpath='{path}', fmt="{frmt}")
            """.format(path=self.path, frmt='UIR')
        super().info_code()




