import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.title("FastTxt")
root.geometry("800x500")
editor_font = tkfont.Font(family="Consolas", size=11)
current_path = None
current_theme = "light"

themes = {
    "light": {"bg": "#ffffff", "fg": "#000000", "gutter": "#eeeeee", "gutter_fg": "#555555", "bar": "#f0f0f0"},
    "dark": {"bg": "#1e1e1e", "fg": "#d4d4d4", "gutter": "#2b2b2b", "gutter_fg": "#858585", "bar": "#333333"},
}

def clear():
    global current_path
    text.delete("1.0", "end")
    current_path = None
    update_numbers()

def copy_all():
    root.clipboard_clear()
    root.clipboard_append(text.get("1.0", "end-1c"))

def save_file(event=None):
    global current_path
    if current_path is None:
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not path:
            return
        current_path = path
    with open(current_path, "w", encoding="utf-8") as f:
        f.write(text.get("1.0", "end-1c"))
    text.edit_modified(False)

def open_file():
    global current_path
    path = filedialog.askopenfilename()
    if path:
        current_path = path
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        text.delete("1.0", "end")
        text.insert("1.0", content)
        update_numbers()
        text.edit_modified(False)

def update_numbers(event=None):
    line_count = int(text.index("end-1c").split(".")[0])
    numbers.config(state="normal")
    numbers.delete("1.0", "end")
    numbers.insert("1.0", "\n".join(str(i) for i in range(1, line_count +1)), "center")
    numbers.config(state="disabled")
    numbers.yview_moveto(text.yview()[0])
    update_status()

def on_scroll(first, last):
    numbers.yview_moveto(first)
    update_numbers()

def on_close():
    if text.edit_modified():
        answer = messagebox.askyesnocancel("Unsaved changes", "Save changes before closing?")
        if answer is None:
            return
        if answer:
            save_file()
            if text.edit_modified():
                return
    root.destroy()

def update_status(event = None):
    line, col = text.index("insert").split(".")
    words = len(text.get("1.0", "end-1c").split())
    status.config(text=f"Ln {line}, Col {int(col) + 1}   |   Words: {words}")

def zoom(event):
    size = editor_font.cget("size")
    if event.delta > 0:
        size += 1
    else:
        size -= 1
    size = max(6, min(60, size))
    editor_font.configure(size=size)
    update_numbers()
    return "break"

def apply_theme(name):
    t = themes[name]
    text.config(bg=t["bg"], fg=t["fg"], insertbackground=t["fg"])
    numbers.config(bg=t["gutter"], fg=t["gutter_fg"])
    status.config(bg=t["bar"], fg=t["fg"])
    bar.config(bg=t["bar"])
    bottom.config(bg=t["bar"])
    for b in (copy_button, clear_button, save_button, open_button, theme_button):
        b.config(bg=t["bar"], fg=t["fg"])

def toggle_theme():
    global current_theme
    if current_theme == "light":
        current_theme = "dark"
    else:
        current_theme = "light"
    apply_theme(current_theme)
    theme_button.config(text="Light" if current_theme == "dark" else "Dark")







bar = tk.Frame(root)
bar.pack(side="top", fill="x")
bottom = tk.Frame(root)
bottom.pack(side="bottom", fill="x")
status = tk.Label(bottom, text="", anchor="w")
status.pack(side="left", fill="x", expand=True)


theme_button = tk.Button(bottom, text="Dark", command=toggle_theme)
theme_button.pack(side="right")

copy_button = tk.Button(bar, text="Copy All", command=copy_all)
copy_button.pack(side="left", fill="x", expand=True)

clear_button = tk.Button(bar, text="Clear", command=clear)
clear_button.pack(side="left", fill="x", expand=True)

save_button = tk.Button(bar, text="Save", command=save_file)
save_button.pack(side="left", fill="x", expand=True)

open_button = tk.Button(bar, text="Open", command=open_file)
open_button.pack(side="left", fill="x", expand=True)




numbers = tk.Text(root, width=4, bg="#eeeeee", font=editor_font)
numbers.tag_configure("center", justify="center")
numbers.config(state="disabled")
numbers.pack(side="left", fill="y")

text = tk.Text(root, wrap="none", undo=True, yscrollcommand=on_scroll, font=editor_font)
text.pack(side="left", fill="both", expand=True)

text.bind("<KeyPress>", update_numbers)
text.bind("<KeyRelease>", update_numbers)
text.bind("<ButtonRelease-1>", update_status)
text.bind("<Control-MouseWheel>", zoom)
root.bind("<Control-S>", save_file)
root.bind("<Control-s>", save_file)


if len(sys.argv) > 1:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text.insert("1.0", f.read())
        text.edit_modified(False)


apply_theme(current_theme)
update_numbers()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
