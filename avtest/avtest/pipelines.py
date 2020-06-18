import pymysql
from twisted.enterprise import adbapi
from pymysql  import cursors

class JavTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'javlibrary',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
                insert into b(id,time,name,number,title,img_url,movie_url) values(null,null,%s,%s,%s,%s,%s)
               '''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['name'],item['number'],item['title'],item['img_url'],item['movie_url']))

    def handle_error(self, error, item, spider):
        print('=' * 10 + 'error' + '=' * 10)
        print(error)
        print('=' * 10 + 'error' + '=' * 10)