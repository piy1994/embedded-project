from Tkinter import *


def main_gui():
    print('hello')
    root = Tk()
    
    w = 200 # width for the Tk root
    h = 75 # height for the Tk root
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    
    
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    username = "abc" #that's the given username
    password = "cba" #that's the given password
    #username entry
    username_entry = Entry(root)
    username_entry.pack()
    #password entry
    password_entry = Entry(root, show='*')
    password_entry.pack()
    def trylogin(): #this method is called when the button is pressed
        #to get what's written inside the entries, I use get()
        #check if both username and password in the entries are same of the given ones
        if username == username_entry.get() and password == password_entry.get():
            print("Correct")
            root.quit()
            root.destroy()
        else:
            print("Wrong")
    #when you press this button, trylogin is called
    button = Button(root, text="check", command = trylogin) 
    button.pack()
    #App starter
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.mainloop()

if __name__ == "__main__":    
    main_gui()  
