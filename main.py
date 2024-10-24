from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
import requests
import pyperclip
import json
import os

history_file = "upload_history.json"


def show_history():
    if not os.path.exists((history_file)):
        mb.showinfo("История", "История загрузок пуста!")
        return

    history_window = Toplevel(window)
    history_window.title("История загрузок")

    files_listbox = Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10, 0), pady=10)

    linkes_listbox = Listbox(history_window, width=50, height=20)
    linkes_listbox.grid(row=0, column=1, padx=(0, 10), pady=10)

    with open(history_file, 'r') as f:
        history = json.load(f)
        for item in history:
            files_listbox.insert(END, item['filepath'])
            linkes_listbox.insert(END, item['dowload_link'])

def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)


def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()
                download_link = response.json()['link']
                entry.delete(0, END)
                entry.insert(0, download_link)
                pyperclip.copy(download_link)
                save_history(filepath, download_link)
                mb.showinfo("Ссылка скопирована!",f"Ссылка {download_link} успешно скопирована в буфер обмена!")
    except Exception as e:
        mb.showerror("Ошибка!",f"Произошла ошибка {e}!")

window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("400x200")

button = ttk.Button(text="Загрузить файл", command=upload)
button.pack()

entry = ttk.Entry()
entry.pack()

history_button = ttk.Button(text="Показать историю", command=show_history)
history_button.pack()

window.mainloop()