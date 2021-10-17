import requests
import tkinter as tk
from tkinter import messagebox, ttk
import os
from csv import DictReader, DictWriter



################################### GUI ##########################################

# Main window 
win = tk.Tk()
win.geometry("410x165")
win.title("Message Sender")
win.resizable(0,0)


# Labels
phone_label = ttk.Label(win, text="Enter Phone Number: ")
phone_label.grid(row=0, column=0, padx=5, pady=8)

message_label = ttk.Label(win, text="Enter Message: ")
message_label.grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)

message_time_label = ttk.Label(win, text="Select Message Count: ")
message_time_label.grid(row=2, column=0, padx=5, pady=3, sticky=tk.W)


# Entery Box 
phone_entry = ttk.Entry(win, width=30)
phone_entry.grid(row=0, column=1, padx=5)
phone_entry.focus()

message_entry = ttk.Entry(win, width=30)
message_entry.grid(row=1, column=1, padx=5)
    

# Spin box 
values = (1,2,3,4,5,10,20,50,100)
spin_box = tk.Spinbox(win, values=values, width=28, relief=tk.FLAT)
spin_box.grid(row=2, column=1)


# Buttons
space = ttk.Label(win, text="")
space.grid(row=3, column=0, pady=8)

send_btn= ttk.Button(win, text="Send")
send_btn.grid(row=4,column=1, pady=5, padx=5, sticky=tk.E)

exit_btn= ttk.Button(win, text="Exit")
exit_btn.grid(row=4,column=2) 


# Check Button
theme_var = tk.IntVar()
theme = tk.Checkbutton(win, text= "Dark Theme", relief=tk.FLAT, variable=theme_var)
theme.grid(sticky=tk.W, row=4, column=0, padx=2)


###################################### Funcationality ######################################

######## Funcation's ##########

# CSV Creator Funcation
def Csv_creator(file_name, field_names, default_dict):
    with open(file_name, 'w', newline='') as r:
        file_writer = DictWriter(r, fieldnames=field_names)
        file_writer.writeheader()
        file_writer.writerow(default_dict)


# File existness Creator Funcation
def File_existness(file_name, field_names, default_dict):
    if os.path.exists(file_name):
        if os.stat(file_name).st_size==0:
            Csv_creator(file_name, field_names, default_dict)
    else:
        Csv_creator(file_name, field_names, default_dict)


# Theme Changer Funcation 
def Theme_changer(file_name, field_names, chekcbutton, *args):
    with open(file_name, 'r') as rf:
        file_reader = DictReader(rf, fieldnames=field_names)
        next(file_reader)
        for value in file_reader:
            if value['Theme value']=='1':
                chekcbutton.select()
                bg_color = "Black"
                fg_color = "White"
                break
            else:
                bg_color = "White"
                fg_color = "Black"
                break
    for arg in args:
        if type(arg)==tk.Checkbutton and bg_color=='Black':
            arg.config(background='Black', foreground='Dark gray')
        else:
            try:
                arg.config(background=bg_color, foreground=fg_color)
            except tk.TclError:
                arg.config(background=bg_color)
            except:
                messagebox.showerror("New Error", "Tell to Rihan Its a new error")


# Value Updater 
def Value_updater(file_name, field_names, key, updated_value):
    with open(file_name, 'r') as data:
        reader = DictReader(data, fieldnames=field_names)
        data_list = []
        for i in reader:
            data_list.append(i)
        data_list[1][key]=updated_value
    with open(file_name, 'w', newline="") as data:
        writer = DictWriter(data, fieldnames=field_names)
        writer.writerows(data_list)


default_data = {"Theme value": 0}
File_existness("Message Sender.csv", ["Theme value"], default_data)


######## Buttons ########### 

# Theme Button
def theme_button():
    Value_updater("Message Sender.csv", ["Theme value"], 'Theme value', theme_var.get())
    Theme_changer(
        "Message Sender.csv", ["Theme value"], theme, phone_label, message_label, space, theme,
        win, message_time_label
    )


# Send Buttton 
def send_button(): 
    number = phone_entry.get()
    message = message_entry.get()
    count = spin_box.get()
    if number=="" or message=="" or count=="":
        if number=="" and message=="":
                messagebox.showerror("Empty field", "Please Enter Mobile Number and Message ")
        else:        
            if number=="":
                    messagebox.showerror("Empty field", "Please Enter Mobile Number ")
            else:
                if count=="":
                    messagebox.showerror("Empty field", "Please enter Message Count ")
                else:
                    messagebox.showerror("Empty field", "Please Enter Message ")
        phone_entry.focus_set()  
    else:
        if int(count)>150:
            messagebox.showinfo("Failed", "Can't Send More Than 150 Message's ")
        else:
            if number.isalpha():
                messagebox.showerror("Invalid", "Invalid Mobile Number ") 
            else:
                try:
                        
                    message_sent = 0
                    for i in range(0, int(count)):
                    #     url = "https://www.fast2sms.com/dev/bulk"
                    #     api = "b4OD5dRG2lNTo9SpcjPhCJKaq8ztAkxYHZQ3VByfieE6smIWU1xQlug3rsPv0bBF8Iqyf9AiHnaOjdmz"

                    #     querystring ={
                    #         "authorization": api,
                    #         "sender_id":"FST2SMS",
                    #         "message": message,
                    #         "language": "english",
                    #         "route": "p",
                    #         "numbers": int(number)
                    #     }
                    #     headers = {
                    #         'cache-control': 'no-cache'   
                    #     }
                    #     requests.request("GET",url,headers=headers,params=querystring)
                        message_sent = message_sent+1
                    messagebox.showinfo("Status", f"{message_sent} Message Has Been Sent Successfully")
                except:
                    messagebox.showerror("Connection Error", "Unable To Connect, Check Your Connection ")


# Exit Button 
def exit_button():
    result= messagebox.askyesno('Exit', "Do You Want To Exit ??")
    if result== True:
        win.destroy()
    else:
        pass


# Binding Buttons 
theme.config(command=theme_button)
send_btn.config(command=send_button)
exit_btn.config(command=exit_button)


# Activating Theme 
Theme_changer(
    "Message Sender.csv", ["Theme value"], theme, phone_label, message_label, space, theme,
    win, message_time_label
)





win.mainloop()
