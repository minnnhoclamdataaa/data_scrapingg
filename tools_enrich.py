import os
import tkinter as tk
import subprocess
import sys

def run_app():
    domain = domain_var.get()
    domain_link = domain.replace(" ", "+")
    day_from = day_from_var.get()
    day_to = day_to_var.get()

    # Thực thi tệp tin google_tun.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    google_tun_path = os.path.join(current_dir, 'google_tun.py')
    subprocess.Popen([sys.executable, google_tun_path, domain_link, day_from, day_to])
    
    # Đóng cửa sổ ứng dụng
    window.destroy()

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Google Tools")

# Tạo các nhãn và hộp nhập thông tin
label_name = tk.Label(window, text="Tên cần search:")
label_name.pack()
domain_var = tk.StringVar()
entry_name = tk.Entry(window, textvariable=domain_var)
entry_name.pack()

label_departure = tk.Label(window, text="Ngày bắt đầu (Ví dụ : 05/20/23):")
label_departure.pack()
day_from_var = tk.StringVar()
entry_departure = tk.Entry(window, textvariable=day_from_var)
entry_departure.pack()

label_arrival = tk.Label(window, text="Ngày kết thúc (Ví dụ 05/25/23):")
label_arrival.pack()
day_to_var = tk.StringVar()
entry_arrival = tk.Entry(window, textvariable=day_to_var)
entry_arrival.pack()

# Tạo nút "Run"
button_run = tk.Button(window, text="Run", command=run_app)
button_run.pack()

def close_app():
    window.destroy()

# Tạo nút "Close"
button_close = tk.Button(window, text="Close", command=close_app)
button_close.pack()

# Bắt đầu vòng lặp chờ sự kiện của giao diện
window.mainloop()
