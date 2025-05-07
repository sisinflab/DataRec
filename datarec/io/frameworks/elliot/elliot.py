import os.path
from datarec.io.frameworks.manager import Framework
from datarec.io.frameworks.elliot.datarec_config import CONF


class Elliot(Framework):

    def __init__(self, timestamp, path):
        self.timestamp = timestamp

        self.directory = os.path.abspath(os.path.dirname(path))
        if os.path.exists(self.directory) is False:
            os.makedirs(self.directory)

        self.train_path, self.test_path, self.val_path = \
            os.path.join(self.directory, 'train.tsv'), \
                os.path.join(self.directory, 'test.tsv'), \
                os.path.join(self.directory, 'validation.tsv')

        self.file = os.path.basename(path)
        self.file_path = os.path.join(self.directory, self.file)

        # create configuration file
        config_file = \
            CONF.format(path=self.file_path,
                        dataset='datarec2elliot',
                        train=self.train_path,
                        test=self.test_path,
                        val=self.val_path)

        self.config_path = os.path.join(self.directory, 'datarec_config.yml')
        with open(self.config_path, 'w') as file:
            file.write(config_file)

    FRAMEWORK_NAME = 'Elliot'

    REPOSITORY = 'https://github.com/sisinflab/elliot'

    PAPER = """Elliot: a Comprehensive and Rigorous Framework for Reproducible Recommender Systems Evaluation"""

    DOI = "https://doi.org/10.1145/3404835.3463245"

    CITATION = """
            @inproceedings{DBLP:conf/sigir/AnelliBFMMPDN21,
              author       = {Vito Walter Anelli and
                              Alejandro Bellog{\'{\i}}n and
                              Antonio Ferrara and
                              Daniele Malitesta and
                              Felice Antonio Merra and
                              Claudio Pomo and
                              Francesco Maria Donini and
                              Tommaso Di Noia},
              editor       = {Fernando Diaz and
                              Chirag Shah and
                              Torsten Suel and
                              Pablo Castells and
                              Rosie Jones and
                              Tetsuya Sakai},
              title        = {Elliot: {A} Comprehensive and Rigorous Framework for Reproducible
                              Recommender Systems Evaluation},
              booktitle    = {{SIGIR} '21: The 44th International {ACM} {SIGIR} Conference on Research
                              and Development in Information Retrieval, Virtual Event, Canada, July
                              11-15, 2021},
              pages        = {2405--2414},
              publisher    = {{ACM}},
              year         = {2021},
              url          = {https://doi.org/10.1145/3404835.3463245},
              doi          = {10.1145/3404835.3463245},
              timestamp    = {Sun, 12 Nov 2023 02:10:04 +0100},
              biburl       = {https://dblp.org/rec/conf/sigir/AnelliBFMMPDN21.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = "  "

    DOC = 'https://elliot.readthedocs.io/en/latest/'

    def info_code(self):
        self.CODE = """
            A configuration file for Elliot has been created here:
            \'{config_path}\'
            You can now run the script.
             If you move the configuration file remember to change the path in the script below.
            
            Elliot script:
            python start_experiments.py --config {config_path}
            
            This script contains a basic recommendation example. Change it if you need.
            """.format(config_path=self.config_path)

        super().info_code()
