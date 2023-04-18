
import mysql.connector as sqltor
import random
from tkinter import *

def exit1(root):
    root.destroy()
    
def content(n1, n2):
    global username
    username = str(n1.get())
    global password
    password = str(n2.get())
    
    
def start_menu():
    root = Tk()
    root.title("Courier Service Mangement System")

    frame1 = Frame(root, bg = "black", height = 300, width = 1600)
    frame1.pack(padx = 0, pady = 0)
    frame1.pack_propagate(False)

    welcome = Label(frame1, text = "Welcome to\n Arch's Courier Service!",\
              font = ("Calisto MT", 50), fg = "white", justify = "center",\
              bg = "black")
    welcome.pack(side = BOTTOM)

    names = Label(frame1, text = "By Nikita Bhatia (XII)", justify = "center",\
                  font = ("Calisto MT",10) , bg = "black", fg = "white")
    names.pack(side = TOP)

    pic1 = PhotoImage(file =  "img1.png", height = 500)
    imgl  = Label(root, image = pic1)
    imgl.pack(pady = 10, anchor = "w")

    login1 = Button(root, text = "Login", command = lambda: login(root),\
                    font = 10 , width = 9, bg = "black", fg = "white")
    signup1 = Button(root, text = "Signup", command = lambda: signup(root),\
                     font = 10, width = 9, bg = "black", fg = "white")
    exit2 = Button(root, text = "Exit", command = lambda: exit1(root), \
                   font = 10, width = 9, bg = "black", fg = "white")
    
    login1.place(x = 1000, y = 500)
    signup1.place(x = 1150, y = 500)
    exit2.place(x = 1300,y = 500)

    frame3 = Frame(root, bg = "black", width = 500)
    frame3.place(x = 950, y =450)

    frame4 = Frame(root, bg = "black", width = 500)
    frame4.place(x = 950, y =590)

    root.configure(bg = "white")
    root.state("zoomed")
    root.mainloop()

def login(root):
    mycon = sqltor.connect(host = "localhost", user = "root", \
                           password = "mysql", database = "courier_system")
    mycursor = mycon.cursor()
    
    query_1 = 'select username, password from customers'
    mycursor.execute(query_1)
    
    records = mycursor.fetchall()
    
    usernames = []
    passwords = []
    
    for i, j in records:
        usernames.append(i)
        passwords.append(j)
    
    mycon.close()
    
    user1 = Label(root, text = "Username", fg = "black", font =15)
    user = Entry(root, width = 50, borderwidth = 5, bg = "black", fg ="white")
    pass1 = Label(root, text = "Password", fg = "black", font = 15)
    pass2 = Entry(root, width = 50, borderwidth = 5, bg = "black", fg ="white") 
    user1.place(x = 1000, y = 605)
    
    user.place(x = 1000, y = 630)
    
    pass1.place(x = 1000, y = 660)
    
    pass2.place(x = 1000, y = 685)
    
    go = Button(root, text = "Go", bg = "black", fg = "white",\
                command = lambda: [content(user, pass2), exit1(root)])
        
    go.place(x = 1000, y = 730)
    root.mainloop()
    
    if username in usernames:
        position = usernames.index(username)
        
        if password == passwords[position]:
            successful_login(username)
        
        else:
            print("Incorrect password!")
            
            choice = int(input("Press 1 to return to home page: "))
            
            start_menu()
                
    else:
        print("No such account exists")
        print("Returning to home page...")
        start_menu()

        
def signup(root):
    exit1(root)
    
    mycon = sqltor.connect(host = "localhost", user = "root", \
                           password = "mysql", database = "courier_system")
    mycursor = mycon.cursor()
    
    print("Please enter the following details to create a new account:")
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    name = input("Enter your name: ")
    email = input("Enter email: ")
    contact = input("Enter contact number: ")
    address = input("Enter your address: ")
    
    val = (username, password, name, email, contact, address, "NULL")
    query = "insert into customers values{}".format(val)
    mycursor.execute(query)
    
    mycon.commit()
    mycon.close()
    
    successful_login(username)

