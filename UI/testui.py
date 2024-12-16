import tkinter as tk
from datetime import datetime

def on_button_click():
    current_dateTime = datetime.now()
    label.config(text=f"Hello World! {current_dateTime}")
 
root = tk.Tk()
root.title("ein App-Beispiel")
root.geometry("600x400")

str_var=tk.StringVar()

label = tk.Label(root, text="drücke ein Button")
label.grid(row=0,column=0)

entry = tk.Entry(root,textvariable = str_var, font=('calibre',10,'normal'))
entry.grid(row=0,column=1)

button = tk.Button(root, text="drücke mich", command=on_button_click)
button.grid(row=2,column=1)
 
root.mainloop()

