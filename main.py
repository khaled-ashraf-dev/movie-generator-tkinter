import requests
import random
from urllib.request import urlopen
from io import BytesIO
from tinydb import TinyDB, Query
from PIL import ImageTk, Image
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Function to query and display a random movie
def query_movie():
    # Retrieve user-selected filter values
    genre = m_genre_var.get()
    year_min = int(e_year_var.get())
    year_max = int(e_year2_var.get())
    rating_str = m_rating_var.get()
    if rating_str == 'Any':
        rating = 0
    else:
        rating = float(rating_str[:3])
    votes = int(m_votes_var.get()[:-1].replace(',', ''))
    english_str = m_english_var.get()
    if english_str == 'Yes':
        english = True

    # Open and query the database
    db = TinyDB('omdb_clean.json')
    Movie = Query()
    results = db.search(
        (Movie.Genre.search(genre)) &
        (Movie.Year >= year_min) &
        (Movie.Year <= year_max) &
        (Movie.imdbRating >= rating) &
        (Movie.imdbVotes >= votes) &
        (Movie.Language == 'English')
    )
    
    # Randomly choose a movie from the filtered results
    choice = random.choice(results)

    # Prepare movie information to display
    title_info = f"""{choice['Title']} ({choice['Year']})

Number of ratings: {choice['imdbVotes']:,}

IMDb link: www.imdb.com/title/{choice['imdbID']}

Genres: {choice['Genre']}

Language: {choice['Language']}

Plot:

{choice['Plot']}"""
    
    # Set the movie information in the UI
    title_info_var.set(title_info)

    # Load and display the movie poster
    URL = choice['Poster']
    u = urlopen(URL)
    raw_data = u.read()
    u.close()

    image = Image.open(BytesIO(raw_data))
    width, height = image.size
    new_width, new_height = int(width*0.75), int(height*0.75)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)

    l_poster = ttk.Label(frame2, image=image)
    l_poster.image = image
    l_poster.grid(row=0, column=0, padx=30, pady=15)

# List of movie genres
genres = ['Documentary', 'Short', 'Comedy', 'Action', 'Adventure', 'Drama',
          'History', 'War', 'Romance', 'Horror', 'Mystery', 'Thriller',
          'Sci-Fi', 'Fantasy', 'Family', 'Crime', 'Animation', 'Western',
          'Music', 'Musical', 'Biography', 'Film-Noir', 'Sport', 'Fantasy', 'Superhero']

# Create the main window
root = ttk.Window(themename="cyborg", title='Movie Recommendations')
root.geometry('{}x{}'.format(800, 650))

# Define StringVars for storing user selections
m_genre_var = ttk.StringVar()
e_year_var = ttk.StringVar()
e_year2_var = ttk.StringVar()
m_rating_var = ttk.StringVar()
m_votes_var = ttk.StringVar()
m_english_var = ttk.StringVar()
title_info_var = ttk.StringVar()
title_info_var.set('old')

# Create the main frame
frame = ttk.Frame(root, width=800, height=120)
frame.pack(padx=50, pady=20)

# Labels and entry fields for filter options
l_genre = ttk.Label(frame, text='Genre', bootstyle="light")
l_genre.grid(row=0, column=0, padx=30, pady=15)

l_year = ttk.Label(frame, text='Year from', bootstyle="light")
l_year.grid(row=0, column=1, padx=30, pady=15)

l_year2 = ttk.Label(frame, text='Year to', bootstyle="light")
l_year2.grid(row=0, column=2, padx=30, pady=15)

l_rating = ttk.Label(frame, text='Rating', bootstyle="light")
l_rating.grid(row=2, column=0, padx=30, pady=15)

l_votes = ttk.Label(frame, text='Votes', bootstyle="light")
l_votes.grid(row=2, column=1, padx=30, pady=15)

l_english = ttk.Label(frame, text='English only', bootstyle="light")
l_english.grid(row=2, column=2, padx=30, pady=15)

# Comboboxes and entry fields for user input
m_genre = ttk.Combobox(frame, bootstyle="light",
                       width=10, textvariable=m_genre_var)
m_genre.grid(row=1, column=0, padx=30, pady=5, sticky='w')
m_genre['values'] = genres
m_genre.current(5)

e_year = ttk.Entry(frame, bootstyle="light", width=10, textvariable=e_year_var)
e_year.grid(row=1, column=1, padx=30, pady=5)
e_year.insert(END, '1900')

e_year2 = ttk.Entry(frame, bootstyle="light",
                    width=10, textvariable=e_year2_var)
e_year2.grid(row=1, column=2, padx=30, pady=5)
e_year2.insert(END, '2020')

m_rating = ttk.Combobox(frame, bootstyle="light",
                        width=10, textvariable=m_rating_var)
m_rating.grid(row=3, column=0, padx=30, pady=5, sticky='w')
m_rating['values'] = ['Any', '6.0+', '6.5+', '7.0+', '7.5+', '8.0+']
m_rating.current(3)

m_votes = ttk.Combobox(frame, bootstyle="light",
                       width=10, textvariable=m_votes_var)
m_votes.grid(row=3, column=1, padx=30, pady=5, sticky='w')
m_votes['values'] = ['5,000+', '10,000+', '25,000+', '50,000+', '100,000+',
                     '200,000+', '500,000+']
m_votes.current(0)

m_english = ttk.Combobox(frame, bootstyle="light",
                         width=10, textvariable=m_english_var)
m_english.grid(row=3, column=2, padx=30, pady=5, sticky='w')
m_english['values'] = ['Yes', 'No']
m_english.current(0)

# Create a frame for movie information display
frame2 = ttk.Frame(root, width=800)
frame2.pack(padx=50, pady=0)

l_title_info = ttk.Label(frame2, bootstyle="light", wraplength=300, textvariable=title_info_var)
l_title_info.grid(row=0, column=1, padx=30, pady=15)

# Create a frame for buttons
frame3 = ttk.Frame(root, width=800)
frame3.pack(padx=50, pady=10)

# Button to recommend another movie
recommend_another_btn = ttk.Button(frame3, text='Recommend Another Movie',
                                    bootstyle='primary', command=query_movie)
recommend_another_btn.grid(row=4, column=0, padx=30, pady=30)

# Initial recommendation
query_movie()
root.mainloop()