def successful_login(username):
    mycon = sqltor.connect(host = "localhost", user = "root",\
                           password = "mysql", database = "courier_system")
    mycursor = mycon.cursor()
    
    query = "select username, order_no from customers"
    mycursor.execute(query)
    
    records = mycursor.fetchall()
    
    order = []
    
    for i,j in records:
        if i == username and j not in ["NULL", None]:
            order.append(j)
    mycon.close()

    print("You have successfully logged in to your account!!!")
    
    if len(order) != 0:
        print("You already have an existing order\n")
        print("                                    1. Make a new order")
        print("                                    2. Delete the existing order.")
        print("                                    3. View details about the existing order")
        print("                                    4. Home page")
        
        choice = int(input("enter your choice: "))
        
        if choice == 1:
            new_order(username)
        elif choice == 2:
            delete_order(order, username)
        elif choice == 3:
            view_order(order)
        elif choice == 4:
            start_menu()
        else:
            print("Invalid choice!!!")
            print("Returning to home page...")
            start_menu()
            
    else:
        print("You don't have any existing orders!\n")
        print("                                   1. Make a new order")
        print("                                   2. Home page")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            new_order(username)
        elif choice == 2:
            start_menu()
        else:
            print("Invalid choice!!!")
            print("Returning to home page...")
            start_menu()


def new_order(username):
    from datetime import date, timedelta
    mycon = sqltor.connect(host = "localhost", user = "root",\
                           password = "mysql", database = "courier_system")
    mycursor = mycon.cursor()
    
    query1 = "select * from customers"
    mycursor.execute(query1)
    
    records = mycursor.fetchall()
    
    info = None
    for i in records:
        if i[0] == username:
            info = i
            break
    info = list(info)    
    query2 = "select * from price"
    mycursor.execute(query2)
    
    prices = mycursor.fetchall()
     
    receiving_address = input("Enter receiving address: ")
    weight = int(input("Enter order weight: "))
    
    print("Your order will be priced according to the following details: ")
    for i in prices:
        print("\t", i)
        
    print()
    
    set_price = 0
    
    for a, b in prices:
        if weight <= a:
            set_price = b
            break
    else:
        length = len(prices)
        max_price = prices[length-1][1]
        set_price = max_price
        
    
    print("Here are a few payment modes available: ")
    print("                                      1. Cash on delivery")
    print("                                      2. Via debit card")
    print("                                      3. Credit card")
    
    pay = int(input("Enter your choice: "))
    
    if pay == 1:
        print("Proceeding your order as payment mode COD...")
        bill_no = str(random.randint(1,9))+str(random.randint(1,9))+\
        str(random.randint(1,9))+str(random.randint(1,9))
        
        name = info[2]
        email = info[3]
        date1 = str(date.today())
        expected = str(date.today() + timedelta(days = 10))
        mode = "Cash on delivery"
        status = "Not paid"
        
        values1 = (bill_no, name, email, date1, expected ,mode,\
                   status, weight, receiving_address)
        
        query3 = "insert into orders values{}".format(values1)
        mycursor.execute(query3)
        mycon.commit()
        
        info[-1] = bill_no
        info = tuple(info)
        query4 = 'insert into customers values{}'.format(info)
        mycursor.execute(query4)
        mycon.commit()
        mycon.close()
        
        print("Your order is confirmed!")
        print("Returning to homepage...")
        start_menu()
        
    elif pay == 2 or pay == 3:
        card = input("Enter card number, CVV: ")
        print("Price to pay:", set_price)
        
        choice = input("Press Y to continue payment and N to cancel order: ")
        
        if choice.lower() == "y":
            print("Payment successful!!!")
            mode = "Cash on delivery"
            status = "Not paid"
            
            bill_no = str(random.randint(1,9))+str(random.randint(1,9))+\
                str(random.randint(1,9))+str(random.randint(1,9))
        
            name = info[2]
            email = info[3]
            date1 = str(date.today())
            expected = str(date.today() + timedelta(days = 10))
            mode = "Cash on delivery"
            status = "Not paid"
            
            values1 = (bill_no, name, email, date1, expected ,mode,\
                       status, weight, receiving_address)
            
            query3 = "insert into orders values{}".format(values1)
            mycursor.execute(query3)
            mycon.commit()
        
            info[-1] = bill_no
            info = tuple(info)
            query4 = 'insert into customers values{}'.format(info)
            mycursor.execute(query4)
            mycon.commit()
            mycon.close()
            print("Your order is confirmed!")
            
            print("Returning to home page...")
            
            start_menu()
            
        else:
            print("Cancelling order...")
            print("Returning to home page...")
            mycon.close()
            start_menu()
    else:
        print("Invalid choice!!")
        print("Returning to home page...")
        mycon.close()
        start_menu()

        
