import tkinter as tk
from tkinter import messagebox, ttk
import json

class LoginWindow:
    def __init__(self, root):
        self.login_win = tk.Toplevel(root)
        self.login_win.title("Login")
        self.login_win.geometry("1200x600")  
        self.root = root
        self.username = None
        self.show_password = False

        # Tạo Frame để canh giữa
        main_frame = tk.Frame(self.login_win)
        main_frame.place(relx=0.5, rely=0.4, anchor='center')

        # Label và entry: Tên đăng nhập
        tk.Label(main_frame, text="Tên Đăng Nhập:", font=("Arial", 12)).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.entry_user = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        # Label và entry: Mật khẩu + nút xem
        tk.Label(main_frame, text="Mật Khẩu:", font=("Arial", 12)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.entry_pass = tk.Entry(main_frame, show="*", font=("Arial", 12), width=30)
        self.entry_pass.grid(row=1, column=1, padx=10, pady=10)

        self.btn_xem = tk.Button(main_frame, text="Xem", width=5, command=self.toggle_password)
        self.btn_xem.grid(row=1, column=2, padx=5)

        # Label và combobox: Tư cách đăng nhập
        tk.Label(main_frame, text="Tư cách đăng nhập:", font=("Arial", 12)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.role_combo = ttk.Combobox(main_frame, values=["Sinh viên", "Giảng viên", "Admin"], state="readonly", width=28, font=("Arial", 12))
        self.role_combo.grid(row=2, column=1, padx=10, pady=10)
        self.role_combo.current(0)

        # Nút: Đăng nhập và Quên mật khẩu
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=3, column=1, pady=20)

        self.btn_login = tk.Button(btn_frame, text="Đăng nhập", width=15, command=self.dang_nhap)
        self.btn_login.pack(side=tk.LEFT, padx=10)

        self.btn_forgot = tk.Button(btn_frame, text="Quên mật khẩu", width=15, command=self.thong_bao_quen)
        self.btn_forgot.pack(side=tk.LEFT, padx=10)

    def toggle_password(self):
        self.show_password = not self.show_password
        self.entry_pass.config(show="" if self.show_password else "*")
        self.btn_xem.config(text="Ẩn" if self.show_password else "Xem")

    def thong_bao_quen(self):
        messagebox.showinfo("Quên mật khẩu", "Vui lòng liên hệ Admin để cung cấp lại mật khẩu.")

    def dang_nhap(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        role_raw = self.role_combo.get()

        role_map = {
            "Sinh viên": "sinhvien",
            "Giảng viên": "giangvien",
            "Admin": "admin"
        }
        role = role_map.get(role_raw, "")

        try:
            with open("accounts.json", "r", encoding="utf-8") as f:
                accounts = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file tài khoản.")
            return

        for acc in accounts:
            if acc["username"] == username and acc["password"] == password and acc["role"] == role:
                messagebox.showinfo("Thành công", f"Đăng nhập thành công với tư cách: {role_raw}")
                self.root.role = role
                self.root.username = username  # Để dùng trong GUI
                self.login_win.destroy()
                return

        messagebox.showerror("Lỗi", "Tên đăng nhập, mật khẩu hoặc tư cách không đúng.")

# ----------------------------
# Hàm đổi mật khẩu từ GUI.py gọi
# ----------------------------
def doi_mat_khau(username, old_pass, new_pass, confirm_pass):
    try:
        with open("accounts.json", "r", encoding="utf-8") as f:
            accounts = json.load(f)

        found = False
        for acc in accounts:
            if acc["username"] == username:
                found = True
                if acc["password"] != old_pass:
                    return False, "Mật khẩu cũ không đúng."
                if new_pass != confirm_pass:
                    return False, "Xác nhận mật khẩu không khớp."
                acc["password"] = new_pass
                break

        if not found:
            return False, "Tài khoản không tồn tại."

        with open("accounts.json", "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=4, ensure_ascii=False)

        return True, "Đổi mật khẩu thành công."

    except Exception as e:
        return False, f"Lỗi: {e}"
