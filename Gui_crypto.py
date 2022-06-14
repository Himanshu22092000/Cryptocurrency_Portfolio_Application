
from tkinter import *
import customtkinter
from tkinter import messagebox
import json
import requests
import sqlite3
from PIL import Image, ImageTk  # <- import PIL for the images
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")   # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green") # Themes: blue (default), dark-blue, green
crypto = customtkinter.CTk()


# crypto.geometry("400x240")
crypto.title(" Cryptocurrency Portfolio Tracker")
#crypto.iconbitmap('crypto.ico')


con=sqlite3.connect('coin.db')
cursorObj=con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id integer primary key,symbol text, amount integer, price real) ")
con.commit()

# cursorObj.execute("insert into coin(symbol, amount , price) values('BTC',2,3250)")
# con.commit()
# cursorObj.execute("insert into coin(symbol, amount , price) values('ETH',10,350)")
# con.commit()
# cursorObj.execute("insert into coin(symbol, amount , price) values('USD',1,10.30)")
# con.commit()

def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

def my_potfolio():
   api_requset = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=USD&CMC_PRO_API_KEY=4685a0a7-64fe-45f7-8f48-aa9e0afb7ff2')
   api = json.loads(api_requset.content)

   cursorObj.execute("select* from coin")
   coins=cursorObj.fetchall()

   def font_color(number):
      if(number>0):
         return "green"
      elif(number<0):
         return "red"
      else:
         return "black"

   def insert_coin():
      cursorObj.execute("insert into coin(symbol, amount , price) values(?,?,?)",(symbol_txt.get(),amount_txt.get(),price_txt.get()))
      con.commit()
      messagebox.showinfo("Portfolio notification","Coin added succesfuly.!")
      reset()

   def update_coin():
      cursorObj.execute("update coin set symbol=?, amount=?, price=? where id=?",(symbol_update.get(),amount_update.get(),price_update.get(),coin_id.get()))
      con.commit()
      messagebox.showinfo("Portfolio notification","Coin updated succesfuly.!")
      reset()

   def delete_coin():
      cursorObj.execute("delete from coin where id=?",(id_delete.get()))
      con.commit()
      messagebox.showinfo("Portfolio notification","Coin deleted succesfuly.!")
      reset()

   def reset():
      for cell in crypto.winfo_children():
         cell.destroy()
      head() 
      app_header()
      my_potfolio()

   

   def head():

      def clear_all():
         cursorObj.execute("delete from coin")
         con.commit()

         messagebox.showinfo("Portfolio notification","databse cleared")
         reset()
         
      def close_app():
         crypto.destroy()

      menu=Menu(crypto)
      file_item=Menu(menu)
      file_item.add_command(label='clear all',command=clear_all)
      file_item.add_command(label='close app',command=close_app)
      menu.add_cascade(label="File",menu=file_item) 
      crypto.config(menu=menu)
      
   head()

   # coins = [{"symbol": "BTC", "amount_owned": 2, "price_per_coin": 3200},
   # {"symbol": "ETH", "amount_owned": 5, "price_per_coin": 20},
   # {"symbol": "USDC", "amount_owned": 10, "price_per_coin": 15},
   # {"symbol": "BNB", "amount_owned": 1, "price_per_coin": 500}]
   Total = 0
   row_no=1
   tCurrentV=0
   total_paid=0
   for i in range(0, 5):
      for coin in coins:
         if(api["data"][i]["symbol"] == coin[1]):
            Total_paid = coin[2]*coin[3]
            current_value = coin[2] *api["data"][i]["quote"]["USD"]["price"]
            P_L_per_coin = api["data"][i]["quote"]["USD"]["price"] -coin[3]
            Total_pl = coin[2]*P_L_per_coin
            tCurrentV+=current_value
            Total += Total_pl
            total_paid+=Total_paid
            print(api["data"][i]["name"]+" - "+api["data"][i]["symbol"])
            print("price: ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
            print("Total paid:", "${0:.2f}".format(Total_paid))
            print("Current value:", "${0:.2f}".format(current_value))
            print("Profit/loss per coin:", "${0:.2f}".format(P_L_per_coin))
            print("Total Profit/loss with coins:", "${0:.2f}".format(Total_pl))
            
            
            ID = Label(crypto, text=coin[0], bg="#CAF0F8", fg="black",font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            ID.grid(row=row_no, column=1, sticky=N+S+E+W)
            name = Label(crypto, text=api["data"][i]["name"], bg="#90E0EF", fg="black",font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            name.grid(row=row_no, column=2, sticky=N+S+E+W)
            price = Label(crypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#CAF0F8", fg="black",font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            price.grid(row=row_no, column=3, sticky=N+S+E+W)
            noCoin = Label(crypto, text=coin[2], bg="#90E0EF", fg="black",font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            noCoin.grid(row=row_no, column=4, sticky=N+S+E+W)
            tAmount = Label(crypto, text="${0:.2f}".format(Total_paid), bg="#CAF0F8", fg="black",font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            tAmount.grid(row=row_no, column=5, sticky=N+S+E+W)
            cValue = Label(crypto, text="${0:.2f}".format(current_value), bg="#90E0EF", fg="black",font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            cValue.grid(row=row_no, column=6, sticky=N+S+E+W)
            plCoin = Label(crypto, text="${0:.2f}".format(P_L_per_coin), bg="#CAF0F8", fg=font_color(P_L_per_coin),font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            plCoin.grid(row=row_no, column=7, sticky=N+S+E+W)
            TplCoin = Label(crypto, text="${0:.2f}".format(Total_pl), bg="#90E0EF", fg=font_color(Total_pl),font="Arial", padx="5",pady="5",borderwidth=2, relief="groove")
            TplCoin.grid(row=row_no, column=8, sticky=N+S+E+W)
            row_no+=1
   print("Grand total Profit/loss:", "${0:.2f}".format(Total))
   
   # fram 1----------------------------------------------------------------

   # crypto 
   # crypto.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
   # crypto.grid_columnconfigure(0, weight=1)
   # crypto.grid_columnconfigure(1, weight=1)
   # crypto.grid_rowconfigure(0, minsize=10)  # add empty row for spacing

   # # button_1 = customtkinter.CTkButton(master=crypto,  text="Add Folder", width=190, height=40,compound="right",)
   # # button_1.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")






   # edditing options------------------------
   symbol_txt = customtkinter.CTkEntry(master=crypto,placeholder_text="symbol(eg:ETH,BTC,..)",width=120,height=25,border_width=1, corner_radius=10)
   symbol_txt.grid(row=row_no+2, column=2)
   price_txt = customtkinter.CTkEntry(master=crypto,placeholder_text="price",width=120,height=25,border_width=1, corner_radius=10)
   price_txt.grid(row=row_no+2, column=3)
   amount_txt = customtkinter.CTkEntry(master=crypto,placeholder_text="number of coins",width=120,height=25,border_width=1, corner_radius=10)
   amount_txt.grid(row=row_no+2, column=4)
   add_coin = customtkinter.CTkButton(master=crypto,
                                 width=120,
                                 height=20,
                                 border_width=1,
                                 corner_radius=8,
                                 text="ADD COIN",
                                 command=insert_coin)

   # add_coin= Button(crypto, text="ADD COIN",command=insert_coin ,bg="#03045E", fg="white", font="Arial 15 bold", padx="5",pady="5",borderwidth=2, relief="groove")

   add_coin.grid(row=row_no+2, column=5, sticky=N+S+E+W)
   
   coin_id = customtkinter.CTkEntry(master=crypto,placeholder_text="please enter ID",width=120,height=25,border_width=1, corner_radius=10)
   coin_id.grid(row=row_no+3, column=1)
   symbol_update = customtkinter.CTkEntry(master=crypto,placeholder_text="symbol(eg:ETH,BTC,..)",width=120,height=25,border_width=1, corner_radius=10)
   symbol_update.grid(row=row_no+3, column=2)
   price_update = customtkinter.CTkEntry(master=crypto,placeholder_text="New price",width=120,height=25,border_width=1, corner_radius=10)
   price_update.grid(row=row_no+3, column=3)
   amount_update = customtkinter.CTkEntry(master=crypto,placeholder_text="number of coins",width=120,height=25,border_width=1, corner_radius=10)
   amount_update.grid(row=row_no+3, column=4)

   coin_update = customtkinter.CTkButton(master=crypto,
                                 width=120,
                                 height=10,
                                 border_width=1,
                                 corner_radius=8,
                                 text="UPDATE COIN",
                                 command=update_coin)

   # coin_update= Button(crypto, text="UPDATE",command=update_coin ,bg="#03045E", fg="white", font="Arial 15 bold", padx="5",pady="5",borderwidth=2, relief="groove")
   
   coin_update.grid(row=row_no+3, column=5, sticky=N+S+E+W)

   id_delete = customtkinter.CTkEntry(master=crypto,placeholder_text="please enter ID",width=120,height=25,border_width=1, corner_radius=10)
   id_delete.grid(row=row_no+4, column=1)
   coin_delete = customtkinter.CTkButton(master=crypto,
                                 width=120,
                                 height=10,
                                 border_width=1,
                                 corner_radius=8,
                                 text="DELETE COIN",
                                 command=delete_coin)
   # coin_delete= Button(crypto, text="DELETE",command=delete_coin ,bg="#03045E", fg="white", font="Arial 15 bold", padx="5",pady="5",borderwidth=2, relief="groove")
   coin_delete.grid(row=row_no+4, column=5, sticky=N+S+E+W)


   TplCoin = Label(crypto, text="${0:.2f}".format(total_paid), bg="#F5FCFF", fg="black",font="Arial 15 bold", padx="5",pady="5",borderwidth=2, relief="groove")
   TplCoin.grid(row=row_no, column=5, sticky=N+S+E+W)
   TplCoin = Label(crypto, text="${0:.2f}".format(tCurrentV), bg="#F5FCFF", fg="black",font="Arial 15 bold", padx="5",pady="5",borderwidth=2, relief="groove")
   TplCoin.grid(row=row_no, column=6, sticky=N+S+E+W)
   TplCoin = Label(crypto, text="${0:.2f}".format(Total), bg="#F5FCFF", fg=font_color(Total),font="Arial 15 bold", padx="5",pady="5",borderwidth=2, relief="groove")
   TplCoin.grid(row=row_no, column=8, sticky=N+S+E+W)
   row_no += 1
   api=""

   Refresh = customtkinter.CTkButton(master=crypto,
                                 width=120,
                                 height=10,
                                 border_width=1,
                                 corner_radius=8,
                                 text="Refresh",
                                 command=my_potfolio)

   # Refresh= Button(crypto, text="Refresh",command=my_potfolio ,bg="#03045E", fg="white", font="elephant 15", padx="5",pady="5",borderwidth=2, relief="groove")

   Refresh.grid(row=row_no+2, column=8, sticky=N+S+E+W)
      

def app_header():

   ID = customtkinter.CTkLabel(crypto, text="ID",width=120,height=25,text_font=("elephant",15))
   ID.grid(row=0, column=1, sticky=N+S+E+W)
   name = customtkinter.CTkLabel(crypto, text="Coin Name",width=120,height=25,text_font=("elephant",15))
   name.grid(row=0, column=2, sticky=N+S+E+W)
   price = customtkinter.CTkLabel(crypto, text="Price",width=120,height=25,text_font=("elephant",15))
   price.grid(row=0, column=3, sticky=N+S+E+W)
   noCoin = customtkinter.CTkLabel(crypto, text="Coin owned",width=120,height=25,text_font=("elephant",15))
   noCoin.grid(row=0, column=4, sticky=N+S+E+W)
   tAmount = customtkinter.CTkLabel(crypto, text="Total paid",width=120,height=25,text_font=("elephant",15))
   tAmount.grid(row=0, column=5, sticky=N+S+E+W)
   cValue = customtkinter.CTkLabel(crypto, text="Current value",width=120,height=25,text_font=("elephant",15))
   cValue.grid(row=0, column=6, sticky=N+S+E+W)
   plCoin = customtkinter.CTkLabel(crypto, text="P/L per coin",width=120,height=25,text_font=("elephant",15))
   plCoin.grid(row=0, column=7, sticky=N+S+E+W)
   TplCoin = customtkinter.CTkLabel(crypto, text="Total P/L ",width=120,height=25,text_font=("elephant",15))
   TplCoin.grid(row=0, column=8, sticky=N+S+E+W)



app_header()
my_potfolio()


crypto.mainloop()

print("created by himanshu jadoun")
cursorObj.close()
con.close()
