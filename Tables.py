import pyodbc
import sqlalchemy as sal

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from sqlalchemy.orm import sessionmaker

engine = sal.create_engine('mssql+pyodbc://DESKTOP-PCE1II2/ProjectDB?driver=SQL Server?Trusted_Connection=yes')
conn = engine.connect()
Base = declarative_base()
# print(engine.table_names())#print table names
#
# result = engine.execute('select * from CustomerTable')
# for row in result:
#     print (row)


# Session = sessionmaker(bind=engine)
# session = Session()
# our_user = session.query(CustomerTable).first()
# print(our_user)

class Customer(Base):
    """"""
    __tablename__ = "CustomerTable"

    cid = Column(Integer, primary_key=True)
    cname = Column(String)

    def __init__(self, cname):
        """"""
        self.cname = cname
class Product(Base):
    """"""
    __tablename__ = "ProductTable"

    pid = Column(Integer, primary_key=True)
    pname = Column(String)
    price = Column(Integer)

    def __init__(self, pname, price):
        """"""
        self.pname = pname
        self.price = price

class Order(Base):
    __tablename__ = 'OrderTable'
    oid = Column(Integer, primary_key=True)
    oDate = Column(Date)
    cid = Column(Integer, ForeignKey('CustomerTable.cid'))
    def __init__(self, oDate, cid):
        """"""
        self.oDate = oDate
        self.cid = cid
class OrderItem(Base):
    __tablename__ = 'OrderItemTable'
    iid = Column(Integer, primary_key=True)
    oid = Column(Integer, ForeignKey('OrderTable.oid'))
    qty = Column(Integer)
    pid = Column(Integer, ForeignKey('ProductTable.pid'))
    def __init__(self, oid, qty,pid):
        """"""
        self.oid = oid
        self.qty = qty
        self.pid = pid
# create tables
Base.metadata.create_all(engine)
