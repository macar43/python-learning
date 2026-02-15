# ============================================
# Guessing Game - Zahlenratespiel
# ============================================

import random

def play_game():
    """Hauptspiel-Funktion"""
    
    # Computer wählt zufällige Zahl zwischen 1 und 100
    secret_number = random.randint(1, 100)
    
    # Zähler für Versuche
    attempts = 0
    guessed = False
    
    print("🎮 Willkommen zum Zahlenratespiel!")
    print("Ich denke mir eine Zahl zwischen 1 und 100.")
    print("Versuche, sie zu erraten!\n")
    
    # Schleife bis zur richtigen Zahl
    while not guessed:
        try:
            # Spieler gibt Zahl ein
            guess = input("Deine Vermutung: ").strip()
            
            # Überprüfe ob Eingabe eine Zahl ist
            if guess == "":
                print("❌ Bitte gib eine Zahl ein!\n")
                continue
            
            guess = int(guess)
            attempts += 1
            
            # Überprüfe Bereich
            if guess < 1 or guess > 100:
                print("❌ Die Zahl muss zwischen 1 und 100 sein!\n")
                continue
            
            # Vergleiche mit geheimer Zahl
            if guess < secret_number:
                difference = secret_number - guess
                print(f"📈 Zu niedrig! Meine Zahl ist höher.")
                print(f"   (Differenz: {difference})\n")
            
            elif guess > secret_number:
                difference = guess - secret_number
                print(f"📉 Zu hoch! Meine Zahl ist niedriger.")
                print(f"   (Differenz: {difference})\n")
            
            else:
                # Richtig geraten!
                guessed = True
                print(f"\n🎉 RICHTIG! Die Zahl war {secret_number}!")
                print(f"✅ Du hast {attempts} Versuche gebraucht!\n")
                
                # Bewertung basierend auf Versuchen
                if attempts <= 5:
                    print("🏆 Mega! Du bist ein Profi!")
                elif attempts <= 10:
                    print("👍 Sehr gut!")
                elif attempts <= 20:
                    print("😊 Gut gemacht!")
                else:
                    print("💪 Nächstes Mal geht's besser!")
        
        except ValueError:
            print("❌ Das ist keine gültige Zahl! Versuche es nochmal.\n")

def main():
    """Hauptprogramm mit Spielwiederholungsoption"""
    
    while True:
        play_game()
        
        # Spieler kann nochmal spielen
        again = input("Möchtest du nochmal spielen? (ja/nein): ").strip().lower()
        
        if again not in ["ja", "j", "yes", "y"]:
            print("\n👋 Danke fürs Spielen! Auf Wiedersehen!")
            break
        
        print("\n" + "="*40 + "\n")

# ============================================
# Programm starten
# ============================================
if __name__ == "__main__":
    main()