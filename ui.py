import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import queries
import datetime

def updateCustomer(cid, newname):
    if newname != "":
        queries.updateCustomerName(cid, newname)
        customers_screen()


def customers_screen():
    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("500x400")
    screen.title("Customers")

    Label(screen, text="ID", width = 5).grid(column=0, row=0)
    Label(screen, text="Name", width = 15).grid(column=1, row=0)
    Label(screen, text="New Name", width = 15).grid(column=2, row=0)

    customers = queries.allCustomers()
    for i in range(len(customers)):
        Label(screen, text=customers[i]['cid']).grid(column=0, row=i+1)
        Label(screen, text=customers[i]['cname']).grid(column=1, row=i+1)
        customers[i]['newname'] = StringVar()
        Entry(screen, width=15, textvariable=customers[i]['newname']).grid(column=2, row=i+1)
        Button(screen, text="edit", width = 4, height = 2, command = lambda x=i : updateCustomer(customers[x]['cid'], customers[x]['newname'].get()) ).grid(column=3, row=i+1)
        Button(screen, text="orders", width = 4, height = 2, command = lambda x=i : CustomerOrders_screen(customers[x]['cid']) ).grid(column=4, row=i+1)
        Button(screen, text="delete", width = 4, height = 2, command = lambda x=i : deleteCustomer(customers[x]['cid']) ).grid(column=5, row=i+1)

    NewCustomerName = StringVar()
    Entry(screen, width = 15, textvariable = NewCustomerName).grid(column=1, row=len(customers)+1)
    Button(screen, text="ADD", width = 4, height = 2, command = lambda : insertCustomer(NewCustomerName.get()) ).grid(column=2, row=len(customers)+1)
    Button(screen, text = "BACK", width = 10, height = 2, command = lambda : home_screen()).grid(column=0, row = len(customers)+2)

    screen.mainloop()

def insertCustomer(name):
    if name != "":
        queries.insertCustomer(name)
        customers_screen()

def deleteCustomer(id):
    queries.deleteCustomer(id)
    customers_screen()


def OrderItems_screen(oid, cid):
    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("600x400")
    screen.title("Order Items")

    Label(screen, text="Order ID", width = 10).grid(column=0, row=0)
    Label(screen, text="Item ID", width = 10).grid(column=1, row=0)
    Label(screen, text="Prod ID", width = 10).grid(column=2, row=0)
    Label(screen, text="Prod Name", width = 10).grid(column=3, row=0)
    Label(screen, text="Number", width = 10).grid(column=4, row=0)
    Label(screen, text="New Number", width = 10).grid(column=5, row=0)

    orderItems = queries.allOrderItemofOrder(oid)
    for i in range(len(orderItems)):
        Label(screen, text=oid).grid(column=0, row=i+1)
        Label(screen, text=orderItems[i]['iid']).grid(column=1, row=i+1)
        Label(screen, text=orderItems[i]['pid']).grid(column=2, row=i+1)
        Label(screen, text=orderItems[i]['pname']).grid(column=3, row=i+1)
        Label(screen, text=orderItems[i]['qty']).grid(column=4, row=i+1)
        orderItems[i]['qty'] = StringVar()
        Entry(screen, width=10, textvariable=orderItems[i]['qty']).grid(column=5, row=i+1)
        Button(screen, text="edit", width = 4, height = 2, command = lambda x=i : updateOrderItem(orderItems[x]['qty'].get(), orderItems[x]['iid'], oid, cid) ).grid(column=6, row=i+1)
        Button(screen, text="delete", width = 4, height = 2, command = lambda x=i : deleteOrderItem(orderItems[x]['iid'], oid, cid) ).grid(column=7, row=i+1)

    pid_pname = StringVar()
    product_number = StringVar()
    dic = {}
    productChoosen = ttk.Combobox(screen, width = 27, textvariable = pid_pname)
    products = queries.allProducts()
    pid_pnames = []
    for i in range(len(products)):
        pid_pnames.append(str(products[i]['pid']) + " " + products[i]['pname'] + "\t" + str(products[i]['price']))
        dic[ str(products[i]['pid']) + " " + products[i]['pname'] + "\t" + str(products[i]['price']) ] = products[i]['pid']
    productChoosen['value'] = pid_pnames
    productChoosen.grid(column=2, columnspan=3, row=len(orderItems)+1)
    productChoosen.current(0)

    Entry(screen, width=10, textvariable=product_number).grid(column=5, row=len(orderItems)+1)
    Button(screen, text = "ADD", width = 10, height = 2, command = lambda : insertOrderItem(oid, product_number.get(), dic[pid_pname.get()], cid)).grid(column=6, row = len(orderItems)+1)

    Button(screen, text = "BACK", width = 10, height = 2, command = lambda : CustomerOrders_screen(cid)).grid(column=0, row = len(orderItems)+2)

    screen.mainloop()

