
import streamlit as st
import pandas as pd
import json
import datetime
import time
import random
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to load Lottie animations
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Load and save library
def load_library():
    if os.path.exists('library.json'):
        with open('library.json', 'r') as file:
            st.session_state.library = json.load(file)

def save_library():
    with open('library.json', 'w') as file:
        json.dump(st.session_state.library, file)

# Add and remove books
def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
   
    
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.6)
    # st.experimental_rerun()
     st.rerun()
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        st.experimental_rerun()

# Function to search books
def search_books(search_term, search_by):
    st.session_state.search_results = [
        book for book in st.session_state.library if search_term.lower() in book[search_by.lower()].lower()
    ]

# Function to generate stats
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    authors = {}
    
    for book in st.session_state.library:
        authors[book["author"]] = authors.get(book["author"], 0) + 1

    return {
        'total_books': total_books,
        'read_books': read_books,
        'percentage_read': percentage_read,
        'authors': authors
    }

# Function for visualizations (placeholder)
def create_visualizations():
    st.write("Visualizations will be added here.")

# Sidebar navigation
st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
nav_options = st.sidebar.radio("Choose an option:", ["View Library", "Add Book", "Statistics"])
st.session_state.current_view = nav_options.lower().replace(" ", "_")

# Main Title
st.markdown("<h1 style='text-align: center;'>Personal Library Manager</h1>", unsafe_allow_html=True)
# Handle different views
if st.session_state.current_view == "View Library":
    # display_books()
 def display_books():
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books!")
    else:
        for book in st.session_state.library:
            st.write(f"**Title:** {book['title']}, **Author:** {book['author']}, **Year:** {book['publication_year']}")

elif st.session_state.current_view == "Add Book":
    st.header("Add a New Book")
    with st.form(key='add_book_form'):
        title = st.text_input("Book Title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        genre = st.selectbox("Genre", [
            "Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "Poetry", "Self-help", "Art", "Religion", "History", "Other"
        ])
        read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
        read_bool = read_status == "Read"
        submit_button = st.form_submit_button(label="Add Book")
        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)
            st.success("Book added successfully!")
            st.balloons()
            st.rerun()

elif st.session_state.current_view == "Search Books":
    st.header("Search Books")
    search_term = st.text_input("Search for a book")
    search_by = st.radio("Search by", ["Title", "Author", "Genre"], horizontal=True)
    if st.button("Search"):
        search_books(search_term, search_by)
    
    if st.session_state.search_results:
        st.subheader("Search Results")
        for book in st.session_state.search_results:
            st.write(f"📖 {book['title']} by {book['author']} ({book['publication_year']}) - {book['genre']}")

# Add book form
if st.session_state.current_view == "add_book":
    st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
    
    with st.form(key='add_book_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Book Title", max_chars=100)
            author = st.text_input("Author", max_chars=100)
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        
        with col2:
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "History", "Other"])
            read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
       
        submit_button = st.form_submit_button(label="Add Book")
        
        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_status == "Read")
    
    if st.session_state.book_added:
        st.success("Book added successfully!")
        st.balloons()
        st.session_state.book_added = False

