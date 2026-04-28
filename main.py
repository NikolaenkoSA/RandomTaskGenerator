import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from datetime import datetime

TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"

# ---------- Предопределённые задачи ----------
DEFAULT_TASKS = [
    {"text": "Прочитать статью по Python", "type": "учёба"},
    {"text": "Сделать зарядку на 15 минут", "type": "спорт"},
    {"text": "Ответить на рабочие письма", "type": "работа"},
    {"text": "Решить 3 задачи на Codewars", "type": "учёба"},
    {"text": "Пробежка 3 км", "type": "спорт"},
    {"text": "Подготовить отчёт за неделю", "type": "работа"},
    {"text": "Посмотреть лекцию по алгоритмам", "type": "учёба"},
    {"text": "Растяжка и йога 20 минут", "type": "спорт"},
    {"text": "Созвониться с командой", "type": "работа"},
    {"text": "Написать конспект по новой теме", "type": "учёба"},
    {"text": "Отжимания 3 подхода по 15 раз", "type": "спорт"},
    {"text": "Обновить резюме", "type": "работа"},
    {"text": "Почитать документацию Django", "type": "учёба"},
    {"text": "Плавание в бассейне", "type": "спорт"},
    {"text": "Запланировать встречу с клиентом", "type": "работа"},
]

# ---------- Загрузка / сохранение ----------
def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- Главное окно ----------
root = tk.Tk()
root.title("Random Task Generator")
root.geometry("800x650")

# Данные
tasks = load_json(TASKS_FILE, DEFAULT_TASKS)
history = load_json(HISTORY_FILE, [])

# ---------- Текущая задача ----------
frame_current = tk.LabelFrame(root, text="Сгенерированная задача", padx=10, pady=10)
frame_current.pack(fill="x", padx=10, pady=5)

lbl_task_text = tk.Label(
    frame_current,
    text="Нажмите кнопку, чтобы сгенерировать задачу",
    wraplength=700,
    font=("Arial", 14, "bold"),
    justify="center",
    fg="#2c3e50"
)
lbl_task_text.pack(pady=5)

lbl_task_type = tk.Label(
    frame_current,
    text="",
    font=("Arial", 11),
    fg="#7f8c8d"
)
lbl_task_type.pack()

def generate_task():
    if not tasks:
        messagebox.showwarning("Нет задач", "Список задач пуст. Добавьте задачи через раздел «Добавить задачу».")
        return
    
    task = random.choice(tasks)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    history.append({
        "text": task["text"],
        "type": task["type"],
        "timestamp": timestamp
    })
    save_json(HISTORY_FILE, history)
    
    lbl_task_text.config(text=f"📋 {task['text']}")
    lbl_task_type.config(text=f"Категория: {task['type'].capitalize()}")
    
    refresh_history()
    update_filter_combo()

btn_generate = tk.Button(
    frame_current,
    text="🎲 Сгенерировать задачу",
    command=generate_task,
    font=("Arial", 12),
    padx=20,
    pady=5,
    bg="#3498db",
    fg="white"
)
btn_generate.pack(pady=10)

# ---------- История ----------
frame_history = tk.LabelFrame(root, text="История сгенерированных задач", padx=10, pady=10)
frame_history.pack(fill="both", expand=True, padx=10, pady=5)

# Listbox с прокруткой
listbox_frame = tk.Frame(frame_history)
listbox_frame.pack(fill="both", expand=True)

listbox_history = tk.Listbox(listbox_frame, height=12, font=("Consolas", 10))
scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox_history.yview)
listbox_history.configure(yscrollcommand=scrollbar.set)

listbox_history.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def refresh_history(filtered=None):
    listbox_history.delete(0, tk.END)
    data = filtered if filtered is not None else history
    if not data:
        listbox_history.insert(tk.END, "История пуста. Сгенерируйте первую задачу!")
        return
    for entry in reversed(data):
        display = f"[{entry['timestamp']}] [{entry['type'].upper()}] {entry['text']}"
        listbox_history.insert(tk.END, display)

# ---------- Фильтрация ----------
frame_filter = tk.LabelFrame(root, text="Фильтрация по типу задачи", padx=10, pady=10)
frame_filter.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filter, text="Тип задачи:").pack(side="left", padx=5)
combo_filter_type = ttk.Combobox(frame_filter, state="readonly", width=15)
combo_filter_type.pack(side="left", padx=5)

