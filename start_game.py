import tkinter as tk

from ai import *
from constants import *
from multi_player import *

main_win = tk.Tk()
main_win.attributes("-fullscreen", True)
main_win['background'] = "#1CAA9C"


def AI():
    main_win.destroy()
    main()

def multi():
    main_win.destroy()
    connect2multiplayer()
    
btn_AI = tk.Button(main_win,text = "Single Player", height= 1, width=16,bg="#61ffef", font=('Arial',34),command=AI)
btn_AI.place(x=550,y=250)

btn_Multi = tk.Button(main_win,text = "Multi Player", height= 1, width=16,bg="#61ffef", font=('Arial',34),command=multi)
btn_Multi.place(x=550,y=400)

main_win.mainloop()

