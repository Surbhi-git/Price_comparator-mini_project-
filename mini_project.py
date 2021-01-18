from tkinter import *
import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import datetime
import os
import time


root=Tk()
root.title("Price Comparator")


# price comparison code
def amazon(email,link,range):
    def send_email(email):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login("minip866@gmail.com","mini@project1")

        subject= "Hey! The prices are affordable"
        body = "Go and order now at https://www.amazon.ae/Samsung-Galaxy-Ultra-128GB-Version/dp/B084H8DSCZ/ref=sr_1_6?dchild=1&keywords=samsung+s20&qid=1599291913&sr=8-6"
        msg = f"Subject:{subject}\n\n\n\n{body}"

        server.sendmail("minip866@gmail.com",email,msg)
        print("email sent")
        server.quit()



    # url = "https://www.amazon.ae/Samsung-Galaxy-Ultra-128GB-Version/dp/B084H8DSCZ/ref=sr_1_6?dchild=1&keywords=samsung+s20&qid=1599291913&sr=8-6"

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

    def check_price_and_log(link):
        page = requests.get(link, headers=headers)

        bs = BeautifulSoup(page.content, 'html.parser')

        #print(bs.prettify().encode("utf-8"))

        product_title = bs.find(id = "productTitle").get_text()
        print(product_title.strip())

        product_price = bs.find(id="priceblock_ourprice").get_text()


        product_price = product_price[2:9]
        print(product_price)

        price_float = float(product_price.replace(";",""))
        print(price_float)

        file_exists = True

        if not os.path.exists("./price.csv"):
            file_exists = False

        with open("price.csv","a") as file:
            writer = csv.writer(file,lineterminator ="\n")
            fields = ["Timestamp","price"]
            
            if not file_exists:
                writer.writerow(fields)

            timestamp = f"{datetime.datetime.date(datetime.datetime.now())},{datetime.datetime.time(datetime.datetime.now())}"
            writer.writerow([timestamp, price_float])
            # print("wrote csv data")

        return price_float


    while True:
        price = check_price_and_log(link)
        if(float(price) <= float(range)):
            send_email(email)
            break
        time.sleep(43200)


# tkinter code starts
e1=Entry(root, width=30,borderwidth=2)
e2=Entry(root, width=30,borderwidth=2)
e3=Entry(root, width=30,borderwidth=2)
e1.grid(row=1, column=1,pady=15)
e2.grid(row=3, column=1,pady=7)
e3.grid(row=5, column=1,pady=15)


myLabel1 = Label(root, text="PRICE COMPARATOR", fg="maroon")
myLabel2 = Label(root, text="Enter your Email:  ")

myLabel3 = Label(root, text="Enter the link:  ")
myLabel4 = Label(root, text="Enter the range:  ")

myLabel1.grid(row=0,columnspan=2)
myLabel2.grid(row=1, column=0)
myLabel3.grid(row=3, column=0)
myLabel4.grid(row=5, column=0)


def open1():
    amazon(e1.get(),e2.get(),e3.get())
    lbl = Label(root,text="You will be notified!")
    lbl.grid(row=1, column=0)

myButton = Button(root, text="Submit", padx=20, pady=2, command=open1, fg="white", bg="green")
myButton.grid(row=10, column=0, columnspan=2,pady=15) 

root.mainloop()
