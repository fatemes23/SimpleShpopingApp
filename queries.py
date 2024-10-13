from datetime import datetime
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Tables import *
from sqlalchemy import desc

engine = sal.create_engine('mssql+pyodbc://DESKTOP-PCE1II2/ProjectDB?driver=SQL Server?Trusted_Connection=yes')
conn = engine.connect()
# create a Session

Session = sessionmaker(bind=engine)
session = Session()


# Create objects
def insertCustomer(name ):
    customer = Customer(name)
    session.add(customer)
    session.commit()

def insertProduct(pname , price):
    product = Product(pname , price )
    session.add(product)
    session.commit()

def insertOrder(oDate , cid):
    order = Order(oDate , cid )
    session.add(order)
    session.commit()



def insertOrderItem(oid , qty , pid):
    orderitem = OrderItem(oid , qty , pid)
    session.add(orderitem)
    session.commit()

def allCustomers ():
    customers = []
    for customer in session.query(Customer).all():
        cust={}
        cust['cid'] = customer.cid
        cust['cname'] = customer.cname
        customers.append(cust)
    return customers

def allProducts ():
    products = []
    for product in session.query(Product).all():
        p={}
        p['pid'] = product.pid
        p['pname'] = product.pname
        p['price'] = product.price
        products.append(p)
    return products

def allOrders ():
    orders = []
    for order in session.query(Order).order_by(Order.oDate.desc()).all():
        o={}
        o['oid'] = order.oid
        o['oDate'] = order.oDate
        o['cid'] = order.cid
        o['cname'] = session.query(Customer).get(order.cid).cname
        orders.append(o)
    return orders

def allOrderItems():
    orderItems = []
    for orderitem in session.query(OrderItem).all():
        oi={}
        oi['iid'] =orderitem.iid
        oi['oid'] =orderitem.oid
        oi['qty'] =orderitem.qty
        oi['pid'] =orderitem.pid
        oi['pname'] = session.query(Product).get(orderitem.pid).pname
        orderItems.append(oi)
    return orderItems

def findCusomerById(cid):
    cust = {}
    cust['cid'] = session.query(Customer).get(cid).cid
    cust['cname'] = session.query(Customer).get(cid).cname
    return cust

def findProductById(pid) :
    product = {}
    product['pid'] = session.query(Product).get(pid).pid
    product['pname'] = session.query(Product).get(pid).pname
    product['price'] = session.query(Product).get(pid).price
    return product

def findOrderById(oid) :
    order = {}
    order['oid'] = session.query(Order).get(oid).oid
    order['oDate'] = session.query(Order).get(oid).oDate
    order['cid'] = session.query(Order).get(oid).cid
    return order

def findOrderItemById(iid) :
    orderitem = {}
    orderitem['iid'] = session.query(OrderItem).get(iid).iid
    orderitem['oid'] = session.query(OrderItem).get(iid).oid
    orderitem['qty'] = session.query(OrderItem).get(iid).qty
    orderitem['pid'] = session.query(OrderItem).get(iid).pid
    return orderitem

def allorderOfCustomer(cid) :
    orders = []
    for order in session.query(Order).filter(Order.cid == cid).order_by(Order.oDate.desc()):
        o ={}
        o['oid'] = order.oid
        o['oDate'] = order.oDate
        o['cid'] = order.cid
        o['cname'] = session.query(Customer).get(order.cid).cname
        orders.append(o)
    return orders

def allOrderItemofOrder(oid):
    orderitems = []
    for orderitem in session.query(OrderItem).filter(OrderItem.oid == oid):
        o ={}
        o['oid'] = orderitem.oid
        o['iid'] = orderitem.iid
        o['pid'] = orderitem.pid
        o['qty'] = orderitem.qty
        o['pname'] = session.query(Product).get(orderitem.pid).pname
        orderitems.append(o)
    return orderitems

def productOfOrderItem(iid) :
    pid = session.query(OrderItem).get(iid).pid
    product = {}
    product['pid'] = session.query(Product).get(pid).pid
    product['pname'] = session.query(Product).get(pid).pname
    product['price'] = session.query(Product).get(pid).price
    return product

def updateCustomerName(cid , newCname) :
    session.query(Customer).filter(Customer.cid == cid).update({Customer.cname:newCname}, synchronize_session = False)
    session.commit()

#________method e bayad moshakhs koni kodoomo mikhaii update koni hatmn___________#
def updateproduct( pid , newPname="",newPrice =-1 ):
    prevprice = session.query(Product).get(pid).price
    prevpname = session.query(Product).get(pid).pname
    if ( newPname==""):
        newPname = prevpname
    if( newPrice == -1 ) :
        newPrice = prevprice
    product = session.query(Product).get(pid)
    product.pname = newPname
    product.price= newPrice
    session.commit()


def updateOrderItem ( iid , newqty):
    session.query(OrderItem).filter(OrderItem.iid == iid).update({OrderItem.qty:newqty}, synchronize_session = False)
    session.commit()

def deleteCustomer(cid):
    session.query(Customer).filter(Customer.cid==cid).delete()
    session.commit()
    # obj=session.query(Customer).filter(Customer.cid==cid).first()
    # session.delete(obj)
    # session.commit()

def deleteProduct(pid):
    session.query(Product).filter(Product.pid==pid).delete()
    session.commit()


def deleteOrder(oid):
    session.query(Order).filter(Order.oid==oid).delete()
    session.commit()


def deleteOrderItem(iid):
    session.query(OrderItem).filter(OrderItem.iid==iid).delete()
    session.commit()
# commit the record the database

# insertCustomer('cust1')
# insertCustomer('cust2')
# insertProduct('product1',100)
# insertProduct('product2',200)
# insertOrder(date.today() , 5)
# insertOrder(datetime.now() , 2)
# insertOrderItem(9,2,9)
# insertOrderItem(10,2,10)
# print ('all customers ',allCustomers() )
# print('all products ', allProducts())
# print('all orders ' , allOrders())
# print( "all order item " , allOrderItems())
# print ('find costomer by id  ', findCusomerById(2))
# print('find product by id ' , findProductById(1))
# print('find order by id ' , findOrderById(2))
# print('find orderItem by id ' , findOrderItemById(1))
# print('all order of customer ', allorderOfCustomer(2))
# print('all order item of order ' , allOrderItemofOrder(2))
# print ( 'find product detail by having iid ',productOfOrderItem(1) )
# print ( 'update name of customer Name ' )
# updateCusomerName(2,'fateme')
# print ('all customers ',allCustomers() ) ;
# print ( 'update price of product ' )
# updateproduct(1,newPrice=170 )
# print('all products ', allProducts())
# print("__delete customer__")
#deleteCustomer(6)
# print("__delete product__")
#deleteProduct(12)
# deleteOrder(2)
# deleteProduct(1)
#deleteOrderItem(13)
# updateOrderItem(14,10)
#
# print('all products ', allProducts())
# print ('all customers ',allCustomers() ) ;
# print('all orders ' , allOrders())
# print( "all order item " , allOrderItems())
#


# session.commit()
