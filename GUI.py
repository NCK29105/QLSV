import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from StudentManagement import Student, StudentList

# Giao diện chính quản lý sinh viên
class StudentGUI:
    def __init__(self, root, role='sinhvien', username=''):
        # Thiết lập cửa sổ và khởi tạo danh sách sinh viên
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Quản lý sinh viên")
        self.role = role
        self.username = username

        self.ds = StudentList()
        self.ds.doc_file("students.json")

        self.create_widgets()
        self.hien_thi_danh_sach()

    # Tạo giao diện nhập liệu và bảng hiển thị
    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X)

        left_frame = tk.Frame(top_frame)
        left_frame.pack(side=tk.LEFT, padx=50, anchor='n')

        right_frame = tk.Frame(top_frame)
        right_frame.pack(side=tk.RIGHT, padx=50, anchor='n')

        labels = [
            "Mã số sinh viên", "Họ tên", "Ngày sinh", "Giới tính", "Quê quán",
            "Email", "Số điện thoại", "Chuyên ngành", "Niên khóa"
        ]

        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(left_frame, text=label).grid(row=i, column=0, padx=5, pady=3, sticky='e')

            if label == "Chuyên ngành":
                self.entries[label] = ttk.Combobox(left_frame, values=["BCSE", "BJS", "ECE", "ESAS", "FTH", "MJM"], state="readonly", width=27)
                self.entries[label].current(0)
            elif label == "Giới tính":
                self.entries[label] = ttk.Combobox(left_frame, values=["Nam", "Nữ"], state="readonly", width=27)
                self.entries[label].current(0)
            else:
                self.entries[label] = tk.Entry(left_frame, width=30)

            self.entries[label].grid(row=i, column=1, padx=5, pady=3)

        button_texts = [
            ("Thêm", self.them_sv),
            ("Sửa", self.sua_sv),
            ("Xóa", self.xoa_sv),
            ("Tìm kiếm", self.tim_kiem),
            ("Thống kê ngành", self.thong_ke_nganh),
            ("Thống kê niên khóa", self.thong_ke_nien_khoa),
            ("Lưu", self.luu_file),
            ("Xuất CSV", self.xuat_csv)
        ]

        self.restricted_buttons = []

        for text, command in button_texts:
            btn = tk.Button(right_frame, text=text, width=20, command=command)
            btn.pack(pady=2)
            if text in ["Thêm", "Sửa", "Xóa", "Lưu"]:
                self.restricted_buttons.append(btn)

            # Ẩn hoặc khóa các chức năng nếu không phải admin hoặc giảng viên
        if self.role not in ["admin", "giangvien"]:
            for btn in self.restricted_buttons:
                btn.config(state="disabled")


        # ----------------------------
        # Nút tài khoản (hiển thị popup tài khoản)
        # ----------------------------
        tk.Button(right_frame, text="Tài khoản", width=20, command=self.mo_popup_tai_khoan).pack(pady=10)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            bottom_frame,
            columns=("stt", "ma_so", "ho_ten", "ngay_sinh", "gioi_tinh", "que_quan", "email", "sdt", "chuyen_nganh", "nien_khoa"),
            show='headings'
        )

        headers = {
            "stt": "STT",
            "ma_so": "Mã số sinh viên",
            "ho_ten": "Họ tên",
            "ngay_sinh": "Ngày sinh",
            "gioi_tinh": "Giới tính",
            "que_quan": "Quê quán",
            "email": "Email",
            "sdt": "Số điện thoại",
            "chuyen_nganh": "Chuyên ngành",
            "nien_khoa": "Niên khóa"
        }

        for col in self.tree["columns"]:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, anchor=tk.CENTER, width=130)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def get_entry_data(self):
        try:
            return Student(
                self.entries["Mã số sinh viên"].get(),
                self.entries["Họ tên"].get(),
                self.entries["Ngày sinh"].get(),
                self.entries["Giới tính"].get(),
                self.entries["Quê quán"].get(),
                self.entries["Email"].get(),
                self.entries["Số điện thoại"].get(),
                self.entries["Chuyên ngành"].get(),
                int(self.entries["Niên khóa"].get())
            )
        except ValueError:
            messagebox.showerror("Lỗi", "Niên khóa phải là số nguyên.")
            return None

    def them_sv(self):
        for entry in self.entries.values():
            if entry.get().strip() == "":
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
                return
        sv = self.get_entry_data()
        if sv:
            self.ds.them(sv)
            self.hien_thi_danh_sach()

    def sua_sv(self):
        for entry in self.entries.values():
            if entry.get().strip() == "":
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
                return
        sv = self.get_entry_data()
        if sv:
            self.ds.sua(sv.ma_so, sv.ho_ten, sv.ngay_sinh, sv.gioi_tinh,
                        sv.que_quan, sv.email, sv.sdt, sv.chuyen_nganh, sv.nien_khoa)
            self.hien_thi_danh_sach()

    def xoa_sv(self):
        if self.entries["Mã số sinh viên"].get().strip() == "":
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã số sinh viên.")
            return
        ma_so = self.entries["Mã số sinh viên"].get()
        self.ds.xoa(ma_so)
        self.hien_thi_danh_sach()

    def tim_kiem(self):
        tu_khoa = self.entries["Mã số sinh viên"].get()
        ket_qua = self.ds.tim(tu_khoa)
        self.tree.delete(*self.tree.get_children())
        ket_qua.sort(key=lambda sv: sv.ho_ten.split()[-1].lower())
        for idx, sv in enumerate(ket_qua, start=1):
            self.tree.insert("", tk.END, values=(idx, sv.ma_so, sv.ho_ten, sv.ngay_sinh, sv.gioi_tinh, sv.que_quan, sv.email, sv.sdt, sv.chuyen_nganh, sv.nien_khoa))

    def hien_thi_danh_sach(self):
        self.tree.delete(*self.tree.get_children())
        self.ds.ds.sort(key=lambda sv: sv.ho_ten.split()[-1].lower())
        for idx, sv in enumerate(self.ds.ds, start=1):
            self.tree.insert("", tk.END, values=(idx, sv.ma_so, sv.ho_ten, sv.ngay_sinh, sv.gioi_tinh, sv.que_quan, sv.email, sv.sdt, sv.chuyen_nganh, sv.nien_khoa))

    def thong_ke_nganh(self):
        if not self.ds.ds:
            messagebox.showwarning("Thông báo", "Không có sinh viên để thống kê.")
            return
        tk_nganh = self.ds.thong_ke_theo_chuyen_nganh()
        msg = ""
        for nganh, svs in tk_nganh.items():
            msg += f"{nganh}: {len(svs)} sinh viên\n"
        messagebox.showinfo("Thống kê theo chuyên ngành", msg)

    def thong_ke_nien_khoa(self):
        if not self.ds.ds:
            messagebox.showwarning("Thông báo", "Không có sinh viên để thống kê.")
            return
        tk_nk = self.ds.thong_ke_theo_nien_khoa()
        msg = ""
        for nk, svs in tk_nk.items():
            msg += f"{nk}: {len(svs)} sinh viên\n"
        messagebox.showinfo("Thống kê theo niên khóa", msg)

    def luu_file(self):
        self.ds.luu_file("students.json")
        messagebox.showinfo("Thông báo", "Đã lưu thành công.")

    def xuat_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Chọn nơi lưu danh sách CSV"
        )
        if file_path:
            try:
                with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["STT", "Mã số", "Họ tên", "Ngày sinh", "Giới tính", "Quê quán", "Email", "SĐT", "Chuyên ngành", "Niên khóa"])
                    for idx, sv in enumerate(self.ds.ds, start=1):
                        writer.writerow([
                            idx,
                            sv.ma_so,
                            sv.ho_ten,
                            sv.ngay_sinh,
                            sv.gioi_tinh,
                            sv.que_quan,
                            sv.email,
                            sv.sdt,
                            sv.chuyen_nganh,
                            sv.nien_khoa
                        ])
                messagebox.showinfo("Thông báo", "Xuất danh sách CSV thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file: {e}")

    # ----------------------------
    # Hiển thị cửa sổ popup tài khoản
    # ----------------------------
    def mo_popup_tai_khoan(self):
        popup = tk.Toplevel(self.root)
        popup.title("Tài khoản")
        popup.geometry("300x200")
        popup.grab_set()

        # Nút Thông tin tài khoản ở đầu tiên
        tk.Button(popup, text="Thông tin tài khoản", width=25, command=self.thong_tin_tai_khoan).pack(pady=5)
        tk.Button(popup, text="Đăng xuất", width=25, command=self.dang_xuat).pack(pady=5)


    # ----------------------------
    # Hiển thị thông tin tài khoản
    # ----------------------------
    def thong_tin_tai_khoan(self):
        messagebox.showinfo("Thông tin tài khoản", f"Bạn đang đăng nhập với tư cách: {self.role}")

    # ----------------------------
    # Đăng xuất và quay lại đăng nhập
    # ----------------------------
    def dang_xuat(self):
        self.root.destroy()
        import Main
        Main.restart_app()
