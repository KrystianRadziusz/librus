import customtkinter as ctk
from tkinter import messagebox
from schedule_module import add_entry, get_schedule, clear_schedule, export_schedule_pdf
from gradebook_module import add_grade, get_grades, clear_grades, export_grades_pdf
from stats_module import export_stats_pdf

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

SUBJECTS = ["Polski","Angielski","Matematyka","Fizyka","Biologia","Chemia","W-F","Geografia","Historia"]
DAYS     = ["Poniedzialek","Wtorek","Sroda","Czwartek","Piatek"]
HOURS    = [f"{h}:00" for h in range(8,19)]
GRADES   = ["1","2","3","4","5","6"]

class App(ctk.CTk):
    """Główne okno aplikacji: trzy zakładki – Plan Lekcji, Dziennik Ocen, Statystyki."""
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.title("Niezbednik ucznia")
        self.geometry("800x600")

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=40, pady=40)

        tabs = ctk.CTkTabview(frame, width=700, height=500)
        tabs.pack(expand=True, fill="both")
        for name in ("Plan Lekcji","Dziennik Ocen","Statystyki"):
            tabs.add(name)

        self._build_schedule_tab(tabs.tab("Plan Lekcji"))
        self._build_gradebook_tab(tabs.tab("Dziennik Ocen"))
        self._build_stats_tab(tabs.tab("Statystyki"))

    def _build_schedule_tab(self, tab):
        """Zakładka Plan Lekcji: dodawanie/wyczyszczenie wpisu i eksport PDF."""
        form = ctk.CTkFrame(tab)
        form.pack(pady=(20,10))

        ctk.CTkLabel(form, text="Przedmiot:").grid(row=0,column=0,sticky="e",padx=5,pady=5)
        self.subject_var = ctk.StringVar(value=SUBJECTS[0])
        ctk.CTkOptionMenu(form,values=SUBJECTS,variable=self.subject_var).grid(row=0,column=1,padx=5,pady=5)

        ctk.CTkLabel(form, text="Dzien:").grid(row=1,column=0,sticky="e",padx=5,pady=5)
        self.day_var = ctk.StringVar(value=DAYS[0])
        ctk.CTkOptionMenu(form,values=DAYS,variable=self.day_var).grid(row=1,column=1,padx=5,pady=5)

        ctk.CTkLabel(form, text="Godzina:").grid(row=2,column=0,sticky="e",padx=5,pady=5)
        self.time_var = ctk.StringVar(value=HOURS[0])
        ctk.CTkOptionMenu(form,values=HOURS,variable=self.time_var).grid(row=2,column=1,padx=5,pady=5)

        ctk.CTkButton(form,text="Dodaj",command=self._on_add_schedule).grid(row=3,column=0,sticky="we",pady=(10,0),ipadx=10)
        ctk.CTkButton(form,text="Wyczysc plan",fg_color="#E94560",hover_color="#D32F2F",
                      command=self._on_clear_schedule).grid(row=3,column=1,sticky="we",pady=(10,0),ipadx=10)

        self.schedule_frame = ctk.CTkScrollableFrame(tab,width=650,height=220)
        self.schedule_frame.pack(pady=10)
        self._refresh_schedule_list()

        ctk.CTkButton(tab,text="Eksport PDF",command=lambda: export_schedule_pdf(self.user_id,"plan.pdf")).pack(pady=(0,20))

    def _on_add_schedule(self):
        """Dodaje wpis do planu lekcji i odświeża listę."""
        add_entry(self.user_id, self.day_var.get(), self.time_var.get(), self.subject_var.get())
        messagebox.showinfo("OK","Dodano wpis do planu lekcji")
        self._refresh_schedule_list()

    def _on_clear_schedule(self):
        """Czyści cały plan lekcji po potwierdzeniu."""
        if messagebox.askyesno("Potwierdz","Czy na pewno wyczyscic plan lekcji?"):
            clear_schedule(self.user_id)
            messagebox.showinfo("OK","Plan lekcji zostal wyczyszczony")
            self._refresh_schedule_list()

    def _refresh_schedule_list(self):
        """Pobiera i wyświetla wszystkie wpisy planu lekcji użytkownika."""
        for w in self.schedule_frame.winfo_children():
            w.destroy()
        for e in get_schedule(self.user_id):
            ctk.CTkLabel(self.schedule_frame, text=f"{e.day} {e.time} – {e.subject}", anchor="w").pack(fill="x", pady=2, padx=5)

    def _build_gradebook_tab(self, tab):
        """Zakładka Dziennik Ocen: dodawanie, czyszczenie ocen i eksport PDF."""
        form = ctk.CTkFrame(tab)
        form.pack(pady=(20,10))

        ctk.CTkLabel(form, text="Przedmiot:").grid(row=0,column=0,sticky="e",padx=5,pady=5)
        self.gr_subj_var = ctk.StringVar(value=SUBJECTS[0])
        ctk.CTkOptionMenu(form,values=SUBJECTS,variable=self.gr_subj_var).grid(row=0,column=1,padx=5,pady=5)

        ctk.CTkLabel(form, text="Ocena:").grid(row=1,column=0,sticky="e",padx=5,pady=5)
        self.gr_score_var = ctk.StringVar(value=GRADES[0])
        ctk.CTkOptionMenu(form,values=GRADES,variable=self.gr_score_var).grid(row=1,column=1,padx=5,pady=5)

        ctk.CTkButton(form,text="Dodaj",command=self._on_add_grade).grid(row=2,column=0,sticky="we",pady=(10,0),ipadx=10)
        ctk.CTkButton(form,text="Wyczysc oceny",fg_color="#E94560",hover_color="#D32F2F",
                      command=self._on_clear_grades).grid(row=2,column=1,sticky="we",pady=(10,0),ipadx=10)

        self.grades_frame = ctk.CTkScrollableFrame(tab,width=650,height=220)
        self.grades_frame.pack(pady=10)
        self._refresh_grades_list()

        ctk.CTkButton(tab,text="Eksportuj PDF",command=lambda: export_grades_pdf(self.user_id,"oceny.pdf")).pack(pady=(0,20))

    def _on_add_grade(self):
        """Dodaje ocenę i odświeża widok ocen."""
        add_grade(self.user_id, self.gr_subj_var.get(), float(self.gr_score_var.get()))
        messagebox.showinfo("OK","Dodano ocene")
        self._refresh_grades_list()

    def _on_clear_grades(self):
        """Czyści wszystkie oceny użytkownika po potwierdzeniu."""
        if messagebox.askyesno("Potwierdz","Czy na pewno wyczyscic oceny?"):
            clear_grades(self.user_id)
            messagebox.showinfo("OK","Dziennik ocen zostal wyczyszczony")
            self._refresh_grades_list()

    def _refresh_grades_list(self):
        """Wyświetla oceny pogrupowane po przedmiocie w jednym wierszu."""
        for w in self.grades_frame.winfo_children():
            w.destroy()
        grades = get_grades(self.user_id)
        grouped = {}
        for g in grades:
            grouped.setdefault(g.subject, []).append(str(int(g.score)) if g.score.is_integer() else str(g.score))
        for subject, scores in grouped.items():
            ctk.CTkLabel(self.grades_frame, text=f"{subject}: " + ", ".join(scores), anchor="w").pack(fill="x", pady=2, padx=5)

    def _build_stats_tab(self, tab):
        """Zakładka Statystyki: średnie oceny (per przedmiot i łączna)."""
        grades = get_grades(self.user_id)
        per_subject = {}
        for g in grades:
            per_subject.setdefault(g.subject, []).append(g.score)
        sub_avg = {subj: sum(vals)/len(vals) for subj, vals in per_subject.items()}

        if sub_avg:
            overall = sum(sub_avg.values())/len(sub_avg)
            lines = [f"{subj}: {avg:.2f}" for subj, avg in sub_avg.items()] + [f"Srednia laczna: {overall:.2f}"]
            display = "\n".join(lines)
        else:
            display = "Brak ocen do analizy"

        ctk.CTkLabel(tab, text=display, justify="left").pack(pady=40)
        ctk.CTkButton(tab,text="Eksport PDF",command=lambda: export_stats_pdf(self.user_id,"statystyki.pdf")).pack(pady=(0,20))
