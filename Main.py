import tkinter as tk
from LoginWindow import LoginWindow
from GUI import StudentGUI

def restart_app():
    root = tk.Tk()
    root.withdraw()
    login = LoginWindow(root)
    root.wait_window(login.login_win)

    if hasattr(root, 'role'):
        root.deiconify()
        app = StudentGUI(root, role=root.role, username=login.username)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    login = LoginWindow(root)
    root.wait_window(login.login_win)

    if hasattr(root, 'role'):
        root.deiconify()
        app = StudentGUI(root, role=root.role, username=login.username)
        root.mainloop()
