import customtkinter as ctk
from tkinter import messagebox
import auth
from gui import App

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

def center(win, width, height):
    """Wyśrodkowuje okno `win` na ekranie o zadanych wymiarach."""
    win.update_idletasks()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

class MainMenu(ctk.CTk):
    """Główne okno z przyciskami Logowanie i Rejestracja."""
    def __init__(self):
        super().__init__()
        self.title("Niezbednik Ucznia")
        center(self, 400, 250)

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkButton(frame, text="Login", command=self._open_login).pack(pady=15, ipadx=10)
        ctk.CTkButton(frame, text="Rejestracja", command=self._open_register).pack(pady=15, ipadx=10)

    def _open_login(self):
        """Otwiera okno logowania; po poprawnym logowaniu uruchamia `App`."""
        win = ctk.CTkToplevel(self)
        win.title("Logowanie")
        center(win, 350, 240)
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(win, text="Uzytkownik:").pack(pady=(20,5))
        user = ctk.CTkEntry(win)
        user.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(win, text="Haslo:").pack(pady=5)
        pwd = ctk.CTkEntry(win, show="*")
        pwd.pack(pady=5, padx=20, fill="x")

        def do_login():
            ok, res = auth.login(user.get(), pwd.get())
            if ok:
                win.destroy()
                self.destroy()
                App(res).mainloop()
            else:
                messagebox.showerror("Blad", res)

        ctk.CTkButton(win, text="Zaloguj", command=do_login).pack(pady=20, ipadx=10)
        win.protocol("WM_DELETE_WINDOW", lambda: (win.grab_release(), win.destroy()))

    def _open_register(self):
        """Otwiera okno rejestracji; po pomyślnej rejestracji wraca do menu."""
        win = ctk.CTkToplevel(self)
        win.title("Rejestracja")
        center(win, 380, 300)
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(win, text="Uzytkownik:").pack(pady=(20,5))
        user = ctk.CTkEntry(win)
        user.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(win, text="Haslo:").pack(pady=5)
        pwd = ctk.CTkEntry(win, show="*")
        pwd.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(win, text="Powtorz haslo:").pack(pady=5)
        pwd2 = ctk.CTkEntry(win, show="*")
        pwd2.pack(pady=5, padx=20, fill="x")

        def do_register():
            if pwd.get() != pwd2.get():
                return messagebox.showwarning("Uwaga", "Hasla sie nie zgadzaja")
            ok, res = auth.register(user.get(), pwd.get())
            if ok:
                messagebox.showinfo("Rejestracja", "Zarejestrowano")
                win.grab_release()
                win.destroy()
            else:
                messagebox.showerror("Rejestracja", res)

        ctk.CTkButton(win, text="Zarejestruj", command=do_register).pack(pady=20, ipadx=10)
        win.protocol("WM_DELETE_WINDOW", lambda: (win.grab_release(), win.destroy()))

if __name__ == "__main__":
    MainMenu().mainloop()