def insertOrderItem(oid, qty, pid, cid):
    if qty != "":
        queries.insertOrderItem(oid, qty, pid)
        OrderItems_screen(oid, cid)

def updateOrderItem(qty, iid, oid, cid):
    if qty != "":
        queries.updateOrderItem(iid, int(qty))
        if oid == -1:
            items_screen()
        else:
            OrderItems_screen(oid, cid)

def deleteOrderItem(iid, oid, cid):
    queries.deleteOrderItem(iid)
    if oid == -1:
        items_screen()
    else:
        OrderItems_screen(oid, cid)

def orders_screen():
    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("400x400")
    screen.title("Orders")

    Label(screen, text="ID", width = 5).grid(column=0, row=0)
    Label(screen, text="Date", width = 15).grid(column=1, row=0)
    Label(screen, text="C Name", width = 15).grid(column=2, row=0)

    orders = queries.allOrders()
    for i in range(len(orders)):
        Label(screen, text=orders[i]['oid']).grid(column=0, row=i+1)
        Label(screen, text=orders[i]['oDate']).grid(column=1, row=i+1)
        Label(screen, text=orders[i]['cname']).grid(column=2, row=i+1)
        Button(screen, text="items", width = 4, height = 2, command = lambda x=i : OrderItems_screen(orders[x]['oid'], -1) ).grid(column=3, row=i+1)
        Button(screen, text="delete", width = 4, height = 2, command = lambda x=i : deleteCustomerOrder(orders[x]['oid'], -1) ).grid(column=4, row=i+1)

    Button(screen, text = "BACK", width = 10, height = 2, command = lambda : home_screen()).grid(column=0, row = len(orders)+1)

    screen.mainloop()

def CustomerOrders_screen(cid):
    if cid == -1:
        orders_screen()

    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("400x400")
    screen.title("Customer Orders")

    Label(screen, text="ID", width = 5).grid(column=0, row=0)
    Label(screen, text="Date", width = 15).grid(column=1, row=0)
    Label(screen, text="C Name", width = 15).grid(column=2, row=0)

    customerOrders = queries.allorderOfCustomer(cid)
    for i in range(len(customerOrders)):
        Label(screen, text=customerOrders[i]['oid']).grid(column=0, row=i+1)
        Label(screen, text=customerOrders[i]['oDate']).grid(column=1, row=i+1)
        Label(screen, text=customerOrders[i]['cname']).grid(column=2, row=i+1)
        Button(screen, text="items", width = 4, height = 2, command = lambda x=i : OrderItems_screen(customerOrders[x]['oid'], cid) ).grid(column=3, row=i+1)
        Button(screen, text="delete", width = 4, height = 2, command = lambda x=i : deleteCustomerOrder(customerOrders[x]['oid'], cid) ).grid(column=4, row=i+1)

    Button(screen, text="ADD NEW ORDER", height = 2, command = lambda : insertOrder(cid) ).grid(columnspan=2, row=len(customerOrders)+1)

    Button(screen, text = "BACK", width = 10, height = 2, command = lambda : customers_screen()).grid(column=0, row = len(customerOrders)+2)

    screen.mainloop()

def insertOrder(cid):
    now = datetime.datetime.now()
    queries.insertOrder(now, cid)
    CustomerOrders_screen(cid)

def deleteCustomerOrder(oid, cid=-1):
    queries.deleteOrder(oid)
    if cid != -1:
        CustomerOrders_screen(cid)
    else:
        orders_screen()

