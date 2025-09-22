from datarec.io.frameworks.manager import Framework


class ClayRS(Framework):
    """
    ClayRS framework adapter.

    Provide metadata, citation, and usage examples for ClayRS framework.
    """

    def __init__(self, timestamp, path):
        """
        Initialize ClayRS adapter.
        Args:
            timestamp (bool): Whether timestamps are included.
            path (str): Path where the ClayRS-compatible dataset is stored.
        """
        self.timestamp = timestamp
        self.path = path

    FRAMEWORK_NAME = 'ClayRS'

    REPOSITORY = 'https://github.com/swapUniba/ClayRS/tree/master'

    PAPER = """ClayRS: An end-to-end framework for reproducible knowledge-aware recommender systems"""

    DOI = "https://doi.org/10.1016/j.is.2023.102273"

    CITATION = """
            @article{DBLP:journals/is/LopsPMSS23,
              author       = {Pasquale Lops and
                              Marco Polignano and
                              Cataldo Musto and
                              Antonio Silletti and
                              Giovanni Semeraro},
              title        = {ClayRS: An end-to-end framework for reproducible knowledge-aware recommender
                              systems},
              journal      = {Inf. Syst.},
              volume       = {119},
              pages        = {102273},
              year         = {2023},
              url          = {https://doi.org/10.1016/j.is.2023.102273},
              doi          = {10.1016/J.IS.2023.102273},
              timestamp    = {Mon, 05 Feb 2024 20:19:36 +0100},
              biburl       = {https://dblp.org/rec/journals/is/LopsPMSS23.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """
    from clayrs import content_analyzer 
    
    ratings = content_analyzer.Ratings(content_analyzer.CSVFile(YOUR_PATH_HERE), timestamp_column=3)
    """

    DOC = 'https://swapuniba.github.io/ClayRS/'

    def info_code(self):
        """
        Provide the code to use in ClayRS to run experiments.
        """
        if self.timestamp:
            self.CODE = """
    from clayrs import content_analyzer 
    
    ratings = content_analyzer.Ratings(content_analyzer.CSVFile('{path}'), timestamp_column=3)
    """.format(path=self.path)
        else:
            self.CODE = """
    from clayrs import content_analyzer 
    
    ratings = content_analyzer.Ratings(content_analyzer.CSVFile('{path}'))
    """.format(path=self.path)
        super().info_code()