# Display library
elif st.session_state.current_view == "view_library":
    st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)

    search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
    search_term = st.text_input("Enter search term:")
    if st.button("Search"):
        search_books(search_term, search_by)

    if st.session_state.search_results:
        st.markdown(f"<h3>Found {len(st.session_state.search_results)} results:</h3>", unsafe_allow_html=True)
        for book in st.session_state.search_results:
            st.markdown(f"**{book['title']}** by {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")

    elif search_term:
        st.markdown("<div class='warning-message'>No books found matching your search.</div>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to get started!")
    else:
        for i, book in enumerate(st.session_state.library):
            st.markdown(f"**{book['title']}** by {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
            if st.button("Remove", key=f"remove_{i}"):
                remove_book(i)

# Statistics view
elif st.session_state.current_view == "statistics":
    st.markdown("<h2 class='sub-header'>Your Library Statistics</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>Your library is empty. Add some books to see stats!</div>", unsafe_allow_html=True)
    else:
        stats = get_library_stats()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Books", stats['total_books'])
        with col2:
            st.metric("Books Read", stats['read_books'])
        with col3:
            st.metric("Percentage Read", f"{stats['percentage_read']:.1f}%")

        create_visualizations()

        if stats['authors']:
            st.markdown("<h3>Top Authors</h3>", unsafe_allow_html=True)
            for author, count in stats['authors'].items():
                st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")

    st.markdown("Copyright © 2025 Sarwat Afreen Personal Library Manager", unsafe_allow_html=True)








# import streamlit as st
# import pandas as pd
# import json
# import datetime
# import time
# import random
# import os
# import plotly.express as px
# import plotly.graph_objects as go
# from streamlit_lottie import st_lottie
# import requests

# # Set page configuration
# st.set_page_config(
#     page_title="Personal Library Management System",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # Function to load Lottie animations
# def load_lottie(url):
#     try:
#         r = requests.get(url)
#         if r.status_code == 200:
#             return r.json()
#     except:
#         return None

# # Initialize session state
# if 'library' not in st.session_state:
#     st.session_state.library = []
# if 'book_added' not in st.session_state:
#     st.session_state.book_added = False
# if 'book_removed' not in st.session_state:
#     st.session_state.book_removed = False
# if 'current_view' not in st.session_state:
#     st.session_state.current_view = "library"
# if 'search_results' not in st.session_state:
#     st.session_state.search_results = []

# # Load and save library
# def load_library():
#     if os.path.exists('library.json'):
#         with open('library.json', 'r') as file:
#             st.session_state.library = json.load(file)

# def save_library():
#     with open('library.json', 'w') as file:
#         json.dump(st.session_state.library, file)

# # Add and remove books
# def add_book(title, author, publication_year, genre, read_status):
#     book = {
#         'title': title,
#         'author': author,
#         'publication_year': publication_year,
#         'genre': genre,
#         'read_status': read_status,
#         'added_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     st.session_state.library.append(book)
#     save_library()
#     st.session_state.book_added = True
#     time.sleep(0.6)
#     st.experimental_rerun()

# def remove_book(index):
#     if 0 <= index < len(st.session_state.library):
#         del st.session_state.library[index]
#         save_library()
#         st.session_state.book_removed = True
#         st.experimental_rerun()

# # Function to search books
# def search_books(search_term, search_by):
#     st.session_state.search_results = [
#         book for book in st.session_state.library if search_term.lower() in book[search_by.lower()].lower()
#     ]

# # Function to generate stats
# def get_library_stats():
#     total_books = len(st.session_state.library)
#     read_books = sum(1 for book in st.session_state.library if book['read_status'])
#     percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
#     authors = {}
    
#     for book in st.session_state.library:
#         authors[book["author"]] = authors.get(book["author"], 0) + 1

#     return {
#         'total_books': total_books,
#         'read_books': read_books,
#         'percentage_read': percentage_read,
#         'authors': authors
#     }

# # Function for visualizations (placeholder)
# def create_visualizations():
#     st.write("Visualizations will be added here.")

# # Sidebar navigation
# st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
# nav_options = st.sidebar.radio("Choose an option:", ["View Library", "Add Book", "Statistics"])
# st.session_state.current_view = nav_options.lower().replace(" ", "_")

# # Main Title
# st.markdown("<h1 style='text-align: center;'>Personal Library Manager</h1>", unsafe_allow_html=True)

# # Add book form
# if st.session_state.current_view == "add_book":
#     st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
    
#     with st.form(key='add_book_form'):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             title = st.text_input("Book Title", max_chars=100)
#             author = st.text_input("Author", max_chars=100)
#             publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        
#         with col2:
#             genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "History", "Other"])
#             read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
        
#         submit_button = st.form_submit_button(label="Add Book")
        
#         if submit_button and title and author:
#             add_book(title, author, publication_year, genre, read_status == "Read")
    
#     if st.session_state.book_added:
#         st.success("Book added successfully!")
#         st.balloons()
#         st.session_state.book_added = False

# # Display library
# elif st.session_state.current_view == "view_library":
#     st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)

#     search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
#     search_term = st.text_input("Enter search term:")
#     if st.button("Search"):
#         search_books(search_term, search_by)

#     if st.session_state.search_results:
#         st.markdown(f"<h3>Found {len(st.session_state.search_results)} results:</h3>", unsafe_allow_html=True)
#         for book in st.session_state.search_results:
#             st.markdown(f"**{book['title']}** by {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")

#     elif search_term:
#         st.markdown("<div class='warning-message'>No books found matching your search.</div>", unsafe_allow_html=True)

#     if not st.session_state.library:
#         st.warning("Your library is empty. Add some books to get started!")
#     else:
#         for i, book in enumerate(st.session_state.library):
#             st.markdown(f"**{book['title']}** by {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
#             if st.button("Remove", key=f"remove_{i}"):
#                 remove_book(i)

# # Statistics view
# elif st.session_state.current_view == "statistics":
#     st.markdown("<h2 class='sub-header'>Your Library Statistics</h2>", unsafe_allow_html=True)

#     if not st.session_state.library:
#         st.markdown("<div class='warning-message'>Your library is empty. Add some books to see stats!</div>", unsafe_allow_html=True)
#     else:
#         stats = get_library_stats()
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric("Total Books", stats['total_books'])
#         with col2:
#             st.metric("Books Read", stats['read_books'])
#         with col3:
#             st.metric("Percentage Read", f"{stats['percentage_read']:.1f}%")

#         create_visualizations()

#         if stats['authors']:
#             st.markdown("<h3>Top Authors</h3>", unsafe_allow_html=True)
#             for author, count in stats['authors'].items():
#                 st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")

#     st.markdown("Copyright © 2025 Sarwat Afreen Personal Library Manager", unsafe_allow_html=True)
