import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv

# 📌 Load environment variables
load_dotenv()  # .env file se variables load karega

# 📌 API Key ko environment variable se load karein
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("⚠ API Key is missing! Please set it in your .env file or Streamlit secrets.")

# 📌 Load Library from File
def load_library(filename="library.txt"):
    """Library ko file se load karega. Agar file exist nahi karti to empty list return karega."""
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            return json.load(file)
    return []

# 📌 Save Library to File
def save_library(library, filename="library.txt"):
    """Library ko JSON format mein save karega taake wapas load kar sakein."""
    with open(filename, "w") as file:
        json.dump(library, file, indent=4)

# 📌 Fetch Book Summary from Google Books API
def get_book_summary(title):
    """Fetch a book summary using Google Books API."""
    if not API_KEY:
        return "❌ API Key not found! Please set it in your environment variables."

    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["volumeInfo"].get("description", "No summary available.")
        else:
            return "❌ No summary found for this book."
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# ✅ Streamlit UI
st.title("📚 Personal Library Manager")

# 📌 Load Library on App Start
library = load_library()

# 📌 Sidebar Navigation
menu = st.sidebar.selectbox("Select an Option", ["📖 Add Book", "❌ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics", "📜 Get Book Summary"])

# 📌 Add Book
if menu == "📖 Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author Name")
    year = st.number_input("Enter Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Enter Genre")
    read_status = st.radio("Have you read this book?", ["Yes", "No"]) == "Yes"

    if st.button("Add Book"):
        library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
        save_library(library)
        st.success(f"✅ '{title}' added successfully!")

# 📌 Remove Book
elif menu == "❌ Remove Book":
    st.subheader("🗑 Remove a Book")
    if library:
        titles = [book["title"] for book in library]
        book_to_remove = st.selectbox("Select a Book to Remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"✅ '{book_to_remove}' removed successfully!")
    else:
        st.warning("⚠ No books available to remove!")

# 📌 Search Book
elif menu == "🔍 Search Book":
    st.subheader("🔎 Search for a Book")
    search_query = st.text_input("Enter Book Title or Author")
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("⚠ No matching books found!")

# 📌 Display Books
elif menu == "📚 Display Books":
    st.subheader("📂 Your Library Collection")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("⚠ No books in your library!")

# 📌 Display Statistics
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    st.write(f"📚 Total Books: **{total_books}**")
    st.write(f"✅ Books Read: **{read_books}**")
    st.write(f"📈 Percentage Read: **{percentage_read:.2f}%**")

# 📌 Get Book Summary
elif menu == "📜 Get Book Summary":
    st.subheader("📖 Get Book Summary")
    book_title = st.text_input("Enter Book Title")
    if st.button("Get Summary"):
        summary = get_book_summary(book_title)
        st.info(summary)
