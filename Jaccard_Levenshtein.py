import tkinter as tk
from sklearn.metrics import jaccard_score

def chuoi_dauvao(text):
    return text.lower().split()

def tinhdotuongdong_jaccard(vanban_1, vanban_2):
    chuoi_1 = chuoi_dauvao(vanban_1)
    chuoi_2 = chuoi_dauvao(vanban_2)

    try:
        dotuongdong_jaccard = jaccard_score(chuoi_1, chuoi_2, average='micro')
    except ValueError:
        dotuongdong_jaccard = 0.0

    tugiongnhau = set(chuoi_1) & set(chuoi_2)
    tukhacnhau_vb1 = set(chuoi_1) - set(chuoi_2)
    tukhacnhau_vb2 = set(chuoi_2) - set(chuoi_1)

    return dotuongdong_jaccard, tugiongnhau, tukhacnhau_vb1, tukhacnhau_vb2

def khoangcach_levenshtein(a, b):
    dodai_vb1, dodai_vb2 = len(a), len(b)

    dp = [[0] * (dodai_vb2 + 1) for _ in range(dodai_vb1 + 1)]

    for i in range(dodai_vb1 + 1):
        for j in range(dodai_vb2 + 1):
            dp[i][j] = j if i == 0 else (i if j == 0 else min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1)))

    return dp[dodai_vb1][dodai_vb2]

def tinhdotuongdong_levenshtein(vanban_1, vanban_2):
    khoangcach = khoangcach_levenshtein(vanban_1, vanban_2)
    chuoidainhat = max(len(vanban_1), len(vanban_2))
    dotuongdong = 1 - (khoangcach / chuoidainhat)

    return dotuongdong, set(vanban_1.lower().split()) & set(vanban_2.lower().split()), set(vanban_1.lower().split()) - set(vanban_2.lower().split()), set(vanban_2.lower().split()) - set(vanban_1.lower().split())

def hienthiketqua_jaccard():
    vanban_1 = entry_vanban_1.get("1.0", "end-1c")
    vanban_2 = entry_vanban_2.get("1.0", "end-1c")

    dotuongdong_jaccard, tugiongnhau, tukhacnhau_vb1, tukhacnhau_vb2 = tinhdotuongdong_jaccard(vanban_1, vanban_2)

    result_label.config(text=f"Độ tương đồng Jaccard: {dotuongdong_jaccard:.2f}")
    tugiongnhau_label.config(text=f"Số từ giống nhau: {len(tugiongnhau)}")
    tukhacnhau_vb1_label.config(text=f"Số từ khác nhau trong văn bản 1: {len(tukhacnhau_vb1)}")
    tukhacnhau_vb2_label.config(text=f"Số từ khác nhau trong văn bản 2: {len(tukhacnhau_vb2)}")

    tuxuathien_entry.delete(0, tk.END)

def hienthiketqua_levenshtein():
    vanban_1 = entry_vanban_1.get("1.0", "end-1c")
    vanban_2 = entry_vanban_2.get("1.0", "end-1c")

    ketqua_levenshtein = tinhdotuongdong_levenshtein(vanban_1, vanban_2)
    dotuongdong_levenshtein = ketqua_levenshtein[0]
    tugiongnhau_levenshtein = ketqua_levenshtein[1]
    tukhacnhau_vb1_levenshtein = ketqua_levenshtein[2]
    tukhacnhau_vb2_levenshtein = ketqua_levenshtein[3]

    diemkitu_vb1, diemkitu_vb2 = len(vanban_1), len(vanban_2)

    tugiongnhau = set(vanban_1.lower().split()) & set(vanban_2.lower().split())
    tukhacnhau_vb1 = set(vanban_1.lower().split()) - set(vanban_2.lower().split())
    tukhacnhau_vb2 = set(vanban_2.lower().split()) - set(vanban_1.lower().split())

    result_label.config(text=f"Độ tương đồng Levenshtein: {dotuongdong_levenshtein:.2f}")
    tugiongnhau_label.config(text=f"Số từ giống nhau: {len(tugiongnhau_levenshtein)}")
    tukhacnhau_vb1_label.config(text=f"Số từ khác nhau trong văn bản 1: {len(tukhacnhau_vb1_levenshtein)}")
    tukhacnhau_vb2_label.config(text=f"Số từ khác nhau trong văn bản 2: {len(tukhacnhau_vb2_levenshtein)}")
    diemkitu_label.config(text=f"Số kí tự trong văn bản:\nVăn bản 1: {diemkitu_vb1}, Văn bản 2: {diemkitu_vb2}")

