from gui.main_window import MainWindow
import customtkinter as ctk


def main():
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
