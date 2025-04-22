# Import thư viện tkinter để tạo GUI
import tkinter as tk

# Import cửa sổ đăng nhập và giao diện chính từ các file khác
from LoginWindow import LoginWindow
from GUI import StudentGUI

# Hàm để khởi động lại ứng dụng (sử dụng khi đăng xuất)
def restart_app():
    # Tạo cửa sổ gốc
    root = tk.Tk()
    # Ẩn cửa sổ chính khi chưa đăng nhập
    root.withdraw()

    # Mở cửa sổ đăng nhập
    login = LoginWindow(root)
    # Đợi cho đến khi cửa sổ đăng nhập đóng lại
    root.wait_window(login.login_win)

    # Nếu sau đăng nhập có gán thuộc tính role (tức là đăng nhập thành công)
    if hasattr(root, 'role'):
        # Hiển thị lại cửa sổ chính
        root.deiconify()
        # Khởi tạo giao diện quản lý sinh viên với quyền và tài khoản tương ứng
        app = StudentGUI(root, role=root.role, username=login.username)
        # Bắt đầu vòng lặp giao diện
        root.mainloop()

# Hàm main của chương trình
if __name__ == "__main__":
    # Tạo cửa sổ gốc
    root = tk.Tk()
    # Ẩn cửa sổ chính ban đầu
    root.withdraw()

    # Mở giao diện đăng nhập
    login = LoginWindow(root)
    root.wait_window(login.login_win)

    # Nếu đăng nhập thành công thì hiển thị giao diện chính
    if hasattr(root, 'role'):
        root.deiconify()
        app = StudentGUI(root, role=root.role, username=login.username)
        root.mainloop()
