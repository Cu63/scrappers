import pymysql


conn = pymysql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock',
                       user='root', passwd='root', db='mysql')

cur = conn.cursor()
cur.execute('USE scraping')
cur.execute('SELECT * FROM page WHERE id=1')
print(cur.fetchone())
cur.close()
conn.close()
