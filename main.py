import tkinter as tk
from tkinter import messagebox, simpledialog

class Book:
    def __init__(self, id, title, author, price, rating):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.rating = rating

    def __str__(self):
        return f"[{self.id}] {self.title} by {self.author} - ₹{self.price} - Rating: {self.rating}"

books = [
    Book(1, "Python Programming", "John Doe", 500, 4.5),
    Book(2, "Data Structures", "Jane Smith", 400, 4.0),
    Book(3, "Algorithms Unlocked", "Thomas", 600, 4.7),
    Book(4, "Machine Learning", "Andrew Ng", 800, 4.9),
    Book(5, "Database Systems", "Elmasri", 450, 4.3)
]

# Algorithm Functions
def binary_search(books_sorted, target):
    left, right = 0, len(books_sorted) - 1
    while left <= right:
        mid = (left + right) // 2
        if books_sorted[mid].title.lower() == target.lower():
            return books_sorted[mid]
        elif books_sorted[mid].title.lower() < target.lower():
            left = mid + 1
        else:
            right = mid - 1
    return None

def bubble_sort(books, key):
    n = len(books)
    for i in range(n):
        for j in range(0, n - i - 1):
            if getattr(books[j], key) > getattr(books[j + 1], key):
                books[j], books[j + 1] = books[j + 1], books[j]
    return books

def knapsack(books, budget):
    n = len(books)
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for w in range(budget + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif books[i - 1].price <= w:
                dp[i][w] = max(books[i - 1].rating + dp[i - 1][w - books[i - 1].price], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_books = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_books.append(books[i - 1])
            w -= books[i - 1].price
    return selected_books, dp[n][budget]

# GUI Functions
def display_books():
    output.delete('1.0', tk.END)
    for book in books:
        output.insert(tk.END, str(book) + "\n")

def search_book():
    sorted_books = sorted(books, key=lambda x: x.title)
    title = simpledialog.askstring("🔍 Search Book", "Enter Book Title:")
    if title:
        result = binary_search(sorted_books, title)
        output.delete('1.0', tk.END)
        if result:
            output.insert(tk.END, f"✅ Book Found:\n{result}")
        else:
            output.insert(tk.END, "❌ Book Not Found!")

def sort_books_by_price():
    sorted_list = bubble_sort(books.copy(), 'price')
    output.delete('1.0', tk.END)
    output.insert(tk.END, "📘 Books Sorted by Price:\n")
    for book in sorted_list:
        output.insert(tk.END, str(book) + "\n")

def sort_books_by_rating():
    sorted_list = bubble_sort(books.copy(), 'rating')
    output.delete('1.0', tk.END)
    output.insert(tk.END, "📗 Books Sorted by Rating:\n")
    for book in sorted_list:
        output.insert(tk.END, str(book) + "\n")

def suggest_bundle():
    budget = simpledialog.askinteger("💰 Suggest Bundle", "Enter your budget (₹):")
    if budget is not None:
        selected, total_rating = knapsack(books, budget)
        output.delete('1.0', tk.END)
        if selected:
            output.insert(tk.END, f"📦 Recommended Books within ₹{budget}:\n")
            for book in selected:
                output.insert(tk.END, str(book) + "\n")
            output.insert(tk.END, f"\nTotal Rating Value: {total_rating}")
        else:
            output.insert(tk.END, "No books found within this budget!")

# Main GUI
root = tk.Tk()
root.title("📚 Online Bookstore - DAA Mini Project")
root.geometry("750x550")
root.config(bg="#e6f2ff")  # Light blue background

title = tk.Label(root, text="📚 ONLINE BOOKSTORE 📚", font=("Helvetica", 20, "bold"), bg="#e6f2ff", fg="#004080")
title.pack(pady=10)

btn_frame = tk.Frame(root, bg="#e6f2ff")
btn_frame.pack(pady=10)

btn_style = {"width": 20, "padx": 5, "pady": 5, "bg": "#007acc", "fg": "white", "font": ("Helvetica", 10, "bold")}

tk.Button(btn_frame, text="📖 Display All Books", command=display_books, **btn_style).grid(row=0, column=0)
tk.Button(btn_frame, text="🔍 Search Book (Binary)", command=search_book, **btn_style).grid(row=0, column=1)
tk.Button(btn_frame, text="💸 Sort by Price", command=sort_books_by_price, **btn_style).grid(row=1, column=0)
tk.Button(btn_frame, text="⭐ Sort by Rating", command=sort_books_by_rating, **btn_style).grid(row=1, column=1)
tk.Button(btn_frame, text="🎁 Suggest Bundle (Knapsack)", width=43, command=suggest_bundle, bg="#33cc33", fg="white", font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=5)

output = tk.Text(root, width=90, height=18, font=("Courier", 10), bg="#f9f9f9", fg="#333333", relief=tk.SUNKEN, bd=2)
output.pack(pady=10)

tk.Button(root, text="❌ Exit", command=root.destroy, bg="red", fg="white", font=("Helvetica", 10, "bold"), width=15).pack(pady=10)

root.mainloop()
