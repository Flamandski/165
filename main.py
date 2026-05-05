import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")

        # Данные тренировок
        self.trainings = []
        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Combobox(self.root, values=["Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2,
                                                                                         pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(self.root,
                                        values=["Все", "Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Фильтровать", command=self.apply_filters).grid(row=7, column=0, pady=10)
        tk.Button(self.root, text="Сбросить фильтры", command=self.reset_filters).grid(row=7, column=1, pady=10)

        # Кнопки сохранения/загрузки
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=8, column=0, pady=10)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=8, column=1, pady=10)

    def validate_input(self, date_str, duration_str):
        # Проверка даты
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return False

        # Проверка длительности
        try:
            duration = float(duration_str)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        return True

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate_input(date, duration):
            return

        training = {
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }

        self.trainings.append(training)
        self.update_table()

        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.type_entry.set('')
        self.duration_entry.delete(0, tk.END)

    def apply_filters(self):
        filtered = self.trainings

        # Фильтр по типу
        filter_type = self.filter_type.get()
        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]

        # Фильтр по дате
        filter_date = self.filter_date.get()
        if filter_date:
            try:
                datetime.strptime(filter_date, '%Y-%m-%d')
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для фильтра")
                return

        self.update_table(filtered)

    def reset_filters(self):
        self.filter_type.set("Все")
        self.filter_date.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open('trainings.json', 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", "Данные сохранены в trainings.json")

    def load_data(self):
        if os.path.exists('trainings.json'):
            with open('trainings.json', 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)
            self.update_table()
            messagebox.showinfo("Успех", "Данные загружены из trainings.json")
        else:
            messagebox.showwarning("Предупреждение", "Файл trainings.json не найден")

    def update_table(self, data=None):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        display_data = data if data is not None else self.trainings
        for training in display_data:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                training["duration"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