def delete_order(order, username):
    mycon = sqltor.connect(host = "localhost", user = "root",\
                           password = "mysql", database = "courier_system")
    mycursor = mycon.cursor()
    print("Here are the order numbers of the orders that you have already placed:")
    
    count = 1
    for i in order:
        print("\t\t\t",count,".",  i)
        count += 1
        
    choice = int(input("Enter your choice: "))
    
    if choice > len(order):
        print("Invalid choice!")
        print("Returning to home page...")
        mycon.close()
        start_menu()
    else:
        order_no = order[choice - 1]
        query1 = 'delete from orders where bill_number = {}'.format(order_no)
        query2 = 'delete from customers where username = "{}"\
            and order_no = "{}"'.format(username, order_no)
        mycursor.execute(query1)
        mycursor.execute(query2)
        
        mycon.commit()
        mycon.close()
        print("Order deleted!!!")
        print("Returning to home page...")
        start_menu()
        
        

def view_order(orders):
    from datetime import date
    mycon = sqltor.connect(host = "localhost", user = "root",\
                           password = "mysql", database = "courier_system")
    mycursor = mycon.cursor()
    
    print("Here are the order numbers of the orders that you have already placed:  ")
    
    choice = 1
    for i in orders:
        print("\t\t\t\t", choice, ".", i)
        choice +=1
        
    choose = int(input("Enter an order_no to view its details: "))
    
    if choose > len(orders):
        print("Invalid choice!!!")
        print("Returning to home page...")
    else:
        order_no = orders[choose - 1]

        query1='select * from orders where bill_number = "{}"'.format(order_no)
        mycursor.execute(query1)
        
        data = list(mycursor.fetchone())
        
        info = {}
        headings = ["Bill number", "Customer name", "Email", "Order_date",\
                "Expected delivery date","Payment mode", "Payment status",\
                        "Order weight", "Receiving address", "Price"]

        if data[4] < str(date.today()):
            data[6] = "Paid"
            
            
        for i in range(len(data)):
            key = headings[i]
            value = data[i]
            info[key] = value
            
        query2 = "select * from price"
        mycursor.execute(query2)
    
        prices = mycursor.fetchall()
        set_price = 0
        weight = info["Order weight"]
        for a, b in prices:
            if weight <= a:
                set_price = b
                break
        else:
            length = len(prices)
            max_price = prices[length-1][1]
            set_price = max_price
        
        info["Price"] = set_price
        
        print()
        print("Here are your order details: ")
        
        for i in info:
            print(i, ":", info[i])
            
        print("Printed all the order details...")
        print("                                 1. View other orders")
        print("                                 2. Home page")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            view_order(orders)
        elif choice == 2:
            mycon.close()
            start_menu()
        else:
            print("Invalid choice!!!")
            print("Returning to home page...")
            mycon.close()
            start_menu()

username = ""
password = ""
start_menu()

