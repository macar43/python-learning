# ============================================
# To-Do Liste - Einfache CLI Anwendung
# ============================================

# Liste speichert alle Aufgaben
todos = []

def display_menu():
    """Zeigt das Hauptmenü an"""
    print("\n" + "="*40)
    print("📝 MEINE TO-DO LISTE")
    print("="*40)
    print("1. ➕ Aufgabe hinzufügen")
    print("2. 📋 Alle Aufgaben anzeigen")
    print("3. ✅ Aufgabe als erledigt markieren")
    print("4. 🗑️  Aufgabe löschen")
    print("5. 🚪 Beenden")
    print("="*40)

def add_todo():
    """Neue Aufgabe zur Liste hinzufügen"""
    task = input("Neue Aufgabe eingeben: ").strip()
    
    if task == "":
        print("❌ Aufgabe darf nicht leer sein!")
        return
    
    # Dictionary für jede Aufgabe: Text + Status
    todo_item = {
        "task": task,
        "done": False
    }
    todos.append(todo_item)
    print(f"✅ Aufgabe '{task}' hinzugefügt!")

def list_todos():
    """Zeigt alle Aufgaben an"""
    if len(todos) == 0:
        print("\n📭 Keine Aufgaben vorhanden!")
        return
    
    print("\n📋 DEINE AUFGABEN:")
    print("-" * 40)
    
    for index, todo in enumerate(todos, 1):
        # Symbole basierend auf Status
        status = "✅" if todo["done"] else "⭕"
        print(f"{index}. {status} {todo['task']}")
    
    print("-" * 40)

def mark_done():
    """Aufgabe als erledigt markieren"""
    list_todos()
    
    if len(todos) == 0:
        return
    
    try:
        num = int(input("\nNummer der Aufgabe eingeben: "))
        
        # Prüfe ob Nummer gültig ist
        if num < 1 or num > len(todos):
            print("❌ Ungültige Nummer!")
            return
        
        # Array startet bei 0, daher num-1
        todos[num - 1]["done"] = True
        print(f"✅ Aufgabe #{num} als erledigt markiert!")
    
    except ValueError:
        print("❌ Bitte eine Zahl eingeben!")

def delete_todo():
    """Aufgabe löschen"""
    list_todos()
    
    if len(todos) == 0:
        return
    
    try:
        num = int(input("\nNummer der Aufgabe zum Löschen: "))
        
        if num < 1 or num > len(todos):
            print("❌ Ungültige Nummer!")
            return
        
        # Gelöschte Aufgabe speichern für die Nachricht
        deleted_task = todos[num - 1]["task"]
        
        # remove() würde erste Übereinstimmung löschen
        # Besser: del mit Index
        del todos[num - 1]
        print(f"🗑️  Aufgabe '{deleted_task}' gelöscht!")
    
    except ValueError:
        print("❌ Bitte eine Zahl eingeben!")

def main():
    """Hauptprogramm - die zentrale Schleife"""
    print("🎉 Willkommen zur To-Do Listen App!")
    
    while True:
        display_menu()
        choice = input("Wähle eine Option (1-5): ").strip()
        
        if choice == "1":
            add_todo()
        
        elif choice == "2":
            list_todos()
        
        elif choice == "3":
            mark_done()
        
        elif choice == "4":
            delete_todo()
        
        elif choice == "5":
            print("\n👋 Auf Wiedersehen!")
            break
        
        else:
            print("❌ Ungültige Eingabe! Bitte 1-5 eingeben.")

# ============================================
# Programm starten
# ============================================
if __name__ == "__main__":
    main()