from datarec.io.frameworks.manager import Framework


class DaisyRec(Framework):
    """
    DaisyRec framework adapter.

    Provide metadata, citation, and usage examples for DaisyRec framework.
    """

    def __init__(self, timestamp, path):
        """
        Initialize DaisyRec adapter.
        Args:
            timestamp (bool): Whether timestamps are included.
            path (str): Path where the DaisyRec-compatible dataset is stored.
        """
        self.timestamp = timestamp
        self.path = path

    FRAMEWORK_NAME = 'DaisyRec'

    REPOSITORY = 'https://github.com/recsys-benchmark/DaisyRec-v2.0'

    PAPER = """DaisyRec 2.0: Benchmarking Recommendation for Rigorous Evaluation"""

    DOI = "https://doi.org/10.1109/TPAMI.2022.3231891"

    CITATION = """
            @inproceedings{DBLP:conf/recsys/SunY00Q0G20,
              author       = {Zhu Sun and
                              Di Yu and
                              Hui Fang and
                              Jie Yang and
                              Xinghua Qu and
                              Jie Zhang and
                              Cong Geng},
              editor       = {Rodrygo L. T. Santos and
                              Leandro Balby Marinho and
                              Elizabeth M. Daly and
                              Li Chen and
                              Kim Falk and
                              Noam Koenigstein and
                              Edleno Silva de Moura},
              title        = {Are We Evaluating Rigorously? Benchmarking Recommendation for Reproducible
                              Evaluation and Fair Comparison},
              booktitle    = {RecSys 2020: Fourteenth {ACM} Conference on Recommender Systems, Virtual
                              Event, Brazil, September 22-26, 2020},
              pages        = {23--32},
              publisher    = {{ACM}},
              year         = {2020},
              url          = {https://doi.org/10.1145/3383313.3412489},
              doi          = {10.1145/3383313.3412489},
              timestamp    = {Tue, 21 Mar 2023 20:57:01 +0100},
              biburl       = {https://dblp.org/rec/conf/recsys/SunY00Q0G20.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }
            
            @article{DBLP:journals/pami/SunFYQLYOZ23,
              author       = {Zhu Sun and
                              Hui Fang and
                              Jie Yang and
                              Xinghua Qu and
                              Hongyang Liu and
                              Di Yu and
                              Yew{-}Soon Ong and
                              Jie Zhang},
              title        = {DaisyRec 2.0: Benchmarking Recommendation for Rigorous Evaluation},
              journal      = {{IEEE} Trans. Pattern Anal. Mach. Intell.},
              volume       = {45},
              number       = {7},
              pages        = {8206--8226},
              year         = {2023},
              url          = {https://doi.org/10.1109/TPAMI.2022.3231891},
              doi          = {10.1109/TPAMI.2022.3231891},
              timestamp    = {Fri, 07 Jul 2023 23:32:20 +0200},
              biburl       = {https://dblp.org/rec/journals/pami/SunFYQLYOZ23.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """

    """

    DOC = 'https://daisyrec.readthedocs.io/en/latest/'

    def info_code(self):
        """
        Provide the code to use in DaisyRec to run experiments.
        """
        if self.timestamp:
            self.CODE = f"""
            In DaisyRec you need to replace the file at 
            \'daisy/utils/loader.py\'
            with the file at
            \'datarec/io/frameworks/daisyrec/loader.py\'
            Then you need to open the file, go to line 36 and change \'YOUR_PATH_HERE\' with
            \'{self.path}\'
            """
        else:
            self.CODE = f"""
            In DaisyRec you need to replace the file at 
            \'daisy/utils/loader.py\'
            with the file at
            \'datarec/io/frameworks/daisyrec/loader.py\'
            Then you need to open the file, go to line 36 and change \'YOUR_PATH_HERE\' with
            \'{self.path}\'
            Morover, from the attribute \'names\' you have to remove the timestamp.
            """
        super().info_code()




