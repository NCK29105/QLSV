import json
from typing import List, Dict
import os

# Lớp cơ sở Nguoi (Trừu tượng)
class Nguoi:
    def __init__(self, ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt):
        self.__ho_ten = ho_ten
        self.__ngay_sinh = ngay_sinh
        self.__gioi_tinh = gioi_tinh
        self.__que_quan = que_quan
        self.__email = email
        self.__sdt = sdt

    # Getter/Setter sử dụng property
    @property
    def ho_ten(self):
        return self.__ho_ten

    @ho_ten.setter
    def ho_ten(self, value):
        self.__ho_ten = value

    @property
    def ngay_sinh(self):
        return self.__ngay_sinh

    @ngay_sinh.setter
    def ngay_sinh(self, value):
        self.__ngay_sinh = value

    @property
    def gioi_tinh(self):
        return self.__gioi_tinh

    @gioi_tinh.setter
    def gioi_tinh(self, value):
        self.__gioi_tinh = value

    @property
    def que_quan(self):
        return self.__que_quan

    @que_quan.setter
    def que_quan(self, value):
        self.__que_quan = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def sdt(self):
        return self.__sdt

    @sdt.setter
    def sdt(self, value):
        self.__sdt = value

# Lớp Student kế thừa từ Nguoi
class Student(Nguoi):
    def __init__(self, ma_so, ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt, chuyen_nganh, nien_khoa):
        super().__init__(ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt)
        self.__ma_so = ma_so
        self.__chuyen_nganh = chuyen_nganh
        self.__nien_khoa = nien_khoa

    @property
    def ma_so(self):
        return self.__ma_so

    @ma_so.setter
    def ma_so(self, value):
        self.__ma_so = value

    @property
    def chuyen_nganh(self):
        return self.__chuyen_nganh

    @chuyen_nganh.setter
    def chuyen_nganh(self, value):
        self.__chuyen_nganh = value

    @property
    def nien_khoa(self):
        return self.__nien_khoa

    @nien_khoa.setter
    def nien_khoa(self, value):
        self.__nien_khoa = value

    # Hiển thị thông tin dạng chuỗi
    def __str__(self):
        return f"{self.ma_so} - {self.ho_ten} - {self.ngay_sinh} - {self.gioi_tinh} - {self.que_quan} - {self.email} - {self.sdt} - {self.chuyen_nganh} - {self.nien_khoa}"

    # Chuyển đối tượng thành dict để lưu file
    def to_dict(self):
        return {
            "ma_so": self.ma_so,
            "ho_ten": self.ho_ten,
            "ngay_sinh": self.ngay_sinh,
            "gioi_tinh": self.gioi_tinh,
            "que_quan": self.que_quan,
            "email": self.email,
            "sdt": self.sdt,
            "chuyen_nganh": self.chuyen_nganh,
            "nien_khoa": self.nien_khoa
        }

    # Chuyển từ dict thành đối tượng Student
    @staticmethod
    def from_dict(data):
        return Student(
            data["ma_so"], data["ho_ten"], data["ngay_sinh"], data.get("gioi_tinh", ""),
            data["que_quan"], data.get("email", ""), data.get("sdt", ""),
            data["chuyen_nganh"], data["nien_khoa"]
        )

# Lớp quản lý danh sách sinh viên
class StudentList:
    def __init__(self):
        self.ds: List[Student] = []

    # Thêm sinh viên vào danh sách
    def them(self, sv: Student):
        self.ds.append(sv)

    # Sửa thông tin sinh viên dựa trên mã số
    def sua(self, ma_so, ho_ten, ngay_sinh, gioi_tinh, que_quan, email, sdt, chuyen_nganh, nien_khoa):
        for sv in self.ds:
            if sv.ma_so == ma_so:
                sv.ho_ten = ho_ten
                sv.ngay_sinh = ngay_sinh
                sv.gioi_tinh = gioi_tinh
                sv.que_quan = que_quan
                sv.email = email
                sv.sdt = sdt
                sv.chuyen_nganh = chuyen_nganh
                sv.nien_khoa = nien_khoa

    # Xoá sinh viên theo mã số
    def xoa(self, ma_so):
        self.ds = [sv for sv in self.ds if sv.ma_so != ma_so]

    # Tìm kiếm sinh viên theo mã số hoặc họ tên
    def tim(self, tu_khoa):
        return [sv for sv in self.ds if tu_khoa.lower() in sv.ma_so.lower() or tu_khoa.lower() in sv.ho_ten.lower()]

    # Sắp xếp danh sách theo họ tên
    def sap_xep(self):
        self.ds.sort(key=lambda sv: sv.ho_ten)

    # Lưu danh sách ra file JSON
    def luu_file(self, tenfile: str):
        with open(tenfile, "w", encoding="utf-8") as f:
            json.dump([sv.to_dict() for sv in self.ds], f, ensure_ascii=False, indent=4)

    # Đọc danh sách từ file JSON
    def doc_file(self, tenfile: str):
        try:
            with open(tenfile, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.ds = [Student.from_dict(d) for d in data]
        except FileNotFoundError:
            self.ds = []

    # Thống kê số lượng sinh viên theo chuyên ngành
    def thong_ke_theo_chuyen_nganh(self):
        tk: Dict[str, List[Student]] = {}
        for sv in self.ds:
            tk.setdefault(sv.chuyen_nganh, []).append(sv)
        return tk

    # Thống kê số lượng sinh viên theo niên khóa
    def thong_ke_theo_nien_khoa(self):
        tk: Dict[int, List[Student]] = {}
        for sv in self.ds:
            tk.setdefault(sv.nien_khoa, []).append(sv)
        return tk
