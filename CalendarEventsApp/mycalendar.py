import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import threading
import time
from plyer import notification

# Списък за събития
events = []

# Функция за добавяне на събитие
def add_event():
    name = entry_name.get()
    time_str = entry_time.get()
    date_str = cal.get_date()
    if not name or not time_str:
        messagebox.showwarning("Грешка", "Попълнете име и час!")
        return
    events.append({"name": name, "time": time_str, "date": date_str})
    listbox_events.insert(tk.END, f"{date_str} - {name} - {time_str}")
    entry_name.delete(0, tk.END)
    entry_time.delete(0, tk.END)

# Функция за проверка на събитията
def check_events():
    while True:
        now_date = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")
        for i, event in enumerate(events[:]):
            if event["date"] == now_date and event["time"] == now_time:
                notification.notify(
                    title="Предстоящо събитие",
                    message=f"{event['name']} започва сега!",
                    timeout=10
                )
                listbox_events.delete(i)
                events.remove(event)
        time.sleep(30)

# --- Създаваме главния прозорец ---
root = tk.Tk()
root.title("Моят Календар")
root.geometry("600x600")
root.configure(bg="#2e2e2e")  # тъмен фон

# --- Горен Frame за календара ---
frame_calendar = tk.Frame(root, bg="#2e2e2e")
frame_calendar.pack(pady=10)

cal = Calendar(frame_calendar, selectmode='day', date_pattern='yyyy-mm-dd',
               background='#1e1e1e', foreground='white', selectbackground='#4caf50', font=("Helvetica", 11))
cal.pack()

# --- Среден Frame за добавяне на събития ---
frame_add = tk.Frame(root, bg="#2e2e2e")
frame_add.pack(pady=15)

tk.Label(frame_add, text="Име на събитието:", bg="#2e2e2e", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_add, width=30, font=("Helvetica", 11))
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Час (ЧЧ:ММ):", bg="#2e2e2e", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_time = tk.Entry(frame_add, width=10, font=("Helvetica", 11))
entry_time.grid(row=1, column=1, padx=5, pady=5, sticky="w")

btn_add = tk.Button(frame_add, text="Добави събитие", command=add_event, bg="#4caf50", fg="white", font=("Helvetica", 12), activebackground="#45a049")
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

# --- Долен Frame за списъка със събития ---
frame_list = tk.Frame(root, bg="#2e2e2e")
frame_list.pack(pady=10, fill="both", expand=True)

tk.Label(frame_list, text="Списък със събития:", bg="#2e2e2e", fg="white", font=("Helvetica", 12)).pack(anchor="w", padx=5)

# Listbox с scrollbar
scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")

listbox_events = tk.Listbox(frame_list, width=80, height=10, yscrollcommand=scrollbar.set, bg="#1e1e1e", fg="white", font=("Helvetica", 11))
listbox_events.pack(pady=5, padx=5, fill="both", expand=True)
scrollbar.config(command=listbox_events.yview)

# --- Стартираме проверката на отделен поток ---
thread = threading.Thread(target=check_events, daemon=True)
thread.start()

# --- Стартираме интерфейса ---
root.mainloop()
