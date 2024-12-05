import os
import ydb
import ydb.iam
from Barcode import Barcode
import binascii


class Database:
    def __init__(self) -> None:
        driver = ydb.Driver(endpoint=os.getenv('YDB_ENDPOINT'), database=os.getenv('YDB_DATABASE'),
                            credentials=ydb.iam.MetadataUrlCredentials())
        driver.wait(fail_fast=True, timeout=5)
        self.pool = ydb.SessionPool(driver)

    def do_sql(self, session: ydb.SessionPool, sql: str) -> list:
        result = session.transaction().execute(sql, commit_tx=True, settings=ydb.BaseRequestSettings().with_timeout(
            3).with_operation_timeout(2))
        return result

    def get_item_by_barcode(self, barcode: int) -> Barcode or None:
        result = self.pool.retry_operation_sync(lambda session: self.do_sql(session,
                                                                   f"SELECT barcode, name, shugar, fats, squirrels, carbohydrates FROM barcodes WHERE barcode = {barcode}"))
        
        if result[0].rows:
            return self.barcode_from_array(result[0].rows[0].values())
        return None

    def get_max_id(self, session: ydb.SessionPool) -> int:
        maxId = session.transaction().execute(
        'SELECT max(id) FROM barcodes;',
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2))[0].rows[0]['column0']
        return maxId


    def add_new_barcode(self, barcode: str, name: str, p1: str, p2: str, p3: str, p4: str):
        maxid = self.pool.retry_operation_sync(self.get_max_id)
        result = self.pool.retry_operation_sync(lambda session: self.do_sql(session,
                                                               f"""INSERT INTO barcodes(id, barcode, name, shugar, fats, squirrels, carbohydrates) VALUES({maxid + 1}, {barcode}, "{name}", {p1}, {p2}, {p3}, {p4})"""))
        
       
        
    

    def barcode_from_array(self, arr: list) -> Barcode:
        barcode = Barcode(*arr)
        return barcode
