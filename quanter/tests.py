from django.test import TestCase
from quanter.svm import StockIndex
import pandas as pd
# import MySQLdb
# # Create your tests here.

# db = MySQLdb.connect(user = 'root',password='root',db='test')
# cursor = db.cursor()
# cussor.execute('select * from table')
# result = cursor.fetchall()
# cursor.close()
# db.close()

class StockIndexTestCase(TestCase):
    def setUp(self):
        self.s = StockIndex()
        self.x = pd.Series(range(20))

    def testPSY(self):
        pass