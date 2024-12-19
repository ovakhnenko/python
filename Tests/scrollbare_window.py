import tkinter as tk

root = tk.Tk()
root.geometry("600x400")

# Создаём Canvas и Scrollbars
canvas = tk.Canvas(root)
v_scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)

# Привязываем Scrollbars к Canvas
canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Размещаем Canvas и Scrollbars
canvas.grid(row=0, column=0, sticky="nsew")
v_scrollbar.grid(row=0, column=1, sticky="ns")
h_scrollbar.grid(row=1, column=0, sticky="ew")

# Создаём прокручиваемый Frame
scrollable_frame = tk.Frame(canvas)

# Размещаем Frame внутри Canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Добавляем содержимое в Frame (например, метки)
for i in range(20):
    for j in range(5):
        tk.Label(scrollable_frame, text=f"Элемент {i+1}, {j+1}", bg="lightblue").grid(row=i, column=j, padx=5, pady=5)

# Обновляем размер scrollregion для Canvas
def configure_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollregion)

# Устанавливаем параметры для строки и столбца
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
