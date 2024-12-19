import tkinter as tk
from tkinter import ttk
 
def get_selected_items():
    selected_items = [item for i, item in enumerate(items) if var_list[i].get()]
    print("Выбранные элементы:", selected_items)
 
# Создаем окно
root = tk.Tk()
root.title("Listbox с чекбоксами")
 
# Список элементов
items = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"]
 
# Список для хранения состояний чекбоксов
var_list = []
 
# Фрейм для чекбоксов
frame = ttk.Frame(root)
frame.pack(pady=10)
 
# Создаем чекбоксы для каждого элемента
for item in items:
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(frame, text=item, variable=var)
    chk.pack(anchor="w", pady=2)
    var_list.append(var)
 
# Кнопка для получения выбранных элементов
button = ttk.Button(root, text="Показать выбранные", command=get_selected_items)
button.pack(pady=10)
 
# Запуск главного цикла приложения
root.mainloop()
