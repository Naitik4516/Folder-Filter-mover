import multiprocessing
import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import time

class FileTransfer:
    # NOTE: We can't communicate with the main thread from a worker process. It means we can't communicate with tkinter gui if we are using multiprocessing.

    def __init__(self, source, destination, ignore) -> None:
        self.source = source
        self.destination = destination
        self.ignore = ignore
        
        self.timestamp_file =  None
        self.total_items = 0
        self.completed_items = 0
        self.current_timestamp = time.time()
        self.timestamp_file = os.path.join(self.destination, 'last_transfer_timestamp.txt')

    def copy_folder(self, item):
        print("Copying ", item)
        destination_item = os.path.join(self.destination, os.path.relpath(item, self.source))
        if os.path.isdir(item):
            shutil.copytree(item, destination_item, ignore=self.get_ignore_list, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination_item)
        
    def get_files_to_transfer(self):
        # Load the last transfer timestamp from a file (if it exists)
        last_transfer_timestamp = 0

        if os.path.exists(self.timestamp_file):
            print("last_transfer_timestamp.txt exists")
            with open(self.timestamp_file, 'r') as f:
                last_transfer_timestamp = float(f.read())

        # Create a list of items that have been modified since the last transfer
        modified_items = []

        for root, dirs, files in os.walk(self.source):
            for item in files + dirs:
                item_path = os.path.join(root, item)
                item_timestamp = os.path.getmtime(item_path)

                if item_timestamp > last_transfer_timestamp:
                    modified_items.append(item_path)

        if not os.path.exists(self.destination):
            os.makedirs(self.destination)

        return modified_items
    
    def run(self):
        files_to_transfer = self.get_files_to_transfer()
        self.total_items = len(files_to_transfer)
        print("Total items:", self.total_items)

        # Create a pool of worker processes
        pool = multiprocessing.Pool()
        pool.map(self.copy_folder, files_to_transfer)
        pool.close()
        pool.join()
        self.complete()

    def complete(self):
            print("Transfer complete.")

            # Update the last transfer timestamp
            with open(self.timestamp_file, 'w') as f:
                f.write(str(self.current_timestamp))

            print(
                f"Modified items transferred from '{self.source}' to '{self.destination}' successfully.")

    def get_ignore_list(self, dir, files):
        return [folder for folder in files if os.path.isdir(os.path.join(dir, folder)) and folder in self.ignore]


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Folder Transfer GUI")
        self.root.geometry("600x300")

        self.source = tk.StringVar(value=os.path.join(os.getcwd(), 'sample_folder'))
        self.dest = tk.StringVar(value=os.path.join(os.getcwd(), 'sample_destination_folder'))
        self.ignore = tk.StringVar(value="venv,.venv,node_modules")

        # Create labels and entry fields for source and destination folders
        source_label = tk.Label(self.root, text="Source: ", font="arial 16")
        source_entry = tk.Entry(self.root, textvariable=self.source, width=30, font="arial 12")
        source_button = tk.Button(self.root, text="Choose source", padx=10, pady=5, command=self.browse_source_folder)
        source_label.grid(row=0, column=0, padx=10, pady=5, sticky='E')
        source_entry.grid(row=0, column=1, padx=10, pady=5)
        source_button.grid(row=0, column=2, padx=10, pady=5, sticky='W')

        dest_label = tk.Label(self.root, text="Destination: ", font="arial 16")
        dest_entry = tk.Entry(self.root, textvariable=self.dest, width=30, font="arial 12")
        dest_button = tk.Button(self.root, text="Choose destination", padx=10, pady=5,
                                command=self.browse_dest_folder)
        dest_label.grid(row=1, column=0, padx=10, pady=5, sticky='E')
        dest_entry.grid(row=1, column=1, padx=10, pady=5)
        dest_button.grid(row=1, column=2, padx=10, pady=5, sticky='W')

        ignore_label = tk.Label(self.root, text="Ignore: ", font="arial 16")
        ignore_entry = tk.Entry(self.root, textvariable=self.ignore, width=30, font="arial 12")
        ignore_label.grid(row=2, column=0, padx=10, pady=5, sticky='E')
        ignore_entry.grid(row=2, column=1, padx=10, pady=5)

        boost_transfer_button = tk.Button(self.root, text="Boost Transfer", font="arial 14", background="orange",
                                          command=self.start_boost_transfer)
        boost_transfer_button.grid(row=3, column=0, columnspan=2, pady=40)
        cancel_button = tk.Button(self.root, text="Cancel", font="arial 14", background="red",
                                  command=self.terminate_pool)
        cancel_button.grid(row=3, column=1, columnspan=2, pady=40)

        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='determinate')
        self.progress_percent = tk.Label(self.root, text='', font="arial 16")

        self.root.mainloop()

    
    def browse_source_folder(self):
        location = filedialog.askdirectory(initialdir=self.source.get(), title="Source")
        self.source.set(location)

    def browse_dest_folder(self):
        location = filedialog.askdirectory(initialdir=self.dest.get(), title="Destination", mustexist=False)
        self.dest.set(location)


    def start_boost_transfer(self):
        source = self.source.get()
        destination = self.dest.get()
        ignore = self.ignore.get()

        tk.messagebox.showinfo("Transfer Started", "Transfer has started. All the progress will be shown in the console.")
        tk.messagebox.showwarning("Warning", "Do not close the window until the transfer is complete. You can minimize the window. If you close the window, the transfer will be cancelled.")
        file_transfer = FileTransfer(source, destination, ignore)
        thread = threading.Thread(target=file_transfer.run)
        thread.start()


if __name__ == "__main__":
    App()
