import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def load_users(cls):
        registered_users = {}
        try:
            with open("users.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    username, password = line.strip().split(":")
                    registered_users[username] = password
            return registered_users
        except FileNotFoundError:
            return {}

    @classmethod
    def save_users(cls, users):
        with open("users.txt", "w") as file:
            for username, password in users.items():
                file.write(f"{username}:{password}\n")

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DIARYbytes")
        self.window.rowconfigure(0, minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)

        self.icon_image = tk.PhotoImage(file=r"icon.png")
        self.window.iconphoto(True, self.icon_image)

        self.txt_edit = tk.Text(self.window, bg="black", fg="white", insertbackground="white", font=("Helvetica", 18))
        self.fr_buttons = tk.Frame(self.window, relief=tk.RAISED, bd=2, bg="sky blue")
        self.btn_new = tk.Button(self.fr_buttons, text="New", command=self.new_file)
        self.btn_open = tk.Button(self.fr_buttons, text="Open", command=self.open_file)
        self.btn_save = tk.Button(self.fr_buttons, text="Save As...", command=self.save_file)
        self.btn_exit = tk.Button(self.fr_buttons, text="Exit", command=self.exit_app)

        self.btn_new.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_exit.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.txt_edit.grid(row=0, column=1, sticky="nsew")

    def new_file(self):
        if self.txt_edit.get("1.0", "end-1c"):  # If not empty
            response = tk.messagebox.askyesnocancel(
                "Save Confirmation",
                "Do you want to save your previous work before creating a new file?"
            )
            if response is None:  # If user clicked Cancel
                return
            elif response:  # If user clicked Yes
                self.save_file()

        self.txt_edit.delete(1.0, tk.END)

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txt_edit.insert(tk.END, text)
        self.window.title(f"DIARYbytes - {filepath}")

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get("1.0", "end-1c")
            output_file.write(text)
        self.window.title(f"DIARYbytes - {filepath}")

    def exit_app(self):
        self.window.destroy()

class Login:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("400x300")
        self.login_window.resizable(width=False, height=False)

        self.lbl_welcome = tk.Label(self.login_window, text="Welcome to DIARYbytes", font=("Helvetica", 16), bg="light green")
        self.lbl_welcome.pack(pady=20)

        self.lbl_username = tk.Label(self.login_window, text="Username:")
        self.lbl_username.pack()
        self.entry_username = tk.Entry(self.login_window, width=30)
        self.entry_username.pack(pady=5)

        self.lbl_password = tk.Label(self.login_window, text="Password:")
        self.lbl_password.pack()
        self.entry_password = tk.Entry(self.login_window, width=30, show="*")  # Password field
        self.entry_password.pack(pady=5)

        self.btn_login = tk.Button(self.login_window, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

        self.btn_signup = tk.Button(self.login_window, text="Sign Up", command=self.sign_up)
        self.btn_signup.pack(pady=10)

        self.lbl_status = tk.Label(self.login_window, text="", fg="red")
        self.lbl_status.pack()

        self.login_window.configure(bg="light green")

    def sign_up(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            registered_users = User.load_users()
            if username in registered_users:
                messagebox.showerror("Sign Up Error", "Username already exists. Please choose another.")
            else:
                registered_users[username] = password
                User.save_users(registered_users)
                messagebox.showinfo("Sign Up Successful", "You are now registered. You can log in.")
        else:
            messagebox.showerror("Sign Up Error", "Both username and password are required.")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        registered_users = User.load_users()
        if username in registered_users and password == registered_users[username]:
            self.login_window.destroy()  # Close the login window
            text_editor = TextEditor()
            text_editor.window.mainloop()
        else:
            self.lbl_status.config(text="Login failed. Please try again.", fg="red")

if __name__ == "__main__":
    app = Login()
    app.login_window.mainloop()
