import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='password',
    port=3306,
    db='egg_price',
    charset='GBK')
conn.autocommit(1)