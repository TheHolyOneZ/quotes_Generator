import customtkinter as ctk
import json
import random
from typing import List, Dict
import tkinter as tk

# Colors for the UI
BG_COLOR = "#000000"    # Black
BUTTON_COLOR = "#6b6b6b" # Gray
TEXT_COLOR = "#ffffff"   # White text
ACCENT_COLOR = "#8a2be2" # Purple

class QuoteGenerator:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.quotes = self._load_quotes()
        self.authors = sorted({quote['author'] for quote in self.quotes})
        self.categories = sorted({quote['category'] for quote in self.quotes})

    def _load_quotes(self) -> List[Dict[str, str]]:
        with open(self.filepath, 'r') as file:
            return json.load(file)

    def filter_by_author(self, author: str) -> List[Dict[str, str]]:
        return [quote for quote in self.quotes if author.lower() in quote['author'].lower()]

    def filter_by_keyword(self, keyword: str) -> List[Dict[str, str]]:
        return [quote for quote in self.quotes if keyword.lower() in quote['text'].lower()]

    def filter_by_category(self, category: str) -> List[Dict[str, str]]:
        return [quote for quote in self.quotes if category.lower() in quote['category'].lower()]

    def random_quote(self) -> Dict[str, str]:
        return random.choice(self.quotes)

    def add_favorite(self, quote: Dict[str, str]):
        self.favorites.append(quote)

    def list_favorites(self) -> List[Dict[str, str]]:
        return self.favorites

class QuoteGeneratorUI:
    def __init__(self, generator: QuoteGenerator):
        self.generator = generator
        self.root = ctk.CTk()
        self.root.geometry("600x500")
        self.root.title("Quote Generator By TheZ")
        self.root.configure(bg=BG_COLOR)

        # Set the window icon
        self.root.iconbitmap("icon.ico")    
        self.root.resizable(False, False)

        # Display area for quotes
        self.quote_display = ctk.CTkLabel(self.root, text="", wraplength=500, bg_color=BG_COLOR, fg_color=BUTTON_COLOR, text_color=TEXT_COLOR)
        self.quote_display.pack(pady=20, padx=20)

        # Dropdown filters
        self.author_var = ctk.StringVar(value="Select Author")
        self.author_dropdown = ctk.CTkOptionMenu(self.root, variable=self.author_var, values=self.generator.authors, fg_color=BUTTON_COLOR, text_color=TEXT_COLOR)
        self.author_dropdown.pack(pady=5)

        self.category_var = ctk.StringVar(value="Select Category")
        self.category_dropdown = ctk.CTkOptionMenu(self.root, variable=self.category_var, values=self.generator.categories, fg_color=BUTTON_COLOR, text_color=TEXT_COLOR)
        self.category_dropdown.pack(pady=5)
        
        # Keyword Entry
        self.keyword_entry = ctk.CTkEntry(self.root, placeholder_text="Filter by Keyword", fg_color=BUTTON_COLOR, text_color=TEXT_COLOR)
        self.keyword_entry.pack(pady=5)

        # Buttons
        self.random_button = ctk.CTkButton(self.root, text="Random Quote", command=self.show_random_quote, fg_color=ACCENT_COLOR)
        self.random_button.pack(pady=5)

        self.filter_button = ctk.CTkButton(self.root, text="Filter Quote", command=self.filter_quote, fg_color=ACCENT_COLOR)
        self.filter_button.pack(pady=5)

        self.favorite_button = ctk.CTkButton(self.root, text="Add to Favorites", command=self.add_to_favorites, fg_color=ACCENT_COLOR)
        self.favorite_button.pack(pady=5)

        self.show_favorites_button = ctk.CTkButton(self.root, text="Show Favorites", command=self.show_favorites, fg_color=ACCENT_COLOR)
        self.show_favorites_button.pack(pady=5)

        self.root.mainloop()

    def show_random_quote(self):
        quote = self.generator.random_quote()
        self.quote_display.configure(text=f'"{quote["text"]}"\n\n- {quote["author"]}')

    def filter_quote(self):
        author = self.author_var.get()
        category = self.category_var.get()
        keyword = self.keyword_entry.get()
        
        filtered_quotes = self.generator.quotes
        if author and author != "Select Author":
            filtered_quotes = self.generator.filter_by_author(author)
        if category and category != "Select Category":
            filtered_quotes = self.generator.filter_by_category(category)
        if keyword:
            filtered_quotes = self.generator.filter_by_keyword(keyword)
        
        if filtered_quotes:
            quote = random.choice(filtered_quotes)
            self.quote_display.configure(text=f'"{quote["text"]}"\n\n- {quote["author"]}')
        else:
            self.quote_display.configure(text="No quotes found.")

    def add_to_favorites(self):
        current_text = self.quote_display.cget("text")
        if current_text:
            for quote in self.generator.quotes:
                if quote["text"] in current_text:
                    self.generator.add_favorite(quote)
                    self.quote_display.configure(text="Added to favorites!")
                    return

    def show_favorites(self):
        favorites = self.generator.list_favorites()
        if favorites:
            favorite_quotes = "\n\n".join([f'"{quote["text"]}"\n- {quote["author"]}' for quote in favorites])
            self.quote_display.configure(text=favorite_quotes)
        else:
            self.quote_display.configure(text="No favorites yet.")

if __name__ == "__main__":
    quote_generator = QuoteGenerator("quotes_1000.json")
    app = QuoteGeneratorUI(quote_generator)
