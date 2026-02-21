import sqlite3
from customer.models import Contact,Category,SubCategory,Product,customerOrder,updateStatus,userreview,cacnceledorder
from django.contrib.auth.models import User
from django.db import connection


db = sqlite3.connect('Database.sqlite3') 
cur = db.cursor()
res= cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(res.fetchall())

res= cur.execute("SELECT total(totalprice) FROM customer_customerorder")
print(res.fetchall())

def totalRevenue():
    with connection.cursor() as cursor:
        cursor.execute("SELECT total(totalprice) FROM customer_customerorder")
        row = cursor.fetchone()
    return row[0]
    
    
def pendingOrders():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM customer_customerorder WHERE status=\"Processing\"")
        row = cursor.fetchone()
    return row[0]

def cancelledOrders():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM customer_cacnceledorder")
        row = cursor.fetchone()
    return row[0]
