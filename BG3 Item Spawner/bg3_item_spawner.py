import sys
import os
import pyperclip
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import time

# --- Import pywinauto ---
try:
    from pywinauto import application, findwindows, keyboard
except ImportError:
    print("Error: pywinauto library is not installed. Please install it using: pip install pywinauto")
    sys.exit(1)

# Read data from a text file
def read_data(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

# Create a dictionary from the data
def create_uuid_data(data):
    uuid_data = {}
    lines = data.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            parts = line.rsplit(' (', 1)
            if len(parts) == 2:
                uuid = parts[0]
                in_game_name = parts[1][:-1]  # Remove closing parenthesis
                uuid_data[in_game_name] = uuid
    return uuid_data

# Function to search and retrieve UUIDs
def search_uuids(uuid_data, search_term):
    matching_uuids = []
    for name, uuid in uuid_data.items():
        if search_term.lower() in name.lower():
            matching_uuids.append((name, uuid))
    return matching_uuids

class UUIDSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baldur's Gate 3 Item Spawner")

        # Try to set the icon, but don't crash if it fails
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bg3_icon.ico')
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print(f"Warning: Could not load icon from {icon_path}")

        self.create_widgets()

    def create_widgets(self):
        self.root.configure(background="#2C3E50")

        main_frame = ttk.Frame(self.root, padding="10 10 10 10", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.search_label = ttk.Label(main_frame, text="Search for item:", style="Title.TLabel")
        self.search_label.pack(pady=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(main_frame, textvariable=self.search_var, justify='center', font=("Segoe UI", 12))
        self.search_entry.pack(fill=tk.X, pady=(0, 10))

        self.result_frame = ttk.Frame(main_frame, style="Results.TFrame")
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_listbox = tk.Listbox(self.result_frame, font=("Segoe UI", 11), bg="#34495E", fg="white", selectbackground="#E74C3C")
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_listbox.config(yscrollcommand=scrollbar.set)

        self.copy_button = ttk.Button(main_frame, text="Spawn Item", command=self.copy_and_paste_uuid, style="Copy.TButton")
        self.copy_button.pack(pady=(10, 0))

        self.root.geometry("350x400")
        self.root.resizable(False, False)
        self.center_window()

        self.search_var.trace("w", self.perform_search)
        self.search_entry.bind("<Return>", lambda event: self.copy_and_paste_uuid())
        self.result_listbox.bind("<Double-1>", lambda event: self.copy_and_paste_uuid())

        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Main.TFrame", background="#2C3E50")
        style.configure("Results.TFrame", background="#2C3E50")
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background="#2C3E50", foreground="#ECF0F1")
        style.configure("Copy.TButton", font=("Segoe UI", 12), background="#E74C3C", foreground="white")
        style.map("Copy.TButton",
                  background=[('active', '#C0392B')],
                  foreground=[('active', 'white')])

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.root.geometry(f"+{x}+{y}")

    def perform_search(self, *args):
        self.result_listbox.delete(0, tk.END)
        search_term = self.search_var.get().lower()

        matching_results = search_uuids(uuid_data, search_term)
        for name, _ in matching_results:
            self.result_listbox.insert(tk.END, name)

    def copy_and_paste_uuid(self):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_item = self.result_listbox.get(selected_index[0])
            selected_uuid = uuid_data[selected_item]
            selected_uuid = selected_uuid.split('"', 1)[1].split('"')[0]

            quantity = simpledialog.askinteger("Quantity", "Enter quantity:", initialvalue=1, minvalue=1, parent=self.root)

            if quantity:
                formatted_string = f'TemplateAddTo("{selected_uuid}", GetHostCharacter(), {quantity})'
                pyperclip.copy(formatted_string)

                # --- pywinauto code to paste into BG3 Console ---
                console_title = "BG3 Script Extender Debug Console"

                try:
                    app = application.Application().connect(title=console_title)
                    window = app.window(title=console_title)
                    window.set_focus()
                    time.sleep(0.1)
                    keyboard.send_keys("{ENTER}{ENTER}")
                    time.sleep(0.1)
                    keyboard.send_keys("^v{ENTER}")
                except findwindows.ElementNotFoundError:
                    messagebox.showerror("Error", f"Could not find {console_title}. Please make sure it's open.", parent=self.root)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while pasting to Script Extender Console: {e}")
                # --- end pywinauto code ---

            else:
                messagebox.showwarning("No Quantity", "Please enter a quantity.", parent=self.root)
        else:
            messagebox.showwarning("No Selection", "Please select an item from the list.", parent=self.root)

if __name__ == "__main__":
    try:
        # Load data from file
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        filename = os.path.join(script_directory, 'uuid_data.txt')

        data = read_data(filename)
        if data is None:
            print(f"Error: File '{filename}' not found.")
            messagebox.showerror("Error", f"File '{filename}' not found.")
            exit(1)

        uuid_data = create_uuid_data(data)

        # Create the main window
        root = tk.Tk()
        app = UUIDSearchApp(root)

        # Start the Tkinter event loop
        root.mainloop()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")