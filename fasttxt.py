import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("TxtFast")

def clear():
    text.delete("1.0", "end")
    update_numbers()

def copy_all():
    root.clipboard_clear()
    root.clipboard_append(text.get("1.0", "end-1c"))

def save_file():
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.get("1.0", "end-1c"))

def open_file():
    path = filedialog.askopenfilename()
    if path:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        text.delete("1.0", "end")
        text.insert("1.0", content)
        update_numbers()

def update_numbers(event=None):
    line_count = int(text.index("end-1c").split(".")[0])
    numbers.config(state="normal")
    numbers.delete("1.0", "end")
    numbers.insert("1.0", "\n".join(str(i) for i in range(1, line_count +1)), "center")
    numbers.config(state="disabled")
    numbers.yview_moveto(text.yview()[0])

def on_scroll(first, last):
    numbers.yview_moveto(first)
    update_numbers()

def on_modified(event=None):
    if text.edit_modified():
        update_numbers()
        text.edit_modified(False)

bar = tk.Frame(root)
bar.pack(side="top", fill="x")

copy_button = tk.Button(bar, text="Copy All", command=copy_all)
copy_button.pack(side="left", fill="x", expand=True)

clear_button = tk.Button(bar, text="Clear", command=clear)
clear_button.pack(side="left", fill="x", expand=True)

save_button = tk.Button(bar, text="Save", command=save_file)
save_button.pack(side="left", fill="x", expand=True)

open_button = tk.Button(bar, text="Open", command=open_file)
open_button.pack(side="left", fill="x", expand=True)

numbers = tk.Text(root, width=4, bg="#eeeeee")
numbers.tag_configure("center", justify="center")
numbers.config(state="disabled")
numbers.pack(side="left", fill="y")

text = tk.Text(root, wrap="none", undo=True, yscrollcommand=on_scroll)
text.pack(side="left", fill="both", expand=True)
text.bind("<<Modified>>", on_modified)

update_numbers()
root.mainloop()