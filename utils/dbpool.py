from dbutils.pooled_db import PooledDB
from utils.singleton import Singleton
import pymysql

MYSQL_PORT = 3306
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "notes"


class DatabaseConnectionPool(Singleton):
    # MYSQL CONFIG
    def __init__(self, user, password, dbname, host='127.0.0.1', port=3306):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=6,
            mincached=2,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            cursorclass=pymysql.cursors.DictCursor
        )

    def fetchall(self, sql):
        return self.__fetch(sql, one_or_all=False)

    def fetchone(self, sql):
        return self.__fetch(sql, one_or_all=True)

    def __fetch(self, sql, one_or_all=True):
        with self.pool.connection() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            query_result = cursor.fetchone() if one_or_all else cursor.fetchall()
            cursor.close()
        return query_result


if __name__ == '__main__':
    pool = DatabaseConnectionPool(user=MYSQL_USER, password=MYSQL_PASSWORD, dbname=MYSQL_DATABASE)
    # res = pool.fetchall('select count(*) as count from library;')
    pool2 = DatabaseConnectionPool.getInstances()
    print(pool == pool2)
# conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
# cur = conn.cursor()
# SQL = "select UserID,Password from UserTable"
# r = cur.execute(SQL)
# r = cur.fetchall()
# print(type(r))
# print(r)
# for UserID in r:
#     print(type(UserID), UserID)
# cur.close()
# conn.close()
# print("\n####linkMySql  End")
# 异常输出
