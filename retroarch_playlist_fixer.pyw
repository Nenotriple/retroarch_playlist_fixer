"""

########################################
#                                      #
#      Retroarch Playlist Fixer        #
#                                      #
#   Author  : github.com/Nenotriple    #
#                                      #
########################################

Description:
-------------
This Python script allows you to redefine the "path" and "db_name" in your JSON formatted .lpl files.
It creates a backup of the original file before making any changes.

"path" (Rom Path) is edited by only changing the folder path, it does not change the filename or file extension.

"db_name" will use the same name as the selected ".lpl" file.


"""

################################################################################################################################################
################################################################################################################################################
#region -  Imports


import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText


#endregion
################################################################################################################################################
################################################################################################################################################
#region -  Setup / Interface


class RetroarchPlaylistFixer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Retroarch Playlist Fixer")
        self.root.geometry("600x275")

        self.primary_frame = tk.Frame(self.root)
        self.primary_frame.pack(fill="both", expand=True, padx=4, pady=4)

######### Filename Frame
        self.frame_filename = tk.Frame(self.primary_frame)
        self.frame_filename.pack(fill="x", pady=4)
        # Filename Label
        self.label_filename = tk.Label(self.frame_filename, text="Playlist File:", anchor="w")
        self.label_filename.pack(side="left")
        # Filename Entry
        self.entry_filename = tk.Entry(self.frame_filename)
        self.entry_filename.pack(side="left", padx=4, expand=True, fill="x")
        # Filename Button - Browse
        self.button_filename = tk.Button(self.frame_filename, text="Browse...", command=self.browse_file)
        self.button_filename.pack(side="left")
        self.bind_widget_highlight(self.button_filename)
        # Filename Button - Clear
        self.clear_filename = tk.Button(self.frame_filename, text="X", command=self.clear_file)
        self.clear_filename.pack(side="left")
        self.bind_widget_highlight(self.clear_filename, color='#ffcac9')


######### Foldername Frame
        self.frame_foldername = tk.Frame(self.primary_frame)
        self.frame_foldername.pack(fill="x", pady=4)
        # Foldername Label
        self.label_foldername = tk.Label(self.frame_foldername, text="Rom Path:  ", anchor="w")
        self.label_foldername.pack(side="left")
        # Foldername Entry
        self.entry_foldername = tk.Entry(self.frame_foldername)
        self.entry_foldername.pack(side="left", padx=4, expand=True, fill="x")
        # Foldername button - Browse
        self.button_foldername = tk.Button(self.frame_foldername, text="Browse...", command=self.browse_folder)
        self.button_foldername.pack(side="left")
        self.bind_widget_highlight(self.button_foldername)
        # Foldername button - Clear
        self.clear_foldername = tk.Button(self.frame_foldername, text="X", command=self.clear_folder)
        self.clear_foldername.pack(side="left")
        self.bind_widget_highlight(self.clear_foldername, color='#ffcac9')


        # Run Button
        self.button_run = tk.Button(self.primary_frame, text="Run!", command=self.run_script)
        self.button_run.pack(fill="x")
        self.bind_widget_highlight(self.button_run)

        # Progressbar
        self.progress = ttk.Progressbar(self.primary_frame, length=100, mode='determinate')
        self.progress.pack(fill="x")

        # ScrolledText
        self.scrolled_text = ScrolledText(self.primary_frame)
        self.scrolled_text.insert('end', 'This script sets the "path" and "db_name" of Retroarch playlist files.\n'
                                  '\n"path" (Rom Path) is edited by only changing the folder path, it does not change the filename or file extension.\n'
                                  '\n"db_name" will use the same name as the selected ".lpl" file.')
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.pack(fill="both", expand=True)


