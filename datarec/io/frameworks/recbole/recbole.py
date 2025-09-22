import os.path

from datarec.io.frameworks.manager import Framework


class RecBole(Framework):
    """
    RecBole framework adapter.

    Provide metadata, citation, and usage examples for RecBole framework.
    """

    def __init__(self, timestamp, path):
        """
        Initialize RecBole adapter.
        Args:
            timestamp (bool): Whether timestamps are included.
            path (str): Path where the RecBole-compatible dataset is stored.
        """
        self.timestamp = timestamp
        directory = os.path.dirname(path)
        self.directory = os.path.join(directory, 'DataRec2RecBole')
        print('RecBole requires a directory named as the the dataset.\n'
              f'Based on your path the directory that will be used is \'{self.directory}\'')
        if os.path.exists(self.directory) is False:
            os.makedirs(self.directory)
        self.path = os.path.join(self.directory, path)

    FRAMEWORK_NAME = 'RecBole'

    REPOSITORY = 'https://github.com/RUCAIBox/RecBole2.0'

    PAPER = """RecBole 2.0: Towards a More Up-to-Date Recommendation Library"""

    DOI = "https://doi.org/10.1145/3511808.3557680"

    CITATION = """
            @inproceedings{DBLP:conf/cikm/ZhaoMHLCPLLWTMF21,
              author       = {Wayne Xin Zhao and
                              Shanlei Mu and
                              Yupeng Hou and
                              Zihan Lin and
                              Yushuo Chen and
                              Xingyu Pan and
                              Kaiyuan Li and
                              Yujie Lu and
                              Hui Wang and
                              Changxin Tian and
                              Yingqian Min and
                              Zhichao Feng and
                              Xinyan Fan and
                              Xu Chen and
                              Pengfei Wang and
                              Wendi Ji and
                              Yaliang Li and
                              Xiaoling Wang and
                              Ji{-}Rong Wen},
              editor       = {Gianluca Demartini and
                              Guido Zuccon and
                              J. Shane Culpepper and
                              Zi Huang and
                              Hanghang Tong},
              title        = {RecBole: Towards a Unified, Comprehensive and Efficient Framework
                              for Recommendation Algorithms},
              booktitle    = {{CIKM} '21: The 30th {ACM} International Conference on Information
                              and Knowledge Management, Virtual Event, Queensland, Australia, November
                              1 - 5, 2021},
              pages        = {4653--4664},
              publisher    = {{ACM}},
              year         = {2021},
              url          = {https://doi.org/10.1145/3459637.3482016},
              doi          = {10.1145/3459637.3482016},
              timestamp    = {Tue, 07 May 2024 20:05:19 +0200},
              biburl       = {https://dblp.org/rec/conf/cikm/ZhaoMHLCPLLWTMF21.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }
            @inproceedings{DBLP:conf/cikm/ZhaoHPYZLZBTSCX22,
              author       = {Wayne Xin Zhao and
                              Yupeng Hou and
                              Xingyu Pan and
                              Chen Yang and
                              Zeyu Zhang and
                              Zihan Lin and
                              Jingsen Zhang and
                              Shuqing Bian and
                              Jiakai Tang and
                              Wenqi Sun and
                              Yushuo Chen and
                              Lanling Xu and
                              Gaowei Zhang and
                              Zhen Tian and
                              Changxin Tian and
                              Shanlei Mu and
                              Xinyan Fan and
                              Xu Chen and
                              Ji{-}Rong Wen},
              editor       = {Mohammad Al Hasan and
                              Li Xiong},
              title        = {RecBole 2.0: Towards a More Up-to-Date Recommendation Library},
              booktitle    = {Proceedings of the 31st {ACM} International Conference on Information
                              {\&} Knowledge Management, Atlanta, GA, USA, October 17-21, 2022},
              pages        = {4722--4726},
              publisher    = {{ACM}},
              year         = {2022},
              url          = {https://doi.org/10.1145/3511808.3557680},
              doi          = {10.1145/3511808.3557680},
              timestamp    = {Sun, 20 Aug 2023 12:23:03 +0200},
              biburl       = {https://dblp.org/rec/conf/cikm/ZhaoHPYZLZBTSCX22.bib},
              bibsource    = {dblp computer science bibliography, https://dblp.org}
            }"""

    CODE = """

    """

    DOC = 'https://recbole.io/'

    def info_code(self):
        """
        Provide the code to use in RecBole to run experiments.
        """
        self.CODE = """
            from recbole.data import create_dataset
            from recbole.config import Config

            config_dict = {{
                "dataset": "datarec",
                "data_path": {path},
            }}
            config = Config(config_dict=config_dict, config_file_list=config_file_list)
            dataset = create_dataset(config)
        """.format(path=self.path)

        super().info_code()