def update_filter_combo():
    types_in_history = sorted({h["type"] for h in history})
    combo_filter_type["values"] = ["Все"] + types_in_history
    combo_filter_type.current(0)

def apply_filter():
    selected_type = combo_filter_type.get()
    if not selected_type or selected_type == "Все":
        refresh_history()
        return
    
    filtered = [h for h in history if h["type"] == selected_type]
    refresh_history(filtered)

def clear_history():
    if not history:
        messagebox.showinfo("Очистка", "История уже пуста")
        return
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        history.clear()
        save_json(HISTORY_FILE, history)
        refresh_history()
        update_filter_combo()
        messagebox.showinfo("Очистка", "История очищена")

btn_apply = tk.Button(frame_filter, text="Применить", command=apply_filter, width=12)
btn_apply.pack(side="left", padx=5)

btn_clear = tk.Button(frame_filter, text="Очистить историю", command=clear_history, width=15, bg="#e74c3c", fg="white")
btn_clear.pack(side="right", padx=5)

# ---------- Добавление задачи ----------
frame_add = tk.LabelFrame(root, text="Добавить новую задачу в коллекцию", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add, text="Текст задачи:").grid(row=0, column=0, sticky="w")
entry_new_text = tk.Entry(frame_add, width=40)
entry_new_text.grid(row=0, column=1, padx=5)

tk.Label(frame_add, text="Тип:").grid(row=0, column=2, sticky="w")
task_types = ["учёба", "спорт", "работа", "дом", "хобби"]
combo_new_type = ttk.Combobox(frame_add, values=task_types, width=12, state="readonly")
combo_new_type.grid(row=0, column=3, padx=5)
combo_new_type.current(0)

def add_task():
    text = entry_new_text.get().strip()
    task_type = combo_new_type.get()
    
    if not text:
        messagebox.showerror("Ошибка", "Текст задачи не может быть пустым")
        return
    
    tasks.append({"text": text, "type": task_type})
    save_json(TASKS_FILE, tasks)
    
    messagebox.showinfo("Успех", f"Задача «{text}» добавлена в коллекцию!")
    entry_new_text.delete(0, tk.END)

def show_all_tasks():
    if not tasks:
        messagebox.showinfo("Все задачи", "Коллекция задач пуста")
        return
    
    # Создаём временное окно со списком
    win = tk.Toplevel(root)
    win.title("Все задачи в коллекции")
    win.geometry("600x400")
    
    tk.Label(win, text="Список всех доступных задач:", font=("Arial", 12, "bold")).pack(pady=10)
    
    listbox = tk.Listbox(win, font=("Consolas", 10))
    scroll = tk.Scrollbar(win, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scroll.set)
    
    listbox.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)
    
    for task in sorted(tasks, key=lambda t: t["type"]):
        listbox.insert(tk.END, f"[{task['type'].upper()}] {task['text']}")

btn_add = tk.Button(frame_add, text="Добавить задачу", command=add_task, width=15)
btn_add.grid(row=0, column=4, padx=5)

btn_show_all = tk.Button(frame_add, text="Показать все задачи", command=show_all_tasks, width=18)
btn_show_all.grid(row=0, column=5, padx=5)

# ---------- Статистика ----------
def show_stats():
    if not history:
        messagebox.showinfo("Статистика", "История пуста. Сгенерируйте хотя бы одну задачу.")
        return
    
    total = len(history)
    type_counts = {}
    for h in history:
        type_counts[h["type"]] = type_counts.get(h["type"], 0) + 1
    
    stats = f"📊 Статистика использования:\n\n"
    stats += f"Всего сгенерировано задач: {total}\n\n"
    stats += "По типам:\n"
    for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count
        stats += f"  {t.capitalize()}: {count} {bar}\n"
    
    messagebox.showinfo("Статистика", stats)

btn_stats = tk.Button(frame_add, text="📊 Статистика", command=show_stats, width=15)
btn_stats.grid(row=0, column=6, padx=5)

# ---------- Инициализация ----------
refresh_history()
update_filter_combo()

root.mainloop()