#endregion
################################################################################################################################################
################################################################################################################################################
#region -  Primary


    def redefine_path_and_db_name(self, filename, new_path):
        # Backup the original file
        try:
            backup_filename = filename + '.backup'
            shutil.copyfile(filename, backup_filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return

        # Load the JSON data
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}")
            return

        # Update the path and database name
        new_db_name = os.path.basename(filename)
        total_items = len(data['items'])
        for i, item in enumerate(data['items']):
            base_name = os.path.basename(item['path'])
            item['path'] = os.path.join(new_path, base_name)
            item['db_name'] = new_db_name
            self.progress['value'] = (i+1) / total_items * 100
            self.root.update_idletasks()

        # Write the updated data back to the file
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError:
            print(f"Error writing to file {filename}")


    def run_script(self):
        self.progress['value'] = 0
        filename = self.entry_filename.get()
        new_path = self.entry_foldername.get()
        if not new_path.endswith('/'):
            new_path += '/'
        self.redefine_path_and_db_name(filename, new_path)
        self.set_run_button_text()


#endregion
################################################################################################################################################
################################################################################################################################################
#region -  Secondary


    # Used for selecting the Retroarch Playlist file.
    def browse_file(self):
        self.progress['value'] = 0
        filename = filedialog.askopenfilename(filetypes=[("LPL files", "*.lpl")])
        self.entry_filename.delete(0, tk.END)
        self.entry_filename.insert(tk.END, filename)

    def clear_file(self):
        self.entry_filename.delete(0, 'end')


    # Used for selecting the rom path.
    def browse_folder(self):
        self.progress['value'] = 0
        foldername = filedialog.askdirectory()
        if not foldername.endswith('/'):
            foldername += '/'
        self.entry_foldername.delete(0, tk.END)
        self.entry_foldername.insert(tk.END, foldername)

    def clear_folder(self):
        self.entry_foldername.delete(0, 'end')


#endregion
################################################################################################################################################
################################################################################################################################################
#region -  Misc


    # Adjusts the "Run Button" text before and after finishing.
    def set_run_button_text(self):
        self.button_run.config(text="Finished!")
        self.root.after(1500, self.reset_run_button_text)

    def reset_run_button_text(self):
        self.button_run.config(text="Run!")


    # Used for highlighting widgets as the mouse hovers over them.
    def bind_widget_highlight(self, widget, add=False, color=None):
        add = '+' if add else ''
        if color:
            widget.bind("<Enter>", lambda event: self.mouse_enter(event, color), add=add)
        else:
            widget.bind("<Enter>", self.mouse_enter, add=add)
        widget.bind("<Leave>", self.mouse_leave, add=add)

    def mouse_enter(self, event, color='#e5f3ff'):
        if event.widget['state'] == 'normal':
            event.widget['background'] = color

    def mouse_leave(self, event):
        event.widget['background'] = 'SystemButtonFace'


#endregion
################################################################################################################################################
################################################################################################################################################
#region -  Framework


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RetroarchPlaylistFixer()
    app.run()


#endregion


#########################
# Simple script version #
#########################
#
#import json
#import os
#import shutil
#
#def redefine_path_and_db_name(filename, new_path):
#    try:
#        backup_filename = filename + '.backup'
#        shutil.copyfile(filename, backup_filename)
#
#        with open(filename, 'r') as f:
#            data = json.load(f)
#    except FileNotFoundError:
#        print(f"File {filename} not found.")
#        return
#    except json.JSONDecodeError:
#        print(f"Error decoding JSON from {filename}")
#        return
#
#    new_db_name = filename
#
#    for item in data['items']:
#        base_name = os.path.basename(item['path'])
#        item['path'] = os.path.join(new_path, base_name)
#        item['db_name'] = new_db_name
#
#    try:
#        with open(filename, 'w') as f:
#            json.dump(data, f, indent=4)
#    except IOError:
#        print(f"Error writing to file {filename}")
#
#redefine_path_and_db_name(filename='Atari - 2600.lpl', new_path='ux0:data/#Roms/Atari - 2600/')