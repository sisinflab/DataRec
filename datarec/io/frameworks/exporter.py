from __future__ import annotations  # se vuoi usare le stringhe senza TYPE_CHECKING
from typing import TYPE_CHECKING
import os.path
from datarec.io.rawdata import RawData
from datarec.io.frameworks.clayrs.clayrs import ClayRS
from datarec.io.frameworks.cornac.cornac import Cornac
from datarec.io.frameworks.daisyrec.daisyrec import DaisyRec
from datarec.io.frameworks.lenskit.lenskit import LensKit
from datarec.io.frameworks.recbole.recbole import RecBole
from datarec.io.frameworks.rechorus.rechorus import ReChorus
from datarec.io.frameworks.recpack.recpack import RecPack
from datarec.io.frameworks.recommenders.recommenders import Recommenders
from datarec.io.frameworks.elliot.elliot import Elliot
from datarec.io.writers.transactions.tabular import write_transactions_tabular

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec

class FrameworkExporter:
    """
    Exporter for converting RawData datasets to external recommender system frameworks.

    Provides methods to format a `RawData` object according to
    the expected schema of supported libraries (e.g., Cornac, RecBole).

    """

    def __init__(self, output_path, user=True, item=True, rating=True, timestamp=False):
        """
        Initialize a FrameworkExporter object.
        Args:
            output_path (str): Path where to save the output file.
            user (bool): Whether to write the user information. If True, the user information will be written in the file.
            item (bool): Whether to write the item information. If True, the item information will be written in the file.
            rating (bool): Whether to write the rating information. If True, the rating information will be written in the file.
            timestamp (bool): Whether to write the timestamp information. If True, the timestamp information will be written in the file.
        """
        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.path = output_path
        self.user: bool = user
        self.item: bool = item
        self.rating: bool = rating
        self.timestamp: bool = timestamp

    def to_clayrs(self, data: RawData):
        """
        Export to ClayRS format.
        Args:
            data (RawData): RawData object to convert to ClayRS format.
        """
        write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)

        ClayRS(timestamp=self.timestamp, path=self.path).info()

    def to_cornac(self, data: RawData):
        """
        Export to Cornac format.
        Args:
            data (RawData): RawData object to convert to Cornac format.
        """
        write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)
        Cornac(timestamp=self.timestamp, path=self.path).info()

    def to_daisyrec(self, data: RawData):
        """
        Export to DaisyRec format.
        Args:
            data (RawData): RawData object to convert to DaisyRec format.
        """
        write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)

        DaisyRec(timestamp=self.timestamp, path=self.path).info()

    def to_lenskit(self, data: RawData):
        """
        Export to LensKit format.
        Args:
            data (RawData): RawData object to convert to LensKit format.
        """
        data.data.rename(columns={data.user: "user", data.item: "item", data.rating: "rating"}, inplace=True)
        data.user = "user"
        data.item = "item"
        data.rating = "rating"

        if self.timestamp:
            data.data.rename(columns={data.timestamp: "timestamp"}, inplace=True)
            data.timestamp = "timestamp"
            data.rating = "rating"

        write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)

        LensKit(timestamp=self.timestamp, path=self.path).info()

    def to_recbole(self, data: RawData):
        """
        Export to RecBole format.
        Args:
            data (RawData): RawData object to convert to RecBole format.
        """

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
        write_transactions_tabular(data=data, filepath=frmk.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)

    def to_rechorus(self, train_data: RawData, test_data: RawData, val_data: RawData):
        """
        Export to Rechus format.
        Args:
            train_data (RawData): Training data as RawData object to convert to Rechus format.
            test_data (RawData): Test data as RawData object to convert to Rechus format.
            val_data (RawData): Validation data as RawData object to convert to Rechus format.
        """
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
            write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)

        frmk.info()

    def to_recpack(self, data: RawData):
        """
        Export to RecPack format.
        Args:
            data (RawData): RawData object to convert to RecPack format.
        """

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

        write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)


        frmk.info()

    def to_recommenders(self, data: RawData):
        """
        Export to Recommenders format.
        Args:
            data (RawData): RawData object to convert to Recommenders format.
        """

        frmk = Recommenders(timestamp=self.timestamp, path=self.path)

        data.data.rename(columns={data.user: "user", data.item: "item", data.rating: "rating"}, inplace=True)
        data.user = "item"
        data.item = "rating"
        data.rating = 'rating'
        if self.timestamp:
            data.data.rename(columns={data.timestamp: "timestamp"}, inplace=True)
            data.timestamp = "timestamp"

        write_transactions_tabular(data=data, filepath=self.path, sep=',', header=False, 
                                   include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)


        frmk.info()

    def to_elliot(self, train_data: DataRec, test_data: DataRec, val_data: DataRec):
        """
        Export to Elliot format.
        Args:
            train_data (DataRec): Training data as DataRec object to convert to Elliot format.
            test_data (DataRec): Test data as DataRec object to convert to Elliot format.
            val_data (DataRec): Validation data as DataRec object to convert to Elliot format.
        """

        frmk = Elliot(timestamp=self.timestamp, path=self.path)

        for data, name in zip([train_data.to_rawdata(), test_data.to_rawdata(), val_data.to_rawdata()],
                              [frmk.train_path, frmk.test_path, frmk.val_path]):
            columns_order = [data.user, data.item, data.rating]
            if self.timestamp:
                columns_order.append(data.timestamp)

            write_transactions_tabular(data=data, filepath=name, sep='\t', header=False,
                          include_user=self.user, include_item=self.item, include_rating=self.rating, include_timestamp=self.timestamp)

        frmk.info()
        train_data.pipeline.add_step("export", "Elliot", self.params)
        test_data.pipeline.add_step("export", "Elliot", self.params)
        val_data.pipeline.add_step("export", "Elliot", self.params)
