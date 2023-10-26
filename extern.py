import tkinter as tk
from tkinter import ttk
import ttkthemes
import sqlite3
import time
from icecream import ic

db = "/tmp/external_requests.db"


def external_request(floor, direction):
    # direction   1: up  -1: down
    con = sqlite3.connect(db)
    cur = con.cursor()
    # cur.execute("DROP TABLE IF EXISTS requests;")
    cur.execute("CREATE TABLE IF NOT EXISTS requests(floor, direction);")
    res = cur.execute(f"SELECT * FROM requests WHERE floor = {floor} AND direction = {direction};")
    if res.fetchone() is None:
        cur.execute(f"INSERT INTO requests (floor, direction) VALUES ({floor}, {direction})")
    con.commit()  # don't forget the commit after an insert
    con.close()


def runtime():
    for _ in range(10):
        start = time.time()
        for n in range(1):
            external_request(n, 1)
        end = time.time()
        print(f'{(end - start) * 1_000:5.3f} ms', end='  ')
    exit(0)


def extern_gui():
    root = tk.Tk()
    root.title("EXTERN")
    root.geometry("350x800")

    label_4 = tk.Label(root, text="\nFloor 4")
    label_4.pack()
    # up_4 = tk.Button(root, text="△", state="disabled", command=lambda: external_request(4, 1))
    # up_4.pack()
    down_4 = tk.Button(root, text="▽", command=lambda: external_request(4, -1))
    down_4.pack()

    label_3 = tk.Label(root, text="\nFloor 3")
    label_3.pack()
    up_3 = tk.Button(root, text="△", command=lambda: external_request(3, 1))
    up_3.pack()
    down_3 = tk.Button(root, text="▽", command=lambda: external_request(3, -1))
    down_3.pack()

    label_2 = tk.Label(root, text="\nFloor 2")
    label_2.pack()
    up_2 = tk.Button(root, text="△", command=lambda: external_request(2, 1))
    up_2.pack()
    down_2 = tk.Button(root, text="▽", command=lambda: external_request(2, -1))
    down_2.pack()

    label_1 = tk.Label(root, text="\nFloor 1")
    label_1.pack()
    up_1 = tk.Button(root, text="△", command=lambda: external_request(1, -1))
    up_1.pack()
    down_1 = tk.Button(root, text="▽", command=lambda: external_request(1, 1))
    down_1.pack()

    label_0 = tk.Label(root, pady=20, text="\nFloor 0")
    label_0.pack()
    up_0 = tk.Button(root, text="△", command=lambda: external_request(0, 1))
    up_0.pack()
    # down_0 = tk.Button(root, text="▽", state="disabled", command= lambda: external_request(0, -1))
    # down_0.pack()

    root.mainloop()


def ttk_themes():
    # source: https://stackoverflow.com/questions/62649613/tk-and-ttk-looks-very-different-is-possibly-to-make-ttk-looks-like-tk import tkinter as tk from tkinter import ttk import ttkthemes
    root = tk.Tk()
    root.style = ttkthemes.ThemedStyle()
    for i, name in enumerate(sorted(root.style.theme_names())):
        b = ttk.Button(root, text=name, command=lambda name: root.style.theme_use(name))
        b.pack(fill='x')
    root.mainloop()


def say(txt):
    print(f"{txt}")


def items():
    # tk-Elemente haben wesentlich mehr direkte Konfigurationsmöglichkeiten
    # ttk-Elemente erhalten das Aussehen über css
    root = tk.Tk()
    root.title("main window")
    root.geometry("350x750")
    answer = input("Select: 1 - tk   2 - ttk  ==> ")
    match answer:
        case "1":
            button1 = tk.Button(root, text="Klick mich!",
                                state="normal",  # normal, disabled
                                pady=20,  # button size
                                command=lambda: say("Ich bin ein tk.Button"))
            button1.pack(pady=50)  # pady: padding
            button2 = tk.Button(root, text="Klick mich!",
                                state="normal",  # normal, disabled
                                pady=0,  # button size
                                command=lambda: say("Ich bin ein tk.Button"))
            button2.pack()  # pady: padding
            button3 = tk.Button(root, text="Klick mich!",
                                state="normal",  # normal, disabled
                                command=lambda: say("Ich bin ein tk.Button"))
            button3.pack()  # pady: padding
        case "2":
            button1 = ttk.Button(root, text="Klick mich!", state="disabled", padding=50,
                                 command=lambda: say("Ich bin ein ttk.Button"))
            button1.pack()  # no padding here!
    for item in button1.keys():
        print(f"{item}: {button1[item]}")
    root.mainloop()


if __name__ == "__main__":
    extern_gui()
    # ttk_themes()
    # items()