def products_screen():
    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("600x400")
    screen.title("Products")

    Label(screen, text="ID", width = 5).grid(column=0, row=0)
    Label(screen, text="Name", width = 10).grid(column=1, row=0)
    Label(screen, text="Price", width = 10).grid(column=2, row=0)
    Label(screen, text="", width = 5).grid(column=3, row=0)
    Label(screen, text="New Name", width = 10).grid(column=4, row=0)
    Label(screen, text="New Price", width = 10).grid(column=5, row=0)

    products = queries.allProducts()
    for i in range(len(products)):
        Label(screen, text=products[i]['pid']).grid(column=0, row=i+1)
        Label(screen, text=products[i]['pname']).grid(column=1, row=i+1)
        Label(screen, text=products[i]['price']).grid(column=2, row=i+1)
        products[i]['newname'] = StringVar()
        products[i]['newprice'] = StringVar()
        Entry(screen, width=10, textvariable=products[i]['newname']).grid(column=4, row=i+1)
        Entry(screen, width=10, textvariable=products[i]['newprice']).grid(column=5, row=i+1)
        Button(screen, text="edit", width = 4, height = 2, command = lambda x=i: updateProduct(products[x]['pid'], products[x]['newname'].get(), products[x]['newprice'].get()) ).grid(column=6, row=i+1)
        Button(screen, text="delete", width = 4, height = 2, command = lambda x=i: deleteProduct(products[x]['pid']) ).grid(column=7, row=i+1)

    NewProductName = StringVar()
    NewProductPrice = StringVar()
    tk.Entry(screen, width = 15, textvariable = NewProductName).grid(column=1, row=len(products)+1)
    tk.Entry(screen, width = 15, textvariable = NewProductPrice).grid(column=2, row=len(products)+1)
    Button(screen, text="ADD", width = 4, height = 2, command = lambda : insertProduct(NewProductName.get(), NewProductPrice.get()) ).grid(column=3, row=len(products)+1)

    Button(screen, text = "BACK", width = 10, height = 2, command = lambda : home_screen()).grid(column=0, row = len(products)+2)

    screen.mainloop()

def updateProduct(pid, name, price):
    if name != "" or price != "":
        if price == "":
            price = -1
        else:
            price = int(price)
        queries.updateproduct(pid, name, price)
        products_screen()

def insertProduct(name, price):
    if name != "" and price != "":
        queries.insertProduct(name, int(price))
        products_screen()

def deleteProduct(id):
    queries.deleteProduct(id)
    products_screen()

def items_screen():
    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("600x400")
    screen.title("OrderItems")

    Label(screen, text="Order ID", width = 10).grid(column=0, row=0)
    Label(screen, text="Item ID", width = 10).grid(column=1, row=0)
    Label(screen, text="Prod ID", width = 10).grid(column=2, row=0)
    Label(screen, text="Prod Name", width = 10).grid(column=3, row=0)
    Label(screen, text="Number", width = 10).grid(column=4, row=0)
    Label(screen, text="New Number", width = 10).grid(column=5, row=0)

    Items = queries.allOrderItems()
    for i in range(len(Items)):
        Label(screen, text=Items[i]['oid']).grid(column=0, row=i+1)
        Label(screen, text=Items[i]['iid']).grid(column=1, row=i+1)
        Label(screen, text=Items[i]['pid']).grid(column=2, row=i+1)
        Label(screen, text=Items[i]['pname']).grid(column=3, row=i+1)
        Label(screen, text=Items[i]['qty']).grid(column=4, row=i+1)
        Items[i]['qty'] = StringVar()
        Entry(screen, width=10, textvariable=Items[i]['qty']).grid(column=5, row=i+1)
        Button(screen, text="edit", width = 4, height = 2, command = lambda x=i : updateOrderItem(Items[x]['qty'].get(), Items[x]['iid'], -1, -1) ).grid(column=6, row=i+1)
        Button(screen, text="delete", width = 4, height = 2, command = lambda x=i : deleteOrderItem(Items[x]['iid'], -1, -1) ).grid(column=7, row=i+1)

    Button(screen, text = "BACK", width = 10, height = 2, command = lambda : home_screen()).grid(column=0, row = len(Items)+2)

    screen.mainloop()


def home_screen():
    global screen
    try:
        screen.destroy()
    except:
        pass

    screen = tk.Tk()
    screen.geometry("200x250")
    screen.title("Home")

    Button(screen, text = "CUSTOMERS", width = 20, height = 2, command = lambda : customers_screen()).pack()

    Button(screen, text = "ORDERS", width = 20, height = 2, command = lambda : orders_screen()).pack()

    Button(screen, text = "ORDERITEMS", width = 20, height = 2, command = lambda : items_screen()).pack()

    Button(screen, text = "PRODUCTS", width = 20, height = 2, command = lambda : products_screen()).pack()

    Button(screen, text = "EXIT", width = 20, height = 2, command = lambda : exit()).pack()

    screen.mainloop()

home_screen()
