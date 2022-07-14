import tkinter
from tkinter import messagebox
import csv
#from time import sleep

flag = 0
# Read the users database from a text file in a dictionary #
# Taking into considerations that each field in the database file #
# has constant number of chars #
def read_database():
    global userDataBase
    userDataBase = {}
    fileObj = open("Database.txt","r")
    reader = csv.reader(fileObj)
    header = next(reader)
    for row in reader:
        userDataBase[row[0]] = {'Name':row[1],'Password':row[2],'Balance':row[3],'State':row[4].rstrip()} 
    fileObj.close()
    #print(userDataBase)

########################################################################################################################################################     
#                                                       Display Main Window                                                                            #
# ######################################################################################################################################################  
def display_main_window():
    global flag
    if flag == 1:
        options_window.destroy()
    global main_window
    # Main Window #
    main_window = tkinter.Tk()
    main_window.title("ATM")
    main_window.geometry("400x200")
    main_window.resizable(False,False)
    main_window.configure(background = "lavender")

    # Entries #
    accountNumEntry = tkinter.Entry(main_window, width = 20)
    accountNumEntry.place(x = 100, y = 0)

    # Labels #
    accountNumLabel = tkinter.Label(main_window, text = "Account Number:", background="lavender")
    accountNumLabel.place(x = 0, y = 0)


    # Buttons #
    loginButton = tkinter.Button(main_window, height = 3, width = 14, text = "Enter", command=lambda:check_account_num(accountNumEntry.get()))
    loginButton.place(x = 20, y = 80)

    closeMainWindowButton = tkinter.Button(main_window, height = 3, width = 14, text = "Quit", command=quit)
    closeMainWindowButton.place(x = 150, y = 80)
    flag = 1
    main_window.mainloop()

########################################################################################################################################################     
#                                                       Check the account number                                                                       #
# ######################################################################################################################################################  
def check_account_num(accountNumEntry):
    global accountNum
    if accountNumEntry in userDataBase:
        accountNum = accountNumEntry
        display_top_window()
    else:
        messagebox.showerror("Error", "Invalid account number", parent = main_window)


########################################################################################################################################################     
#                                                          Welcome Window                                                                              #
# ######################################################################################################################################################  
def display_top_window():
    global top_level_window
    top_level_window = tkinter.Tk()
    top_level_window.geometry("300x200")
    top_level_window.resizable(False, False)
    top_level_window.title("Welcome")
    top_level_window.configure(background="lavender")

    welcomeMsg = tkinter.Message(top_level_window, text="Welcome " + userDataBase[accountNum]['Name'], background="lavender")
    welcomeMsg.place(x = 0, y = 0)

    pinEntry = tkinter.Entry(top_level_window, width = 4, show = '*')
    pinEntry.place(x = 100, y = 70)

    pinLabel = tkinter.Label(top_level_window, text = "Enter your PIN:", background="lavender")
    pinLabel.place(x = 0, y = 70)

    pinButton = tkinter.Button(top_level_window, height = 3, width = 14, text = "Enter", command= lambda: pinCheck(pinEntry.get()))
    pinButton.place(x = 60, y = 110)
    top_level_window.mainloop()


########################################################################################################################################################     
#                                                       Checking the user PIN                                                                          #
# ######################################################################################################################################################  
def pinCheck(pinEntry):
    global errCount
    global userDataBase
    if (pinEntry == userDataBase[accountNum]['Password']) and (userDataBase[accountNum]['State'] == 'Unblocked'):
        errCount = 0
        main_window.destroy()
        top_level_window.destroy()
        display_options_window()
    elif errCount == 3 or userDataBase[accountNum]['State'] == 'Blocked':
        errCount = 0
        messagebox.showerror("Error", "You account has been blocked.\nPlease visit the branch", parent = top_level_window)
        top_level_window.destroy()
        # Mark that account as blocked state #
        userDataBase[accountNum]['State'] = 'Blocked'
        update_data_base()
    else:
        errCount +=1
        messagebox.showerror("Error", "Invalid password.\nPlease try again", parent = top_level_window)


