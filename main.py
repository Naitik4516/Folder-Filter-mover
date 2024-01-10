from tkinter import *
import os
import shutil
from tkinter import filedialog, messagebox

def ignore_list(dir, files):
    return [folder for folder in files if os.path.isdir(os.path.join(dir, folder)) and folder in ignore.get()]

def move():
    shutil.copytree(source.get(),dest.get(),ignore=ignore_list, dirs_exist_ok=True)
    messagebox.showinfo("Success","Files are moved successfully!")

def setSource():
    location = filedialog.askdirectory(initialdir=os.getcwd(),title="Source")
    source.set(location)
    
def setDest():
    location = filedialog.askdirectory(title="Source",mustexist=False)
    dest.set(location)

root = Tk()
root.geometry('600x300')
root.title("Folders mover for programmers")

source = StringVar(value=os.getcwd())
dest = StringVar(value="C:\\")
ignore = StringVar(value="venv,.venv,node_modules")

source_label = Label(root,text="Source: ", font="arial 16")
source_entry = Entry(root, textvariable=source, width=40, font="arial 12")
source_button = Button(root,text="choose source",padx=10,pady=5, command=setSource)
dest_label = Label(root,text="Destination: ", font="arial 16")
dest_entry = Entry(root, textvariable=dest, width=40, font="arial 12")
dest_button = Button(root,text="choose destination",padx=10,pady=5, command=setDest)
ignore_label = Label(root,text="Ignore Files or Folders: ", font="arial 16")
ignore_entry = Entry(root, textvariable=ignore, width=40, font="arial 12")

move_button = Button(root,text="Move",padx=10,pady=5, command=move)

source_label.pack()
source_entry.pack()
source_button.pack()
dest_label.pack()
dest_entry.pack()
dest_button.pack()
ignore_label.pack()
ignore_entry.pack()
move_button.pack(side=BOTTOM,pady=10)


root.mainloop()