import streamlit as st
import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Load Library from File
def load_library(filename="library.json"):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            return json.load(file)
    return []

# Save Library to File
def save_library(library, filename="library.json"):
    with open(filename, "w") as file:
        json.dump(library, file, indent=4)

# Fetch Book Summary from API
def get_book_summary(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["volumeInfo"].get("description", "No summary available.")
    return "No summary found."

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Streamlit UI
st.title("📚 Personal Library Manager")
st.sidebar.header("📖 Menu")
choice = st.sidebar.radio("Choose an option:", ["Add Book", "Remove Book", "Search Book", "View Library", "Statistics", "Book Summary"])

# Add a Book
if choice == "Add Book":
    st.header("📌 Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark as Read")
        submit = st.form_submit_button("Add Book")
        
        if submit and title:
            st.session_state.library.append({
                "title": title, "author": author, "year": year, "genre": genre, "read": read_status
            })
            save_library(st.session_state.library)
            st.success(f"📖 '{title}' added to your library!")

# Remove a Book
elif choice == "Remove Book":
    st.header("🗑️ Remove a Book")
    book_titles = [book["title"] for book in st.session_state.library]
    book_to_remove = st.selectbox("Select a book to remove", book_titles) if book_titles else None
    if st.button("Remove Book") and book_to_remove:
        st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
        save_library(st.session_state.library)
        st.success(f"'{book_to_remove}' has been removed.")

# Search a Book
elif choice == "Search Book":
    st.header("🔎 Search for a Book")
    search_query = st.text_input("Enter book title or author")
    if st.button("Search") and search_query:
        results = [book for book in st.session_state.library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            st.write(pd.DataFrame(results))
        else:
            st.warning("No matching books found.")

# View Library
elif choice == "View Library":
    st.header("📚 Your Library")
    if st.session_state.library:
        st.write(pd.DataFrame(st.session_state.library))
    else:
        st.warning("Your library is empty!")

# View Statistics
elif choice == "Statistics":
    st.header("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books
    
    if total_books > 0:
        fig, ax = plt.subplots()
        ax.pie([read_books, unread_books], labels=["Read", "Unread"], autopct='%1.1f%%', colors=["green", "red"])
        st.pyplot(fig)
    else:
        st.warning("No books available to display statistics.")

# Get Book Summary
elif choice == "Book Summary":
    st.header("📖 Get Book Summary")
    book_title = st.text_input("Enter Book Title")
    if st.button("Fetch Summary") and book_title:
        summary = get_book_summary(book_title)
        st.write(summary)
