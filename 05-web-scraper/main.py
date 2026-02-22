# ============================================
# Web-Scraper - Daten von Websites extrahieren
# ============================================

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class WebScraper:
    """Web-Scraper für verschiedene Websites"""
    
    def __init__(self):
        """Initialisiert den Scraper"""
        # User-Agent (sonst blocken manche Websites)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def scrape_quotes(self):
        """Scraped Zitate von quotes.toscrape.com"""
        
        print("\n📖 Scrape Quotes from quotes.toscrape.com...")
        
        try:
            url = "http://quotes.toscrape.com/"
            response = requests.get(url, headers=self.headers,timeout=5)  # 5 Sekunden
            response.raise_for_status()  # Fehler bei schlechtem Status
            if not response.ok:
             print(f"Fehler: HTTP {response.status_code}")
            # HTML parsen mit BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Finde alle Zitat-Container
            quotes = soup.find_all("div", class_="quote")
            
            print(f"✅ {len(quotes)} Zitate gefunden!\n")
            
            # Extrahiere die ersten 5 Zitate
            for i, quote in enumerate(quotes[:5], 1):
                # Zitat-Text
                text = quote.find("span", class_="text").get_text()
                
                # Autor
                author = quote.find("small", class_="author").get_text()
                
                # Tags
                tags = quote.find_all("a", class_="tag")
                tag_list = [tag.get_text() for tag in tags]
                
                print(f"{i}. {text}")
                print(f"   - {author}")
                print(f"   Tags: {', '.join(tag_list)}\n")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Fehler beim Abrufen: {e}")
    
    def scrape_books(self):
        """Scraped Bücher von books.toscrape.com"""
        
        print("\n📚 Scrape Books from books.toscrape.com...")
        
        try:
            url = "http://books.toscrape.com/"
            response = requests.get(url, headers=self.headers, timeout=5)  # 5 Sekunden
            response.raise_for_status()
            if not response.ok:
                print(f"Fehler: HTTP {response.status_code}")
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Finde alle Buch-Container
            books = soup.find_all("article", class_="product_pod")
            
            print(f"✅ {len(books)} Bücher gefunden!\n")
            
            # Extrahiere die ersten 5 Bücher
            for i, book in enumerate(books[:5], 1):
                # Titel
                title = book.find("h3").find("a")["title"]
                
                # Preis
                price = book.find("p", class_="price_color").get_text()
                
                # Verfügbarkeit
                availability = book.find("p", class_="instock availability").get_text(strip=True)
                
                # Rating (als Text)
                rating_class = book.find("p", class_="star-rating")["class"]
                rating = rating_class[1]  # z.B. "Three" aus ["star-rating", "Three"]
                
                print(f"{i}. {title}")
                print(f"   💷 Preis: {price}")
                print(f"   ⭐ Rating: {rating}")
                print(f"   📦 {availability}\n")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Fehler beim Abrufen: {e}")
    
    def scrape_github_trending(self):
        """Scraped GitHub Trending Repositories"""
        
        print("\n⭐ Scrape GitHub Trending Repositories...")
        
        try:
            url = "https://github.com/trending"
            response = requests.get(url, headers=self.headers,timeout=5)  # 5 Sekunden
            response.raise_for_status()
            if not response.ok:
                print(f"Fehler: HTTP {response.status_code}")
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Finde alle Repository-Elemente
            repos = soup.find_all("article", class_="Box-row")
            
            print(f"✅ {len(repos)} Trending Repos gefunden!\n")
            
            # Extrahiere die ersten 5 Repos
            for i, repo in enumerate(repos[:5], 1):
                # Repo-Name und Link
                repo_link = repo.find("h2", class_="h3").find("a")
                repo_name = repo_link.get_text(strip=True)
                repo_url = "https://github.com" + repo_link["href"]
                
                # Beschreibung
                description_elem = repo.find("p", class_="col-9")
                description = description_elem.get_text(strip=True) if description_elem else "Keine Beschreibung"
                
                # Language
                lang_elem = repo.find("span", itemprop="programmingLanguage")
                language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
                
                # Stars heute
                stars_elem = repo.find("span", class_="d-inline-block float-sm-right")
                stars_today = stars_elem.get_text(strip=True) if stars_elem else "0"
                
                print(f"{i}. {repo_name}")
                print(f"   🔗 {repo_url}")
                print(f"   💬 {description[:80]}..." if len(description) > 80 else f"   💬 {description}")
                print(f"   🔤 Language: {language}")
                print(f"   ⭐ Stars heute: {stars_today}\n")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Fehler beim Abrufen: {e}")
    
    def scrape_and_save_quotes(self, filename="quotes.json"):
        """Scraped Zitate und speichert sie als JSON"""
        
        print(f"\n💾 Speichere Zitate in {filename}...")
        
        try:
           # url = "http://quotes.toscrape.com/"
            for page in range(1, 4):
              url = f"http://quotes.toscrape.com/page/{page}/"
            response = requests.get(url, timeout=5,headers=self.headers) # 5 Sekunden
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            quotes = soup.find_all("div", class_="quote")
            if not response.ok:
                print(f"Fehler: HTTP {response.status_code}")
            # Extrahiere alle Zitate
            quotes_list = []
            for quote in quotes:
                text = quote.find("span", class_="text").get_text()
                author = quote.find("small", class_="author").get_text()
                
                quotes_list.append({
                    "text": text,
                    "author": author,
                    "scraped_at": datetime.now().isoformat()
                })
            
            # Speichere als JSON
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(quotes_list, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {len(quotes_list)} Zitate gespeichert in '{filename}'!")
        
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")

def main():
    """Hauptprogramm"""
    
    scraper = WebScraper()
    
    print("="*60)
    print("🕷️  WEB-SCRAPER - Extrahiere Daten von Websites")
    print("="*60)
    
    while True:
        print("\n📋 Wähle eine Option:")
        print("1. 📖 Quotes scrapen")
        print("2. 📚 Bücher scrapen")
        print("3. ⭐ GitHub Trending scrapen")
        print("4. 💾 Quotes scrapen und speichern (JSON)")
        print("5. 🚪 Beenden")
        
        choice = input("\nDeine Wahl (1-5): ").strip()
        
        if choice == "1":
            scraper.scrape_quotes()
        
        elif choice == "2":
            scraper.scrape_books()
        
        elif choice == "3":
            scraper.scrape_github_trending()
        
        elif choice == "4":
            scraper.scrape_and_save_quotes()
        
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