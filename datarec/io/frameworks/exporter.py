import os.path

from datarec.io import RawData
from datarec.io import write_tabular
from datarec.io.frameworks.clayrs.clayrs import ClayRS
from datarec.io.frameworks.cornac.cornac import Cornac
from datarec.io.frameworks.daisyrec.daisyrec import DaisyRec
from datarec.io.frameworks.lenskit.lenskit import LensKit
from datarec.io.frameworks.recbole.recbole import RecBole
from datarec.io.frameworks.rechorus.rechorus import ReChorus
from datarec.io.frameworks.recpack.recpack import RecPack
from datarec.io.frameworks.recommenders.recommenders import Recommenders
from datarec.io.frameworks.elliot.elliot import Elliot


class FrameworkExporter:

    def __init__(self, output_path, user=True, item=True, rating=True, timestamp=False):
        self.path = output_path
        self.user = user
        self.item = item
        self.rating = rating
        self.timestamp = timestamp

    def to_clayrs(self, data: RawData):
        write_tabular(rawdata=data, path=self.path, sep=',', header=False,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        ClayRS(timestamp=self.timestamp, path=self.path).info()

    def to_cornac(self, data: RawData):
        write_tabular(rawdata=data, path=self.path, sep='\t', header=False,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        Cornac(timestamp=self.timestamp, path=self.path).info()

    def to_daisyrec(self, data: RawData):
        write_tabular(rawdata=data, path=self.path, sep='\t', header=False,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        DaisyRec(timestamp=self.timestamp, path=self.path).info()

    def to_lenskit(self, data: RawData):
        data.data.rename(columns={data.user: "user", data.item: "item",
                                  data.rating: "rating"}, inplace=True)
        data.user = "user"
        data.item = "item"
        data.rating = "rating"

        if self.timestamp:
            data.data.rename(columns={data.timestamp: "timestamp"}, inplace=True)
            data.timestamp = "timestamp"
            data.rating = "rating"

        write_tabular(rawdata=data, path=self.path, sep='\t', header=False,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        LensKit(timestamp=self.timestamp, path=self.path).info()

    def to_recbole(self, data: RawData):

        data.data.rename(columns={data.user: "user: token", data.item: "item: token",
                                  data.rating: "rating: float"}, inplace=True)
        data.user = "user: token"
        data.item = "item: token"
        data.rating = "rating: float"

        if self.timestamp:
            data.data.rename(columns={data.timestamp: "timestamp"}, inplace=True)
            data.timestamp = "timestamp:float"

        frmk = RecBole(timestamp=self.timestamp, path=self.path)
        frmk.info()

        write_tabular(rawdata=data, path=frmk.path, sep='\t', header=True,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

    def to_rechorus(self, train_data: RawData, test_data: RawData, val_data: RawData):
        # user_id	item_id	time
        if self.rating:
            print('Ratings will be interpreted as implicit interactions.')
            self.rating = False

        frmk = ReChorus(timestamp=self.timestamp, path=self.path)

        for data, name in zip([train_data, test_data, val_data], ['train.csv', 'dev.csv', 'test.csv']):
            data.data.rename(columns={data.user: "user_id", data.item: "item_id"}, inplace=True)
            data.user = "user_id"
            data.item = "item_id"

            if self.timestamp:
                data.data.rename(columns={data.timestamp: "time"}, inplace=True)
                data.timestamp = "time"

            path = os.path.join(frmk.directory, name)
            write_tabular(rawdata=data, path=path, sep='\t', header=True,
                          user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        frmk.info()

    def to_recpack(self, data: RawData):

        if self.rating:
            print('Ratings will be interpreted as implicit interactions.')
            self.rating = False

        frmk = RecPack(timestamp=self.timestamp, path=self.path)

        data.data.rename(columns={data.user: "userId", data.item: "itemId"}, inplace=True)
        data.user = "userId"
        data.item = "itemId"
        if self.timestamp:
            data.data.rename(columns={data.timestamp: "timestamp"}, inplace=True)
            data.timestamp = "timestamp"

        write_tabular(rawdata=data, path=frmk.file_path, sep='\t', header=True,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        frmk.info()

    def to_recommenders(self, data: RawData):

        frmk = Recommenders(timestamp=self.timestamp, path=self.path)

        data.data.rename(columns={data.user: "user", data.item: "item", data.rating: "rating"}, inplace=True)
        data.user = "item"
        data.item = "rating"
        data.rating = 'rating'
        if self.timestamp:
            data.data.rename(columns={data.timestamp: "timestamp"}, inplace=True)
            data.timestamp = "timestamp"

        write_tabular(rawdata=data, path=frmk.file_path, sep='\t', header=True,
                      user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        frmk.info()

    def to_elliot(self, train_data: RawData, test_data: RawData, val_data: RawData):

        frmk = Elliot(timestamp=self.timestamp, path=self.path)

        for data, name in zip([train_data, test_data, val_data], [frmk.train_path, frmk.test_path, frmk.val_path]):
            columns_order = [data.user, data.item, data.rating]
            if self.timestamp:
                columns_order.append(data.timestamp)

            write_tabular(rawdata=data, path=name, sep='\t', header=False,
                          user=self.user, item=self.item, rating=self.rating, timestamp=self.timestamp)

        frmk.info()