########################################################################################################################################################     
#                                                          Home page Window                                                                            #
# ######################################################################################################################################################   
def display_options_window():
    global options_window
    options_window = tkinter.Tk()
    options_window.title("ATM")
    options_window.geometry("500x330")
    options_window.resizable(False,False)
    options_window.configure(background = "lavender")
    
    welcomeLabel = tkinter.Label(options_window, text="Welcome " + userDataBase[accountNum]['Name'], background="lavender")
    welcomeLabel2 = tkinter.Label(options_window, text="Please Choose the operation you want", background="lavender")
    welcomeLabel.place(x = 0, y = 0)
    welcomeLabel2.place(x = 0, y = 20)    

    cashWithdrawBtn = tkinter.Button(options_window, text = "Cash Withdraw", command=cash_withdraw_window, height = 3, width = 14)
    cashWithdrawBtn.place(x = 60, y = 60)

    balanceInquiryBtn = tkinter.Button(options_window, text = "Balance Inquiry", command=balance_inquiry, height = 3, width = 14)
    balanceInquiryBtn.place(x = 60, y = 140)

    passChangeBtn = tkinter.Button(options_window, text = "Password Change", command=password_change, height = 3, width = 14)
    passChangeBtn.place(x = 60, y = 230)

    fawryServiceBtn = tkinter.Button(options_window, text = "Fawry Service", command=fawry_service, height = 3, width = 14)
    fawryServiceBtn.place(x = 330, y = 60)

    logOutBtn = tkinter.Button(options_window, text = "Log Out", command=display_main_window, height = 3, width = 14)
    logOutBtn.place(x = 330, y = 140)

    exitBtn = tkinter.Button(options_window, text = "Exit", command=lambda:close_window(options_window), height = 3, width = 14)
    exitBtn.place(x = 330, y = 230)

    options_window.mainloop()

########################################################################################################################################################     
#                                                       Cash Withdraw Window                                                                           #
# ######################################################################################################################################################  
def cash_withdraw_window():
    global cashWithdraw_window
    cashWithdraw_window = tkinter.Tk()
    cashWithdraw_window.title("Cash Withdraw")
    cashWithdraw_window.geometry("400x200")
    cashWithdraw_window.resizable(False,False)
    cashWithdraw_window.configure(background = "lavender")

    cashWithdrawLabel = tkinter.Label(cashWithdraw_window, text = "Enter the desired amount to withdraw: ", background="lavender")
    cashWithdrawLabel.place(x = 0, y = 0)

    cashWithdrawEntry = tkinter.Entry(cashWithdraw_window, width = 10)
    cashWithdrawEntry.place(x = 220, y = 0)
    # Will give error in case of not entering anything in the entry #
    cashWithdrawBtn = tkinter.Button(cashWithdraw_window, text = "Withdraw", command=lambda: cash_withdraw(cashWithdrawEntry.get()), height = 3, width = 14)
    cashWithdrawBtn.place(x = 100, y = 50)

########################################################################################################################################################     
#                                                       Function to check for the entered amount                                                       #
# ###################################################################################################################################################### 
def cash_withdraw(cashToWithdraw):
    read_database()
    oldBalance = userDataBase[accountNum]['Balance']
    cashToWithdraw = cashToWithdraw.lower()
    if not(cashToWithdraw.islower()):
        if len(cashToWithdraw) > 0 and int(cashToWithdraw) > 0:
            if int(cashToWithdraw) <= int(oldBalance):
                if int(cashToWithdraw) <= 5000:
                    if int(cashToWithdraw) % 100 == 0:
                        ATM_Actuator_Out(int(cashToWithdraw))
                        #update the balance#
                        userDataBase[accountNum]['Balance'] = int(oldBalance) - int(cashToWithdraw)
                        update_data_base()
                        messagebox.showinfo("Thank You", "Thank You!", parent = options_window)
                        cashWithdraw_window.destroy()
                    else:
                        messagebox.showerror("Error", "Enter multiples of 100 only. Please Try again", parent = cashWithdraw_window) 
                else:
                    messagebox.showerror("Error", "Maximum amount is 5000. Please Try again", parent = cashWithdraw_window) 
            else:
                messagebox.showerror("Error", "No sufficient balance", parent = options_window)
                cashWithdraw_window.destroy()
        else:
            messagebox.showerror("Error", "Enter a valid amount.\nPlease try again", parent = cashWithdraw_window)
    else:
        messagebox.showerror("Error", "Enter a valid amount.\nPlease try again", parent = cashWithdraw_window)

########################################################################################################################################################     
#                                                       Function to withdraw money                                                                     #
# ###################################################################################################################################################### 
def ATM_Actuator_Out(cashToWithdraw):
    pass




