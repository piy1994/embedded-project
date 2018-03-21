from Tkinter import *


def main_gui():
    #print('hello')
    root = Tk()
    
    w = 300 # width for the Tk root
    h = 75 # height for the Tk root
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    
    
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    username = "piyush" #that's the given username
    password = "project" #that's the given password
    #username entry
    Label(root, text = "Username").grid(row=0)
    Label(root, text = "Password").grid(row=1)

    username_entry = Entry(root)
    password_entry = Entry(root, show='*')

    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)
  
    def trylogin():
	#this method is called when the button is pressed
        #to get what's written inside the entries, I use get()
        #check if both username and password in the entries are same of the given ones
        if username == username_entry.get() and password == password_entry.get():
            print("Access Granted")
            root.quit()
            root.destroy()
        else:
            print("Access Denied")
    #when you press this button, trylogin is called
    button = Button(root, text="check", command = trylogin).grid(row=3) 
#    button.pack()
    #App starter
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Authorization Required')
    root.mainloop()

if __name__ == "__main__":    
    main_gui()  
