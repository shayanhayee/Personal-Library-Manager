import json
import streamlit as st

# Initialize library
library = []

# Load library from file
def load_library():
    try:
        with open('library.txt', 'r') as file:
            global library
            library = json.load(file)
    except FileNotFoundError:
        library = []

# Save library to file
def save_library():
    with open('library.txt', 'w') as file:
        json.dump(library, file, indent=4)

# Add a book
def add_book(title, author, year, genre, read_status):
    library.append({
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read_status
    })
    save_library()
    st.success(f"✅ '{title}' added to your library!")

# Remove a book
def remove_book(title):
    global library
    original_count = len(library)
    library = [book for book in library if book['title'].lower() != title.lower()]
    save_library()
    if len(library) < original_count:
        st.success(f"🗑️ '{title}' removed from your library!")
    else:
        st.warning(f"❌ Book titled '{title}' not found.")

# Display books
def display_books():
    if library:
        for book in library:
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            st.markdown(f"**{book['title']}** by {book['author']} ({book['year']})\n*Genre:* {book['genre']}\n*Status:* {read_status}")
            st.divider()
    else:
        st.info("📚 Your library is empty. Add some books!")

# Search books
def search_books(query, search_by):
    results = [book for book in library if query.lower() in book[search_by].lower()]
    if results:
        st.success(f"🔍 Found {len(results)} matching book(s):")
        for book in results:
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            st.markdown(f"**{book['title']}** by {book['author']} ({book['year']})\n*Genre:* {book['genre']}\n*Status:* {read_status}")
            st.divider()
    else:
        st.warning("❌ No matching books found.")

# Display statistics
def display_statistics():
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.subheader("📊 Library Statistics")
    st.metric(label="Total Books", value=total_books)
    st.metric(label="Books Read", value=read_books)
    st.metric(label="Books Unread", value=unread_books)
    st.progress(read_percentage / 100)
    st.write(f"**Reading Progress:** {read_percentage:.1f}%")

# Main app
st.title("📚 Personal Library Manager")
st.sidebar.title("Navigation")

load_library()

# Sidebar navigation
page = st.sidebar.radio("Go to", ["Add Book", "Remove Book", "Search Books", "View Library", "Library Statistics"])

if page == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("Add Book", use_container_width=True):
        if title and author and genre:
            add_book(title, author, year, genre, read_status)
        else:
            st.error("Please fill in all the fields.")

elif page == "Remove Book":
    st.header("Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book", use_container_width=True):
        remove_book(title_to_remove)

elif page == "Search Books":
    st.header("Search for a Book")
    search_query = st.text_input("Search for a book")
    search_by = st.selectbox("Search by", ["title", "author"])
    if st.button("Search", use_container_width=True):
        search_books(search_query, search_by)

elif page == "View Library":
    st.header("Your Library")
    display_books()

elif page == "Library Statistics":
    st.header("Library Statistics")
    display_statistics()
