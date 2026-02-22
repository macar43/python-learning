# ============================================
# Quiz-App mit SQLite Datenbank
# ============================================

import sqlite3
import json
from datetime import datetime

class QuizDatabase:
    """Verwaltet die SQLite Datenbank"""
    
    def __init__(self, db_name="quiz.db"):
        """Initialisiert die Datenbank"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Verbinde mit der Datenbank"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Erstelle Tabellen falls nicht vorhanden"""
        
        # Tabelle für Fragen
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabelle für Spielergebnisse
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def add_question(self, question, opt_a, opt_b, opt_c, opt_d, correct):
        """Fügt eine neue Frage zur Datenbank hinzu (CREATE)"""
        try:
            self.cursor.execute("""
                INSERT INTO questions 
                (question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (question, opt_a, opt_b, opt_c, opt_d, correct))
            self.conn.commit()
            print(f"✅ Frage hinzugefügt!")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Hinzufügen: {e}")
            return False
    
    def get_all_questions(self):
        """Ruft alle Fragen ab (READ)"""
        self.cursor.execute("SELECT * FROM questions")
        return self.cursor.fetchall()
    
    def get_question_by_id(self, q_id):
        """Ruft eine Frage nach ID ab"""
        self.cursor.execute("SELECT * FROM questions WHERE id = ?", (q_id,))
        return self.cursor.fetchone()
    
    def update_question(self, q_id, question, opt_a, opt_b, opt_c, opt_d, correct):
        """Aktualisiert eine Frage (UPDATE)"""
        try:
            self.cursor.execute("""
                UPDATE questions 
                SET question = ?, option_a = ?, option_b = ?, 
                    option_c = ?, option_d = ?, correct_answer = ?
                WHERE id = ?
            """, (question, opt_a, opt_b, opt_c, opt_d, correct, q_id))
            self.conn.commit()
            print(f"✅ Frage #{q_id} aktualisiert!")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Aktualisieren: {e}")
            return False
    
    def delete_question(self, q_id):
        """Löscht eine Frage (DELETE)"""
        try:
            self.cursor.execute("DELETE FROM questions WHERE id = ?", (q_id,))
            self.conn.commit()
            print(f"✅ Frage #{q_id} gelöscht!")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Löschen: {e}")
            return False
    
    def save_result(self, player_name, score, total):
        """Speichert Spielergebnis"""
        percentage = (score / total) * 100 if total > 0 else 0
        try:
            self.cursor.execute("""
                INSERT INTO results 
                (player_name, score, total_questions, percentage)
                VALUES (?, ?, ?, ?)
            """, (player_name, score, total, percentage))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
            return False
    
    def get_leaderboard(self, limit=10):
        """Ruft Top-Spieler ab"""
        self.cursor.execute("""
            SELECT player_name, score, total_questions, percentage, played_at
            FROM results
            ORDER BY percentage DESC, score DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()
    
    def close(self):
        """Schließt die Datenbankverbindung"""
        self.conn.close()

class QuizApp:
    """Hauptanwendung für das Quiz"""
    
    def __init__(self):
        """Initialisiert die Quiz-App"""
        self.db = QuizDatabase()
        self.load_sample_questions()
    
    def load_sample_questions(self):
        """Lädt Beispielfragen wenn Datenbank leer ist"""
        questions = self.db.get_all_questions()
        
        if len(questions) == 0:
            print("📝 Lade Beispielfragen...\n")
            
            sample_questions = [
                {
                    "question": "Welche Programmiersprache ist am weitesten verbreitet?",
                    "a": "Python",
                    "b": "JavaScript",
                    "c": "Java",
                    "d": "C++",
                    "correct": "b"
                },
                {
                    "question": "Was ist die Hauptstadt von Frankreich?",
                    "a": "Lyon",
                    "b": "Marseille",
                    "c": "Paris",
                    "d": "Toulouse",
                    "correct": "c"
                },
                {
                    "question": "In welchem Jahr wurde Python erfunden?",
                    "a": "1989",
                    "b": "1991",
                    "c": "1995",
                    "d": "2000",
                    "correct": "b"
                },
                {
                    "question": "Welcher Planet ist der größte in unserem Sonnensystem?",
                    "a": "Saturn",
                    "b": "Jupiter",
                    "c": "Neptune",
                    "d": "Uranus",
                    "correct": "b"
                },
                {
                    "question": "Wer hat die Relativitätstheorie entwickelt?",
                    "a": "Isaac Newton",
                    "b": "Albert Einstein",
                    "c": "Galileo Galilei",
                    "d": "Stephen Hawking",
                    "correct": "b"
                }
            ]
            
            for q in sample_questions:
                self.db.add_question(
                    q["question"], q["a"], q["b"], q["c"], q["d"], q["correct"]
                )
            print("✅ 5 Beispielfragen geladen!\n")
    
    def play_quiz(self):
        """Startet ein Quiz-Spiel"""
        questions = self.db.get_all_questions()
        
        if len(questions) == 0:
            print("❌ Keine Fragen in der Datenbank!")
            return
        
        player_name = input("Dein Name: ").strip()
        if not player_name:
            print("❌ Name kann nicht leer sein!")
            return
        
        print(f"\n🎮 Quiz gestartet, {player_name}!\n")
        
        score = 0
        
        for i, question in enumerate(questions, 1):
            q_id, q_text, opt_a, opt_b, opt_c, opt_d, correct, _ = question
            
            print(f"Frage {i}/{len(questions)}: {q_text}")
            print(f"A) {opt_a}")
            print(f"B) {opt_b}")
            print(f"C) {opt_c}")
            print(f"D) {opt_d}")
            
            answer = input("Deine Antwort (A/B/C/D): ").strip().upper()
            
            if answer not in ["A", "B", "C", "D"]:
                print("❌ Ungültige Eingabe!\n")
                continue
            
            if answer == correct.upper():
                print("✅ Richtig!\n")
                score += 1
            else:
                print(f"❌ Falsch! Richtig war: {correct.upper()}\n")
        
        # Ergebnis speichern
        percentage = (score / len(questions)) * 100
        self.db.save_result(player_name, score, len(questions))
        
        print("="*50)
        print(f"🎉 Quiz beendet!")
        print(f"Spieler: {player_name}")
        print(f"Punkte: {score}/{len(questions)}")
        print(f"Prozent: {percentage:.1f}%")
        print("="*50 + "\n")
    
    def show_leaderboard(self):
        """Zeigt die Top 10 Spieler"""
        results = self.db.get_leaderboard(10)
        
        if len(results) == 0:
            print("📭 Noch keine Ergebnisse!\n")
            return
        
        print("\n🏆 LEADERBOARD - Top 10")
        print("="*60)
        
        for i, (name, score, total, percentage, date) in enumerate(results, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"{medal} {name:20} {score}/{total} ({percentage:.1f}%) - {date}")
        
        print("="*60 + "\n")
    
    def manage_questions(self):
        """Menü zum Verwalten von Fragen"""
        
        while True:
            print("\n📚 FRAGEN VERWALTEN")
            print("1. Alle Fragen anzeigen")
            print("2. Frage hinzufügen")
            print("3. Frage aktualisieren")
            print("4. Frage löschen")
            print("5. Zurück zum Hauptmenü")
            
            choice = input("Wahl (1-5): ").strip()
            
            if choice == "1":
                questions = self.db.get_all_questions()
                if len(questions) == 0:
                    print("📭 Keine Fragen!")
                else:
                    print("\n📋 ALLE FRAGEN:")
                    for q in questions:
                        print(f"ID: {q[0]} - {q[1]}")
                print()
            
            elif choice == "2":
                print("\n➕ NEUE FRAGE HINZUFÜGEN")
                question = input("Frage: ").strip()
                opt_a = input("Option A: ").strip()
                opt_b = input("Option B: ").strip()
                opt_c = input("Option C: ").strip()
                opt_d = input("Option D: ").strip()
                correct = input("Richtige Antwort (A/B/C/D): ").strip().upper()
                
                if correct in ["A", "B", "C", "D"]:
                    self.db.add_question(question, opt_a, opt_b, opt_c, opt_d, correct)
                else:
                    print("❌ Ungültige Antwort!")
                print()
            
            elif choice == "3":
                questions = self.db.get_all_questions()
                if len(questions) == 0:
                    print("📭 Keine Fragen!")
                else:
                    q_id = int(input("Frage ID zum Aktualisieren: "))
                    question = input("Neue Frage: ").strip()
                    opt_a = input("Option A: ").strip()
                    opt_b = input("Option B: ").strip()
                    opt_c = input("Option C: ").strip()
                    opt_d = input("Option D: ").strip()
                    correct = input("Richtige Antwort (A/B/C/D): ").strip().upper()
                    
                    self.db.update_question(q_id, question, opt_a, opt_b, opt_c, opt_d, correct)
                print()
            
            elif choice == "4":
                q_id = int(input("Frage ID zum Löschen: "))
                self.db.delete_question(q_id)
                print()
            
            elif choice == "5":
                break
            
            else:
                print("❌ Ungültige Eingabe!")
    
    def main_menu(self):
        """Hauptmenü"""
        
        while True:
            print("="*50)
            print("🧠 QUIZ-APP MIT DATENBANK")
            print("="*50)
            print("1. 🎮 Quiz spielen")
            print("2. 🏆 Leaderboard anzeigen")
            print("3. 📚 Fragen verwalten")
            print("4. 🚪 Beenden")
            print("="*50)
            
            choice = input("Wahl (1-4): ").strip()
            
            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.show_leaderboard()
            elif choice == "3":
                self.manage_questions()
            elif choice == "4":
                print("\n👋 Auf Wiedersehen!")
                self.db.close()
                break
            else:
                print("❌ Ungültige Eingabe!")

def main():
    """Programm starten"""
    app = QuizApp()
    app.main_menu()

# ============================================
# Programm starten
# ============================================
if __name__ == "__main__":
    main()