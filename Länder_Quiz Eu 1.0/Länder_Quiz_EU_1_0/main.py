# Importierte Bibliotheken und ihre Verwendung:
# tkinter (tk): Für die Erstellung der grafischen Benutzeroberfläche (GUI)
# messagebox: Für die Anzeige von Popup-Nachrichten und Dialogen
# PIL (Python Imaging Library): Für die Verarbeitung und Anzeige von Bildern
# json: Für das Lesen der Fragen aus der JSON-Datei
# os: Für Dateisystem-Operationen (z.B. Lock-Datei)
# random: Für die zufällige Auswahl von Fragen
# subprocess: Für das Öffnen von PDF-Dateien
# sys: Für Systemoperationen
# atexit: Für die Ausführung von Funktionen beim Programmende

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import random
import subprocess
import sys
import atexit

# Laden der Fragen aus der JSON-Datei
with open("questions_with_ids.json", "r", encoding="utf-8") as file:
    all_questions = json.load(file)

# Liste zur Verfolgung bereits gestellter Fragen
asked_ids = []

# Definition des Lock-Datei-Pfads
LOCK_FILE = "quiz_running.lock"

def check_already_running():
    if os.path.exists(LOCK_FILE):
        response = messagebox.askyesno(
            "Programm läuft bereits",
            "Eine andere Instanz des Programms läuft bereits.\nMöchten Sie diese beenden und eine neue starten?",
            icon='warning'
        )
        if response:
            try:
                os.remove(LOCK_FILE)
                return False
            except:
                messagebox.showerror(
                    "Fehler",
                    "Konnte die vorherige Instanz nicht beenden. Bitte schließen Sie sie manuell."
                )
                return True
        return True
    return False

def create_lock():
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
    except:
        pass

def remove_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass

## Erste Klasse: Startfenster
class StartWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Länder-Quiz EU 1.0")
        self.master.geometry("800x600")
        self.master.configure(bg="#000000")  # Hintergrundfarbe schwarz
        
        # Setzen des minimalen Fenstergrößen
        self.master.minsize(600, 600)  # Erhöhung der minimalen Höhe auf 600

        # Laden und Setzen der Hintergrundgrafik
        try:
            self.bg_image = Image.open("flage/background.png")
            self.update_background_image()
            
            # Erstellen des Canvas für die Hintergrundgrafik im oberen Bereich
            self.canvas = tk.Canvas(master, width=800, height=150, highlightthickness=0)
            self.canvas.pack(fill="x", expand=False)
            
            # Verbinden des Fenstergröße-Events mit der update_background_image-Methode
            self.master.bind('<Configure>', self.on_resize)
            
            # Erstellen des Hauptrahmens für den Inhalt mit optimalem Platzverteilung
            main_frame = tk.Frame(master, bg="#000000")
            main_frame.pack(fill="both", expand=True)
            
            # Hinzufügen von oben
            tk.Frame(main_frame, height=20, bg="#000000").pack()
            
            # Hinzufügen des Titels
            title_label = tk.Label(main_frame,
                               text="Willkommen zum Länder-Quiz!",
                               font=("Arial", 28, "bold"),
                               fg="#ffffff",  # Textfarbe weiß
                               bg="#000000")
            title_label.pack(pady=(20, 10))
            
            # Hinzufügen des Beschreibungstextes
            desc_label = tk.Label(main_frame,
                              text="Teste dein Wissen über europäische Länder\nund ihre Hauptstädte!",
                              font=("Arial", 16),
                              fg="#ffffff",  # Textfarbe weiß
                              bg="#000000",
                              justify="center")
            desc_label.pack(pady=(10, 30))
            
            # Rahmen für die Buttons
            button_frame = tk.Frame(main_frame, bg="#000000")
            button_frame.pack(fill="x", expand=True, padx=20)
            
            # Start Button
            self.start_button = tk.Button(button_frame,
                                      text="Quiz starten",
                                      font=("Arial", 16, "bold"),
                                      bg="#00796b",
                                      fg="white",
                                      padx=30,
                                      pady=15,
                                      command=self.start_quiz,
                                      cursor="hand2")
            self.start_button.pack(pady=(0, 20))

            # Hilfe Button
            self.help_button = tk.Button(button_frame,
                                     text="📚 Benutzeranleitung",
                                     font=("Arial", 14),
                                     bg="#4fc3f7",
                                     fg="white",
                                     padx=20,
                                     pady=10,
                                     command=self.show_manual,
                                     cursor="hand2")
            self.help_button.pack(pady=(0, 20))
            
            # Hinzufügen von unten
            tk.Frame(main_frame, height=20, bg="#000000").pack()
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            # In Fall der Bild nicht gefunden wird, wird das alte Design verwendet
            self.title_label = tk.Label(master,
                                    text="Willkommen zum Länder-Quiz!",
                                    font=("Arial", 20, "bold"),
                                    bg="#000000",
                                    fg="#ffffff")  # Textfarbe weiß
            self.title_label.pack(pady=40)
            
            self.start_button = tk.Button(master,
                                      text="Quiz starten",
                                      font=("Arial", 14),
                                      bg="#00796b",
                                      fg="white",
                                      padx=20,
                                      pady=10,
                                      command=self.start_quiz)
            self.start_button.pack()

    def start_quiz(self):
        self.master.destroy()
        root = tk.Tk()
        app = QuizWindow(root)
        root.mainloop()

    def show_manual(self):
        # Erstellen einer popup-Fenster für die Auswahl des Dateityps
        dialog = tk.Toplevel(self.master)
        dialog.title("Anleitung öffnen")
        dialog.geometry("400x200")
        dialog.configure(bg="#000000")  # Hintergrundfarbe schwarz
        
        # Center the popup window
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Add title
        title_label = tk.Label(dialog,
                           text="Wie möchtest du die Anleitung lesen?",
                           font=("Arial", 12, "bold"),
                           bg="#000000",
                           fg="#ffffff")  # Textfarbe weiß
        title_label.pack(pady=20)
        
        # Rahmen für die Buttons
        button_frame = tk.Frame(dialog, bg="#000000")
        button_frame.pack(expand=True)
        
        # PDF Button
        pdf_button = tk.Button(button_frame,
                           text="📄 PDF-Version",
                           font=("Arial", 11),
                           bg="#4fc3f7",
                           fg="white",
                           padx=20,
                           pady=10,
                           cursor="hand2",
                           command=lambda: self.open_manual("pdf"))
        pdf_button.pack(side=tk.LEFT, padx=10)
        
        # Text Button
        txt_button = tk.Button(button_frame,
                           text="📝 Text-Version",
                           font=("Arial", 11),
                           bg="#4fc3f7",
                           fg="white",
                           padx=20,
                           pady=10,
                           cursor="hand2",
                           command=lambda: self.open_manual("txt"))
        txt_button.pack(side=tk.LEFT, padx=10)

    def open_manual(self, file_type):
        try:
            filename = f"Benutzeranleitung.{file_type}"
            if os.path.exists(filename):
                if sys.platform == 'win32':
                    os.startfile(filename)
                else:
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.call([opener, filename])
            else:
                # If the required file is not found
                other_file = "Benutzeranleitung.txt" if file_type == "pdf" else "Benutzeranleitung.pdf"
                if os.path.exists(other_file):
                    msg = f"Die {file_type.upper()}-Version wurde nicht gefunden.\nMöchten Sie stattdessen die {'Text' if file_type == 'pdf' else 'PDF'}-Version öffnen?"
                    if messagebox.askyesno("Datei nicht gefunden", msg):
                        self.open_manual("txt" if file_type == "pdf" else "pdf")
                else:
                    messagebox.showerror("Fehler", "Keine Anleitung gefunden!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Die Anleitung konnte nicht geöffnet werden: {str(e)}")

    def update_background_image(self, event=None):
        # Get the current window width
        window_width = self.master.winfo_width()
        if window_width < 100:  # Avoid updating for very small sizes
            return
            
        # Determine the image height while maintaining the aspect ratio
        original_width, original_height = self.bg_image.size
        aspect_ratio = original_height / original_width
        new_height = int(window_width * aspect_ratio)
        
        if new_height > 150:  # Set maximum height
            new_height = 150
            
        # Change the image size
        resized_image = self.bg_image.resize((window_width, new_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        
        # Update the Canvas size and redraw the image
        self.canvas.config(width=window_width, height=new_height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def on_resize(self, event):
        # Delay image update for performance
        if hasattr(self, '_resize_timer'):
            self.master.after_cancel(self._resize_timer)
        self._resize_timer = self.master.after(100, lambda: self.update_background_image())

# The second class: question display interface
class QuizWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Länder-Quiz EU 1.0")
        self.master.geometry("800x900")
        self.master.configure(bg="#000000")  # Hintergrundfarbe schwarz
        
        # Setzen des minimalen Fenstergrößen
        self.master.minsize(800, 850)
        
        # Main container frame
        main_container = tk.Frame(master, bg="#000000")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top frame for question counter
        self.counter_frame = tk.Frame(main_container, bg="#000000")
        self.counter_frame.pack(fill="x", pady=(0, 20))
        
        # Question counter
        self.question_counter = tk.Label(self.counter_frame,
                                    text="Frage: 1 / 80 | Richtig: 0 | Falsch: 0",
                                    font=("Arial", 12),
                                    bg="#000000",
                                    fg="#ffffff")  # Textfarbe weiß
        self.question_counter.pack(side="left")
        
        # End button
        self.quit_button = tk.Button(self.counter_frame,
                                 text="Quiz beenden",
                                 font=("Arial", 12),
                                 bg="#ff5252",
                                 fg="white",
                                 command=self.show_results,
                                 cursor="hand2")
        self.quit_button.pack(side="right")
        
        # Question frame
        self.question_frame = tk.Frame(main_container, bg="#000000")
        self.question_frame.pack(fill="both", expand=True)
        
        # Question label
        self.question_label = tk.Label(self.question_frame,
                                   text="Wie heißt dieses Land?",
                                   font=("Arial", 24, "bold"),
                                   bg="#000000",
                                   fg="#ffffff")  # Textfarbe weiß
        self.question_label.pack(pady=(0, 30))
        
        # Image frame with white border
        self.image_frame = tk.Frame(self.question_frame, bg="#ffffff", bd=2)  
        self.image_frame.pack(pady=(0, 30))
        
        # Answer frame
        self.answers_frame = tk.Frame(self.question_frame, bg="#000000")
        self.answers_frame.pack(fill="x", padx=50)
        
        # Bottom frame for next button
        bottom_frame = tk.Frame(main_container, bg="#000000")
        bottom_frame.pack(fill="x", side="bottom", pady=(20, 0))
        
        # Next button
        self.next_button = tk.Button(bottom_frame,
                                 text="Nächste Frage",
                                 font=("Arial", 14),
                                 bg="#00796b",
                                 fg="white",  # Textfarbe weiß
                                 padx=20,
                                 pady=10,
                                 command=self.load_question,
                                 cursor="hand2")
        self.next_button.pack()
        
        self.score_right = 0
        self.score_wrong = 0
        self.current_question = None

        self.load_question()

    def load_question(self):
        self.clear_buttons()
        if len(asked_ids) == len(all_questions):
            self.show_results()
            return

        self.clear_image()  

        while True:
            q = random.choice(all_questions)
            if q["id"] not in asked_ids:
                self.current_question = q
                asked_ids.append(q["id"])
                break

        self.question_label.config(text=q["question"], fg="#ffffff") 
        self.display_image(q["image"])
        self.update_counters()

        # Speichern der Antwort-Buttons
        self.answer_buttons = []
        
        # Create answer buttons with consistent styling
        for choice in q["choices"]:
            btn = tk.Button(self.answers_frame, text=choice, font=("Arial", 12),
                          width=40, height=2,  # Made buttons larger
                          bg="#e0f7fa", # Light blue background
                          cursor="hand2",
                          command=lambda c=choice: self.check_answer(c))
            btn.pack(pady=5)
            self.answer_buttons.append(btn) # Button in der Liste speichern

# Deaktivieren des "Nächste Frage"-Buttons bis eine Antwort ausgewählt wurde
        self.next_button.config(state="disabled")

    def clear_buttons(self):
        for widget in self.answers_frame.winfo_children():
            widget.destroy()
        self.question_label.config(text="")

    def clear_image(self):
        # Löschen der vorherigen Bildschirm
        if hasattr(self, 'image_label'):
            self.image_label.destroy()

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((400, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label = tk.Label(self.image_frame, image=photo, bg="#000000") # Schwarzer Hintergrund für das Bild
            self.image_label.image = photo
            self.image_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label = tk.Label(self.image_frame,
                                    text="Bild nicht gefunden\nBitte überprüfen Sie den Bildpfad",
                                    image="",
                                    fg="#ff0000",  # Textrot für Fehler
                                    font=("Arial", 12),
                                    bg="#000000")
            self.image_label.pack(pady=10)

    def check_answer(self, selected):
      # Deaktivieren aller Antwort-Buttons
        for btn in self.answer_buttons:
            btn.config(state="disabled")
            if btn.cget("text") == selected:
                btn.config(bg="#aaaaaa")  # Ändern Sie die Farbe des ausgewählten Buttons in grau

        correct = self.current_question["answer"]
        if selected == correct:
            self.score_right += 1
            self.question_label.config(text="✅ Richtig!", fg="#00ff00")
        else:
            self.score_wrong += 1
            self.question_label.config(text=f"❌ Falsch! Richtig war: {correct}", fg="#ff0000")
        
        # Aktivieren des "Nächste Frage"-Buttons
        self.next_button.config(state="normal")
        
        self.update_counters()

    def show_results(self):
        self.master.destroy()
        root = tk.Tk()
        # Weiterleiten der Anzahl der beantworteten Fragen
        answered_questions = len(asked_ids)
        ResultWindow(root, self.score_right, self.score_wrong, answered_questions)
        root.mainloop()

    def update_counters(self):
        total = len(asked_ids)
        self.question_counter.config(text=f"Frage: {total} / {len(all_questions)} | Richtig: {self.score_right} | Falsch: {self.score_wrong}")

# The third class: results interface
class ResultWindow:
    def __init__(self, master, score_right, score_wrong, answered_questions):
        self.master = master
        self.master.title("Länder-Quiz EU 1.0")
        self.master.geometry("500x600")
        self.master.configure(bg="#000000")  # Schwarzer Hintergrund
        
        # Setzen des minimalen Fenstergrößen
        self.master.minsize(400, 500)
        
        # Main container frame
        main_frame = tk.Frame(self.master, bg="#000000")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(main_frame,
                      text="Dein Ergebnis",
                      font=("Arial", 32, "bold"),
                      bg="#000000",
                      fg="#ffffff")
        title.pack(pady=(0, 40))
        
        # Anzahl der beantworteten Fragen
        total_questions = len(all_questions)
        questions_label = tk.Label(main_frame,
                               text=f"Du hast {answered_questions} von {total_questions} Fragen beantwortet.",
                               font=("Arial", 14),
                               bg="#000000",
                               fg="#ffffff")  # Textfarbe weiß
        questions_label.pack(pady=(0, 20))
        
        # Right answers
        right_label = tk.Label(main_frame,
                           text=f"Richtige Antworten: {score_right}",
                           font=("Arial", 14),
                           fg="#00ff00",  # Textfarbe grün
                           bg="#000000")
        right_label.pack(pady=5)
        
        # Wrong answers
        wrong_label = tk.Label(main_frame,
                           text=f"Falsche Antworten: {score_wrong}",
                           font=("Arial", 14),
                           fg="#ff0000",  # Textfarbe rot
                           bg="#000000")
        wrong_label.pack(pady=5)
        
        # Success rate
        success_rate = (score_right / answered_questions * 100) if answered_questions > 0 else 0
        rate_label = tk.Label(main_frame,
                          text=f"Erfolgsquote: {success_rate:.1f}%",
                          font=("Arial", 16, "bold"),
                          bg="#000000",
                          fg="#ffffff")  # Textfarbe weiß
        rate_label.pack(pady=(20, 30))
        
        # Motivational message
        message = self.get_motivation_message(success_rate)
        motivation_label = tk.Label(main_frame,
                             text=message,
                             font=("Arial", 14),
                             fg="#00796b",
                             bg="#000000")
        motivation_label.pack(pady=(0, 40))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#000000")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Restart button
        restart_button = tk.Button(button_frame,
                               text="Quiz erneut starten",
                               font=("Arial", 12),
                               bg="#00796b",
                               fg="white",
                               padx=20,
                               pady=10,
                               command=self.restart_quiz,
                               cursor="hand2")
        restart_button.pack(side=tk.LEFT, padx=10)
        
        # End button
        quit_button = tk.Button(button_frame,
                            text="Beenden",
                            font=("Arial", 12),
                            bg="#ff5252",
                            fg="white",
                            padx=20,
                            pady=10,
                            command=self.master.destroy,
                            cursor="hand2")
        quit_button.pack(side=tk.RIGHT, padx=10)

    def get_motivation_message(self, success_rate):
        if success_rate >= 80:
            return "Super gemacht! "
        elif success_rate >= 50:
            return "Gut gemacht, du kannst noch besser werden! "
        else:
            return "Du solltest mehr üben! "

    def restart_quiz(self):
        global asked_ids
        asked_ids = [] # Zurücksetzen der Liste der gestellten Fragen
        self.master.destroy()
        root = tk.Tk()
        app = StartWindow(root)
        root.mainloop()

# Start the program
if __name__ == "__main__":
    if check_already_running():
        sys.exit(1)
        
    create_lock()
    atexit.register(remove_lock)  # Register function to delete lock file on program exit
    
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()
    
    remove_lock()  # Delete lock file on program exit