########################################################################################################################################################     
#                                                      Balance Inquiry Window                                                                          #
# ######################################################################################################################################################  
def balance_inquiry():
    read_database()
    inquiry_window = tkinter.Tk()
    inquiry_window.title("Balance Inquiry")
    inquiry_window.geometry("400x200")
    inquiry_window.resizable(False,False)
    inquiry_window.configure(background = "lavender")

    nameLabel = tkinter.Label(inquiry_window, text = "Full Name: " + userDataBase[accountNum]['Name'], background="lavender")
    nameLabel.place(x = 0, y = 0)
    balanceLabel = tkinter.Label(inquiry_window, text = "Balance: " + userDataBase[accountNum]['Balance'], background="lavender")
    balanceLabel.place(x = 0, y = 30)

    exitInquiryBtn = tkinter.Button(inquiry_window, text = "Ok", command=lambda: close_window(inquiry_window), height = 3, width = 14)
    exitInquiryBtn.place(x = 150, y = 100)


########################################################################################################################################################     
#                                                     Password Change Window                                                                           #
# ######################################################################################################################################################  
def password_change():
    global passChange_window
    passChange_window = tkinter.Tk()
    passChange_window.title("Passowrd Change")
    passChange_window.geometry("400x200")
    passChange_window.resizable(False,False)
    passChange_window.configure(background = "lavender")

    newPassLabel = tkinter.Label(passChange_window, text = "Enter the new password: ", background="lavender")
    newPassLabel.place(x = 0, y = 20)
    newPassEntry = tkinter.Entry(passChange_window, width = 4, show = '*')
    newPassEntry.place(x = 160, y = 20)

    confirmNewPassLabel = tkinter.Label(passChange_window, text = "Confirm the new password: ", background="lavender")
    confirmNewPassLabel.place(x = 0, y = 50)
    confirmNewPassEntry = tkinter.Entry(passChange_window, width = 4, show = '*')
    confirmNewPassEntry.place(x = 160, y = 50)

    passChangeBtn = tkinter.Button(passChange_window, text = "Enter", command=lambda:check_new_pass(newPassEntry.get(), confirmNewPassEntry.get()), height = 3, width = 14)
    passChangeBtn.place(x = 50, y = 100)

    closePassChangeBtn = tkinter.Button(passChange_window, text = "Close", command = lambda: close_window(passChange_window), height = 3, width = 14)
    closePassChangeBtn.place(x = 200, y = 100)

    
    passChange_window.mainloop()




########################################################################################################################################################     
#                                                      Fawry Service Window                                                                            #
# ######################################################################################################################################################  
def fawry_service():
    global fawry_window
    fawry_window = tkinter.Tk()
    fawry_window.title("Phone Recharge")
    fawry_window.geometry("400x300")
    fawry_window.resizable(False,False)
    fawry_window.configure(background = "lavender")

    rechargeLabel = tkinter.Label(fawry_window, text = "Choose your service provider:", background="lavender")
    rechargeLabel.place(x = 0, y = 0)
 
    orangeBtn = tkinter.Button(fawry_window, text = "Orange Recharge", command = lambda:recharge_service_window("+2012"), height = 3, width = 14)
    orangeBtn.place(x = 30, y = 80) 

    etislatBtn = tkinter.Button(fawry_window, text = "Etislat Recharge", command = lambda:recharge_service_window("+2011"), height = 3, width = 14)
    etislatBtn.place(x = 230, y = 80) 

    vodafoneBtn = tkinter.Button(fawry_window, text = "Vodafone Recharge", command = lambda:recharge_service_window("+2010"), height = 3, width = 14)
    vodafoneBtn.place(x = 30, y = 200) 

    weBtn = tkinter.Button(fawry_window, text = "WE Recharge", command = lambda:recharge_service_window("+2015"), height = 3, width = 14)
    weBtn.place(x = 230, y = 200) 

