import pymysql
import redis
from django.shortcuts import render, redirect
from django.test import TestCase
from decimal import Decimal
# Create your tests here.
def read(table_name,index):
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='store',charset='utf8')
    cur=conn.cursor()
    cur.execute("select * from %s"%table_name)
    r=list(cur.fetchall())
    d={}
    for i in range(len(r)):
        d[r[i][index]]=[r[i][j] for j in range(len(r[i]))]
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return d
def con_mysql():
    return pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='store',charset='utf8')
def permission(cook):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select power from user where account='%s'" % cook)
    a = cursor.fetchall()
    conn.commit()
    cursor.close()
    return a[0][0]
def insert_type(table_name,desc):
    conn=con_mysql()
    cursor=conn.cursor()
    cursor.execute("insert into good_type values('%s','%s')"%(table_name,desc))
    conn.commit()
    cursor.close()

def delete(table,who,key):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("delete from %s where %s=%s"%(table,who,key))
    conn.commit()
    cursor.close()
def find(a,b,c):
    r=read(a,b)
    d={}
    for keys,values in r.items():
        if keys==c:
            for i in range(len(values)):
                d['a'+str(i)]=values[i]
    return d

def show(a,b):
    r=read(a,b)
    lists=[]
    for keys,values in r.items():
        d = {}
        for i in range(len(values)):
            d['a'+str(i)]=values[i]
        lists.append(d)
    return lists
def reads(table_name,index):
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='store',charset='utf8')
    cur=conn.cursor()
    cur.execute("select * from goods where title=(select sort from goods_type where type_id=%s )"%table_name)
    r=list(cur.fetchall())
    d={}
    for i in range(len(r)):
        d[r[i][index]]=[r[i][j] for j in range(len(r[i]))]
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return d
# k='红酒'
# print(read("goods where locate('%s',title)>0 or locate('%s',goods_name)>0"%(k,k),0))
# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# r = redis.Redis(connection_pool=pool)
# k='3456'
# r.set('123',value='[123,232]')
# r.lpush("%s"%k,123)
# r.lpush("%s"%k,456)
# li=r.lrange('3456',0,4)
# print(type(li))
# print(li)
def readss(table_name,):
    conn = con_mysql()
    cur=conn.cursor()
    cur.execute("select * from %s" % table_name)
    r=list(cur.fetchall())

    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return r
k='1234511'
print(readss("goods where goods_id=%s"%k))





