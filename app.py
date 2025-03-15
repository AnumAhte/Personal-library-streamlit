import streamlit as st
import json
import os
import requests

# File for storing books
LIBRARY_FILE = "library.json"

# Function to fetch book summary
@st.cache_data
def get_book_summary(title):
    """Fetch a book summary from Google Books API."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and "items" in data:
            return data["items"][0]["volumeInfo"].get("description", "No summary available.")
        else:
            return "❌ No summary found for this book."
    
    except Exception as e:
        return f"⚠️ Error fetching summary: {str(e)}"

# Function to load library from file
def load_library():
    """Load the library from a file."""
    if os.path.exists(LIBRARY_FILE) and os.path.getsize(LIBRARY_FILE) > 0:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save library to file
def save_library(library):
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# Streamlit UI
st.title("📚 Personal Library Manager")
st.sidebar.header("📖 Menu")

menu_option = st.sidebar.radio("Select an option:", ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics", "Book Summary"])

# Add Book
if menu_option == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Enter Book Title:")
    author = st.text_input("Enter Author:")
    year = st.number_input("Enter Publication Year:", min_value=0, step=1)
    genre = st.text_input("Enter Genre:")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
        save_library(library)
        st.success("✅ Book added successfully!")

# Remove Book
elif menu_option == "Remove Book":
    st.header("🗑 Remove a Book")
    book_titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove:", book_titles)
    
    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success("✅ Book removed successfully!")

# Search Book
elif menu_option == "Search Book":
    st.header("🔍 Search for a Book")
    search_query = st.text_input("Enter book title or author:")
    
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("⚠️ No matching books found.")

# Display Books
elif menu_option == "Display Books":
    st.header("📚 Your Library")
    
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("⚠️ No books in the library.")

# Statistics
elif menu_option == "Statistics":
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    
    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"📖 **Books Read:** {read_books} ({(read_books / total_books * 100) if total_books > 0 else 0:.2f}%)")

# Book Summary
elif menu_option == "Book Summary":
    st.header("📖 Get Book Summary")
    book_title = st.text_input("Enter Book Title for Summary:")
    
    if st.button("Get Summary"):
        summary = get_book_summary(book_title)
        st.write(f"📖 **Summary:** {summary}")