########################################################################################################################################################     
#                                                    Recharge window                                                                                   #
# ###################################################################################################################################################### 
def recharge_service_window(startingNumber):
    global recharge_window
    recharge_window = tkinter.Tk()
    recharge_window.title("Phone Recharge")
    recharge_window.geometry("400x300")
    recharge_window.resizable(False,False)
    recharge_window.configure(background = "lavender")

    phoneLabel = tkinter.Label(recharge_window, text = "Enter your phone number: ", background="lavender")
    phoneLabel.place(x = 0, y = 20)

    phoneEntry = tkinter.Entry(recharge_window, width = 20)
    phoneEntry.insert(0, startingNumber)
    phoneEntry.place(x = 180, y = 20) 

    amountLabel = tkinter.Label(recharge_window, text = "Enter the amount to recharge: ", background="lavender")
    amountLabel.place(x = 0, y = 50)

    amountEntry = tkinter.Entry(recharge_window, width = 20)
    amountEntry.place(x = 180, y = 50) 

    rechargeBtn = tkinter.Button(recharge_window, text = "Recharge", command = lambda: recharge(amountEntry.get(),phoneEntry.get()), height = 3, width = 14)
    rechargeBtn.place(x = 20, y = 150) 


########################################################################################################################################################     
#                                                    Function to recharge                                                                              #
# ###################################################################################################################################################### 
def recharge(amountToRecharge,phoneNumber):
    read_database()
    oldBalance = userDataBase[accountNum]['Balance']
    amountToRecharge = amountToRecharge.lower()
    phoneNumber = phoneNumber.lower()
    # Check if the entered number is not some characters #
    if not(amountToRecharge.islower()) and not(phoneNumber.islower()):
        if len(amountToRecharge) > 0 and len(phoneNumber) > 0  and len(phoneNumber) < 14 and int(amountToRecharge) > 0 and int(phoneNumber) > 0:
            if int(amountToRecharge) <= int(oldBalance):
                #update the balance#
                userDataBase[accountNum]['Balance'] = int(oldBalance) - int(amountToRecharge)
                update_data_base()
                messagebox.showinfo("Thank You", "Thank You!", parent = recharge_window)
                recharge_window.destroy()
                fawry_window.destroy()
            else:
                messagebox.showerror("Error", "No sufficient balance", parent = options_window)
                recharge_window.destroy()
                fawry_window.destroy()
        elif len(amountToRecharge) == 0 or int(amountToRecharge) < 0:
            messagebox.showerror("Error", "Enter a valid amount.\nPlease try again", parent = recharge_window)
        elif len(phoneNumber) == 0 or int(phoneNumber) < 0:
            messagebox.showerror("Error", "Enter a valid phone number.\nPlease try again", parent = recharge_window)
        else:
            messagebox.showerror("Error", "Enter a valid phone number.\nPlease try again", parent = recharge_window)
    else:
        messagebox.showerror("Error", "Enter a valid data.\nPlease try again", parent = recharge_window)



########################################################################################################################################################     
#                                                    Check the new password                                                                            #
# ######################################################################################################################################################  
def check_new_pass(newPassEntry, confirmNewPassEntry):
    newPassEntry = newPassEntry.lower()
    confirmNewPassEntry = confirmNewPassEntry.lower()
    if not(newPassEntry.islower()) and not(confirmNewPassEntry.islower()) and len(newPassEntry) == 4 and len(confirmNewPassEntry) == 4:
        if newPassEntry == confirmNewPassEntry and newPassEntry != ''  and confirmNewPassEntry != '':
            messagebox.showinfo("Thank You", "Thank You. Your password has been changed succefully!", parent = options_window)
            passChange_window.destroy()
            # Update the Dict #
            userDataBase[accountNum]['Password'] = newPassEntry
            # Update the database file #
            update_data_base()
        else:
            messagebox.showerror("Error", "Passwords don't match.\nPlease try again.", parent = passChange_window)
    else:
        messagebox.showerror("Error", "Enter a valid password.\nPlease try again.", parent = passChange_window)

########################################################################################################################################################     
#                                                    Function to update the database file                                                              #
# ###################################################################################################################################################### 
def update_data_base():
    fileObj = open("Database.txt","w+", newline='')
    csvwriter = csv.writer(fileObj)
    csvwriter.writerow(['ID', 'Name', 'Password', 'Balance', 'State'])
    for org in userDataBase:
        csvwriter.writerow([org, userDataBase[org]['Name'], userDataBase[org]['Password'], userDataBase[org]['Balance'], userDataBase[org]['State']])
    fileObj.close()


########################################################################################################################################################     
#                                                    Function to close any window                                                                      #
# ######################################################################################################################################################  
def close_window(window_to_close):
    window_to_close.destroy()


# Variable to count the number of wrongly entered account number #
errCount = 0
# First read the initial database #
read_database()
display_main_window()

