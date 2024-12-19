import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime

defaultPassword = "123Start#"
userOU = "OU=Users,OU=TEST,DC=test,DC=local"  
groupOU = "OU=Groups,OU=TEST,DC=test,DC=local"
domainName = "test.local"

def on_name_aendert(*args):
    userName = vornameBenutzer_str_var.get().lower() + "." + nachnameBenutzer_str_var.get().lower()
    emailAddress = userName + "@" + domainName_str_var.get()
    userName_str_var.set(userName)
    userEMailAdresse_str_var.set(emailAddress)
    prüfe_daten()

def prüfe_daten():
    if len(userName_str_var.get()) > 20:
        button_generiere.config(state='disabled')
    else:    
        button_generiere.config(state='normal')

def on_generiere_button_click():
    groupOU =groupOU_str_var.get() 
    ps_command = f"Get-ADGroup -Filter * -SearchBase " + groupOU + "| Select-Object Name"
    result = ps_run(ps_command)
    print(result)

def on_default_button_click():
    standardwertenEinstellen()

def on_schliesse_button_click():
    exit(0)

def ps_run(ps_command):
    completed = subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    return completed 

def standardwertenEinstellen():
    userOU_str_var.set(userOU)
    groupOU_str_var.set(groupOU)
    domainName_str_var.set(domainName)
    vornameBenutzer_str_var.set("")
    nachnameBenutzer_str_var.set("")
    defaultPassword_str_var.set(defaultPassword)
    userName_str_var.set("")
    userEMailAdresse_str_var.set("")

def get_selected_groups():
    selected_groups = [group for i, group in enumerate(groups) if var_list[i].get()]
    print(selected_groups)    

root = tk.Tk()
root.title("Benutzergenerator")
root.geometry("600x600")

canvas = tk.Canvas(root)
v_scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")
v_scrollbar.grid(row=0, column=1, sticky="ns")
h_scrollbar.grid(row=1, column=0, sticky="ew")

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

#buttons
button_generiere = tk.Button(scrollable_frame, text="Generiere", width=12, command=on_generiere_button_click, fg='blue')
button_generiere.grid(row=0, column=1, padx=5, pady=10, sticky="w")
button_standardwert = tk.Button(scrollable_frame, text="Standardwert", width=12, command=on_default_button_click)
button_standardwert.grid(row=0, column=2, padx=5, pady=10, sticky="w")
button_schliessen = tk.Button(scrollable_frame, text="Schließen", width=12, command=on_schliesse_button_click)
button_schliessen.grid(row=0, column=3, padx=5, pady=10, sticky="w")

#userOU
label = tk.Label(scrollable_frame, text="Benutzer OU: ")
label.grid(row=1, column=3, padx=10, pady=5, sticky="w")
userOU_str_var=tk.StringVar()
entry = tk.Entry(scrollable_frame, textvariable = userOU_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
entry.grid(row=1, column=4)

#groupOU
label = tk.Label(scrollable_frame, text="Gruppe OU: ")
label.grid(row=2,column=3, padx=10, pady=5, sticky="w")
groupOU_str_var=tk.StringVar()
entry = tk.Entry(scrollable_frame,textvariable = groupOU_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
entry.grid(row=2, column=4)

#domainName
label = tk.Label(scrollable_frame, text="Domänename: ")
label.grid(row=3,column=3, padx=10, pady=5, sticky="w")
domainName_str_var=tk.StringVar()
entry = tk.Entry(scrollable_frame, textvariable = domainName_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
entry.grid(row=3, column=4)

#vornameBenutzer
label = tk.Label(scrollable_frame, text="Benutzervorname: ", fg='blue')
label.grid(row=4,column=3, padx=10, pady=5, sticky="w")
vornameBenutzer_str_var=tk.StringVar()
vornameBenutzerEntry = tk.Entry(scrollable_frame,textvariable = vornameBenutzer_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
vornameBenutzerEntry.bind("<Key>", on_name_aendert)
vornameBenutzerEntry.grid(row=4, column=4)

#nachnameBenutzer
label = tk.Label(scrollable_frame, text="Benutzernachname: ", fg='blue')
label.grid(row=5,column=3, padx=10, pady=5, sticky="w")
nachnameBenutzer_str_var=tk.StringVar()
nachnameBenutzerEntry = tk.Entry(scrollable_frame, textvariable = nachnameBenutzer_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
nachnameBenutzerEntry.bind("<Key>", on_name_aendert)
nachnameBenutzerEntry.grid(row=5, column=4)

#defaultPassword
label = tk.Label(scrollable_frame, text="Benutzerkennwort: ", fg='blue')
label.grid(row=6,column=3, padx=10, pady=5, sticky="w")
defaultPassword_str_var=tk.StringVar()
entry = tk.Entry(scrollable_frame, textvariable = defaultPassword_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
entry.grid(row=6, column=4)

#$userName
label = tk.Label(scrollable_frame, text="Benutzername: ")
label.grid(row=7,column=3, padx=10, pady=5, sticky="w")
userName_str_var=tk.StringVar()
entry = tk.Entry(scrollable_frame,textvariable = userName_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
entry.grid(row=7, column=4)

#emailAddress
label = tk.Label(scrollable_frame, text="E-Mail: ")
label.grid(row=8, column=3, padx=10, pady=5, sticky="w")
userEMailAdresse_str_var=tk.StringVar()
entry = tk.Entry(scrollable_frame,textvariable = userEMailAdresse_str_var, font=('Arial',10,'normal'), fg='black', width = 64)
entry.grid(row=8, column=4)

#gruppen
groups = ["group 1", "group 2", "group 3", "group 4", "group 5", "group 6", "group 1", "group 2", "group 3", "group 4", "group 5", "group 6"]
var_list = []
for group in groups:
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(scrollable_frame, text=group, variable=var)
    chk.grid(padx=10, pady=5, sticky="w")
    var_list.append(var)

def configure_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollregion)

standardwertenEinstellen() 
vornameBenutzerEntry.focus()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.mainloop()
