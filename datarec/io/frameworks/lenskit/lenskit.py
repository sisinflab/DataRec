from datarec.io.frameworks.manager import Framework


class LensKit(Framework):

    def __init__(self, timestamp, path):
        self.timestamp = timestamp
        self.path = path

    FRAMEWORK_NAME = 'LensKit'

    REPOSITORY = 'https://github.com/lenskit/lkpy'

    PAPER = """LensKit for Python: Next-Generation Software for Recommender Systems Experiments"""

    DOI = "https://doi.org/10.1145/3340531.3412778"

    CITATION = """
            @inproceedings{DBLP:conf/cikm/Ekstrand20,
              author       = {Michael D. Ekstrand},
              editor       = {Mathieu d'Aquin and
                              Stefan Dietze and
                              Claudia Hauff and
                              Edward Curry and
                              Philippe Cudr{\'{e}}{-}Mauroux},
              title        = {LensKit for Python: Next-Generation Software for Recommender Systems
                              Experiments},
              booktitle    = {{CIKM} '20: The 29th {ACM} International Conference on Information
                              and Knowledge Management, Virtual Event, Ireland, October 19-23, 2020},
              pages        = {2999--3006},
              publisher    = {{ACM}},
              year         = {2020},
              url          = {https://doi.org/10.1145/3340531.3412778},
              doi          = {10.1145/3340531.3412778},
              timestamp    = {Tue, 29 Dec 2020 18:42:41 +0100},
              biburl       = {https://dblp.org/rec/conf/cikm/Ekstrand20.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """

    """

    DOC = 'https://lkpy.lenskit.org/en/stable/'

    def info_code(self):
        self.CODE = """
        LensKit accepts pandas DataFrames with specific column naming. DataRec will do that for you!
        
        import pandas as pd
        
        ratings = pd.read_csv({path}, sep='\\t', header=False)
        """.format(path=self.path)

        super().info_code()




