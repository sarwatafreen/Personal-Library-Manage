
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

# Custom CSS for styling
st.markdown("""
   <style>
        .main-header {
            font-size: 4rem !important;
            color: #ff6347;
            font-weight: 800;
            margin-bottom: 2rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .sub-header {
            font-size: 2.8rem !important;
            color: #3b82f6;
            font-weight: 600;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

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

# Load library from file
def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
                return True
    except Exception as e:
        st.error(f"Error loading library: {e}")
    return False

# Save library to file
def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
            return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
    return False

# Add a book to library
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
    time.sleep(0.6)  # Animation delay

# Remove a book
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# Sidebar navigation
st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
lottie_book = load_lottie("https://assets9.lottiefiles.com/temp/1f20_aKAfIn.json")
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, height=200, key='book_animation')

nav_options = st.sidebar.radio(
    "Choose an option:",
    ["View Library", "Add Book"]
)

if nav_options == "View Library":
    st.session_state.current_view = "library"
elif nav_options == "Add Book":
    st.session_state.current_view = "add"

st.markdown("<h1 class='main-header'>Personal Library Manager</h1>", unsafe_allow_html=True)

# Add book form
if st.session_state.current_view == "add":
    st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
    
    with st.form(key='add_book_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Book Title", max_chars=100)
            author = st.text_input("Author", max_chars=100)
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        
        with col2:
            genre = st.selectbox("Genre", [
                "Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "Poetry", "Self-Help", "Art", "Religion", "History", "Other"
            ])
            read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
            read_bool = read_status == "Read"
        
        submit_button = st.form_submit_button(label="Add Book")
        
        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)
            
    if st.session_state.book_added:
        st.success("Book added successfully!")
        st.balloons()
        st.session_state.book_added = False

# Display library
elif st.session_state.current_view == "library":
    st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to get started!")
    else:
        cols = st.columns(2)
        for i, book in enumerate(st.session_state.library):
            with cols[i % 2]:
                st.markdown(f"""
                <div style='border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; border-radius: 0.5rem;'>
                    <h3>{book['title']}</h3>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><span style='color: {'green' if book['read_status'] else 'red'};'>
                        {"Read" if book['read_status'] else "Unread"}
                    </span></p>
                </div>
                """, unsafe_allow_html=True)
                search_by = st.selectbox("Srarch by:",["Title","Author","Genre"])
                search_term =st.text_input("Enter search term:")
                if st.button("Search",use_container_width=False):
                    if search_term:
                        with st.spinner("Searching ..."):
                            time.sleep(0.5)
                            search_books(search_term, search_by)
        if hasattr(st.session_state, 'search_results') :    
                if st.session_state.search_reasults:
                    st.markdown(f"<h3> Found{len(st.session_state.search_results)} results:</h3>", unsafe_allow_html=True)      
                    for i, book in enumerate(st.session_state.search_results):
                      st.markdown(f"""
                            <div class = 'book-card'>
                            <h3>{book['title']}</h3>
                            <p><strong>Author:</strong> {book['author' ]}</p>
                                <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                                 <p><strong>Genr:</strong> {book['genre']}</p>
                                 <p><span class='{"read-badge" if book ["read_status"] else "unread-badge"}'>{
                                         "Read" if book["read_staus"] else "Unread"
                                 }</span></p>
                                 </div>>
      """, unsafe_allow_html=True)
                elif search_term:
                 st.markdown("<div class='warning-message'>No books found matching your search.</div>", unsafe_allow_html=True)

elif st.session_state.Current_view == "stats":
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

        create_visulations()

        if stats['authors']:
            st.markdown("<h3>Top Authors</h3>", unsafe_allow_html=True)
            top_authors = dict(list(stats['authors'].items())[:5])
            for author, count in top_authors.items():
                st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")

        st.markdown("---")
        st.markdown("Copyright © 2025 Sarwat Afreen Personal Library Manager", unsafe_allow_html=True)

    if st.button("Remove", key=f"remove_{i}"):
                    if remove_book(i):
                        st.experimental_rerun()
