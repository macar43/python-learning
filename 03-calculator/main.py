# ============================================
# Taschenrechner mit GUI (tkinter)
# ============================================

import tkinter as tk
from tkinter import messagebox

class Calculator:
    """Taschenrechner-Klasse mit GUI"""
    
    def __init__(self, root):
        """Initialisiert die GUI"""
        self.root = root
        self.root.title("🧮 Taschenrechner")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Variable für die aktuelle Eingabe
        self.expression = ""
        
        # Erstelle die GUI
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle GUI-Elemente"""
        
        # ===== Display (Anzeigefeld) =====
        self.display = tk.Entry(
            self.root,
            font=("Arial", 20),
            borderwidth=2,
            relief="solid",
            justify="right"
        )
        self.display.pack(padx=10, pady=10, fill="both", ipady=10)
        
        # ===== Buttons-Frame =====
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Button-Layout (4x4 Grid)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "⌫", "√", "^"]
        ]
        
        # Erstelle jeden Button
        for row_idx, row in enumerate(buttons):
            for col_idx, button_text in enumerate(row):
                self.create_button(
                    button_frame,
                    button_text,
                    row_idx,
                    col_idx
                )
    
    def create_button(self, parent, text, row, col):
        """Erstellt einen einzelnen Button"""
        
        # Button-Style
        if text == "=":
            bg_color = "#4CAF50"  # Grün
            fg_color = "white"
        elif text in ["/", "*", "-", "+", "^", "√"]:
            bg_color = "#FF9800"  # Orange
            fg_color = "white"
        elif text in ["C", "⌫"]:
            bg_color = "#f44336"  # Rot
            fg_color = "white"
        else:
            bg_color = "#e0e0e0"  # Grau
            fg_color = "black"
        
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 18, "bold"),
            bg=bg_color,
            fg=fg_color,
            command=lambda: self.on_button_click(text),
            relief="raised",
            padx=20,
            pady=20
        )
        button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    def on_button_click(self, char):
        """Verarbeitet Button-Klicks"""
        
        if char == "=":
            self.calculate()
        elif char == "C":
            self.clear()
        elif char == "⌫":
            self.backspace()
        elif char == "√":
            self.sqrt()
        elif char == "^":
            self.expression += "**"
            self.update_display()
        else:
            # Normale Zahlen und Operatoren
            self.expression += str(char)
            self.update_display()
    
    def update_display(self):
        """Aktualisiert das Anzeigefeld"""
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
    
    def calculate(self):
        """Berechnet das Ergebnis"""
        try:
            # Eval wertet mathematische Ausdrücke aus
            result = eval(self.expression)
            
            # Runde auf 10 Dezimalstellen
            if isinstance(result, float):
                result = round(result, 10)
            
            self.expression = str(result)
            self.update_display()
        
        except ZeroDivisionError:
            messagebox.showerror("Fehler", "❌ Division durch Null nicht erlaubt!")
            self.clear()
        
        except SyntaxError:
            messagebox.showerror("Fehler", "❌ Ungültiger mathematischer Ausdruck!")
            self.clear()
        
        except Exception as e:
            messagebox.showerror("Fehler", f"❌ Fehler: {str(e)}")
            self.clear()
    
    def clear(self):
        """Löscht alles"""
        self.expression = ""
        self.update_display()
    
    def backspace(self):
        """Löscht das letzte Zeichen"""
        self.expression = self.expression[:-1]
        self.update_display()
    
    def sqrt(self):
        """Berechnet Quadratwurzel"""
        try:
            result = float(self.expression) ** 0.5
            self.expression = str(round(result, 10))
            self.update_display()
        except:
            messagebox.showerror("Fehler", "❌ Kann Quadratwurzel nicht berechnen!")
            self.clear()

def main():
    """Hauptfunktion - startet die Anwendung"""
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

# ============================================
# Programm starten
# ============================================
if __name__ == "__main__":
    main()