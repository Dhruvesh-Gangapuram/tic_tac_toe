import tkinter as tk
from server import *
from client import *

def connect2multiplayer():
    
    main_win = tk.Tk()
    main_win.attributes("-fullscreen", True)
    main_win['background'] = "#1CAA9C"


    def host():
        main_win.destroy()
        send()

    def connect_game():
        main_win.destroy()
        recv()
    
    
    btn_host = tk.Button(main_win,text = "Host a game", height= 1, width=16,bg="#61ffef", font=('Arial',34),command=host)
    btn_host.place(x=550,y=250)

    btn_connect = tk.Button(main_win,text = "Connect a game", height= 1, width=16,bg="#61ffef", font=('Arial',34),command=connect_game)
    btn_connect.place(x=550,y=400)

    main_win.mainloop()