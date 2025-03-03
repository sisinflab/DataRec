class Framework:
    FRAMEWORK_NAME = None

    PAPER = None

    DOI = None

    CITATION = None

    CODE = None

    REPOSITORY = None

    DOC = None

    def info_code(self):
        print(f"How to use {self.FRAMEWORK_NAME} with DataRec:\n" + self.CODE)

    def info(self):
        if self.FRAMEWORK_NAME is None:
            raise AttributeError

        print(f"If you are going to use {self.FRAMEWORK_NAME} don't forget to cite the paper!")

        if self.PAPER:
            print(f'Paper: \'{self.PAPER}\'')
        if self.DOI:
            print(f'DOI: {self.DOI}')
        if self.CITATION:
            print(f'Bib text from dblp.org:\n {self.CITATION}')

        if self.CODE:
            print(
                '\n================================================ CODE EXAMPLE ================================================\n')
            self.info_code()
            print(
                '==============================================================================================================\n')

        if self.REPOSITORY:
            print(f'For more information check {self.FRAMEWORK_NAME} repository: \'{self.REPOSITORY}\'')

        if self.DOC:
            print(f'More documentation on how to use {self.FRAMEWORK_NAME} at \'{self.DOC}\'')


