import tkinter as tk
#from tkinter import ttk
from tkinter import filedialog, messagebox
import numpy as np
import os
import pyradian_asm as asm

class Notepad(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    def create_widgets(self):
        # Create the save and open button frame
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        # Create the open button
        self.open_button = tk.Button(button_frame, text='Ouvrir', command=self.open_file)
        self.open_button.pack(side=tk.LEFT)
        # Create the save button
        self.save_button = tk.Button(button_frame, text='Enregistrer sous', command=self.save_file)
        self.save_button.pack(side=tk.LEFT)
        # Create the text widget and the scroll bar
        self.text = tk.Text(self)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Create the scroll bar
        self.scrollbar = tk.Scrollbar(self.text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)
        # Create the line numbers widget
    # Define a function for opening a file
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text.delete('1.0', 'end')
                self.text.insert('end', file.read())


    #a function for saving a file
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text.get('1.0', 'end'))



        # Move the insertion cursor to the beginning of the current line
        current_line = self.text.index(tk.INSERT).split('.')[0]
        self.text.mark_set('insert', f'{current_line}.0')
class IDE(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the two notepads and console
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame to hold the notepads
        notepad_frame = tk.Frame(main_frame)
        notepad_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the first notepad
        self.notepad1 = Notepad(notepad_frame)
        self.notepad1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a separator between the notepads
        separator = tk.Frame(notepad_frame, width=2, bg='gray')
        separator.pack(side=tk.LEFT, fill=tk.Y)


        # Create a frame to hold the console
        console_frame = tk.Frame(main_frame, bg='gray')
        console_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the console widget
        self.console = tk.Text(console_frame, bg='black', fg='white')
        self.console.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



# Create the main tkinter window


# Start the main event loop


class memory_display(tk.Frame):
    def __init__(self,memory, master=None):
        super().__init__(master)
        self.master = master
        self.memory=memory
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.register_display = tk.Text(self, bg='black', fg='white')
        self.register_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_display(self, memory: asm.memory):
        # Convert the numpy array to a nested list
        memory_list = memory.tolist()

        # Convert the list to a string and display it in the register display
        self.register_display.delete('1.0', tk.END)
        self.register_display.insert(tk.END, str(memory_list))
#put the memory display below the notepad
        
root = tk.Tk()
root.geometry('800x600')
app = IDE(root)
full_memory = np.zeros(256, dtype=np.uint8)
memory_display = memory_display(full_memory, root)
memory_display.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
root.mainloop()
