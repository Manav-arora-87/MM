import pymysql as mysql
def CollectionPool():
    db=mysql.connect(host="localhost",db='mm',port=3306,user='root',password='Annu@786')
    cmd= db.cursor(mysql.cursors.DictCursor)
    return (db,cmd)
