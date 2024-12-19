import tkinter as tk
from tkinter import ttk
 
# Создаем главное окно
root = tk.Tk()
root.title("Listbox с несколькими колонками")
 
# Создаем Treeview с несколькими колонками
columns = ("#1", "#2", "#3")
tree = ttk.Treeview(root, columns=columns, show="headings")
 
# Определяем заголовки и ширину колонок
tree.heading("#1", text="Колонка 1")
tree.heading("#2", text="Колонка 2")
tree.heading("#3", text="Колонка 3")
 
tree.column("#1", width=100)
tree.column("#2", width=100)
tree.column("#3", width=100)
 
# Добавляем данные
data = [
    ("Первый", "Элемент", "Тест"),
    ("Второй", "Элемент", "Пример"),
    ("Третий", "Элемент", "Python"),
]
 
for row in data:
    tree.insert("", tk.END, values=row)
 
# Размещаем Treeview в окне
tree.pack(fill=tk.BOTH, expand=True)
 
# Запускаем главный цикл
root.mainloop()
