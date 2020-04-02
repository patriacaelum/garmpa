import tkinter as tk

from gui import Garmpa


def main():
    root = tk.Tk()
    root.title("garmpa")

    garmpa = Garmpa(master=root)

    root.mainloop()


if __name__ == "__main__":
    main()