def kiemtratuxuathien():
    tucankiemtra = tuxuathien_entry.get()
    vanban_1, vanban_2 = entry_vanban_1.get("1.0", tk.END), entry_vanban_2.get("1.0", tk.END)
    diem_vb1 = chuoi_dauvao(vanban_1).count(tucankiemtra)
    diem_vb2 = chuoi_dauvao(vanban_2).count(tucankiemtra)
    ketqua_tuxuathien_label.config(text=f"Số lần từ '{tucankiemtra}' xuất hiện:\nVăn bản 1: {diem_vb1}, Văn bản 2: {diem_vb2}")

def xoadulieu():
    entry_vanban_1.delete("1.0", tk.END)
    entry_vanban_2.delete("1.0", tk.END)
    result_label.config(text="")
    tugiongnhau_label.config(text="")
    tukhacnhau_vb1_label.config(text="")
    tukhacnhau_vb2_label.config(text="")
    tuxuathien_entry.delete(0, tk.END)
    ketqua_tuxuathien_label.config(text="")
    diemkitu_label.config(text="")

root = tk.Tk()
root.title("Đánh giá sự tương đồng văn bản")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_vanban_1 = tk.Label(frame_input, text="Văn bản 1:")
label_vanban_1.grid(row=0, column=0, pady=5)
entry_vanban_1 = tk.Text(frame_input, width=70, height=10)
entry_vanban_1.grid(row=1, column=0, padx=10)

label_vanban_2 = tk.Label(frame_input, text="Văn bản 2:")
label_vanban_2.grid(row=2, column=0, pady=5)
entry_vanban_2 = tk.Text(frame_input, width=70, height=10)
entry_vanban_2.grid(row=3, column=0, padx=10)

jaccard_button = tk.Button(root, text="Tính độ tương đồng Jaccard", command=hienthiketqua_jaccard)
jaccard_button.pack(pady=5)

levenshtein_button = tk.Button(root, text="Tính độ tương đồng Levenshtein", command=hienthiketqua_levenshtein)
levenshtein_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"))
result_label.pack()

tugiongnhau_label = tk.Label(root, text="")
tugiongnhau_label.pack()

tukhacnhau_vb1_label = tk.Label(root, text="")
tukhacnhau_vb1_label.pack()

tukhacnhau_vb2_label = tk.Label(root, text="")
tukhacnhau_vb2_label.pack()

diemkitu_label = tk.Label(root, text="")
diemkitu_label.pack()

frame_tuxuathien = tk.Frame(root)
frame_tuxuathien.pack(pady=10)

tuxuathien_label = tk.Label(frame_tuxuathien, text="Kiểm tra từ xuất hiện:")
tuxuathien_label.grid(row=0, column=0)
tuxuathien_entry = tk.Entry(frame_tuxuathien, width=30)
tuxuathien_entry.grid(row=0, column=1)

kiemtratuxuathien_button = tk.Button(frame_tuxuathien, text="Kiểm tra", command=kiemtratuxuathien)
kiemtratuxuathien_button.grid(row=0, column=2, padx=10)

ketqua_tuxuathien_label = tk.Label(frame_tuxuathien, text="")
ketqua_tuxuathien_label.grid(row=1, column=0, columnspan=3)

xoa_button = tk.Button(root, text="Xóa dữ liệu", command=xoadulieu)
xoa_button.pack(pady=10)

root.mainloop()