import os
from datetime import datetime
import pandas as pd
from tkinter import Toplevel, Label, Scrollbar, Frame, Canvas, Checkbutton, IntVar, Button, StringVar, Entry
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from tkinter import PhotoImage
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

CSV_FILE_PATH = r"C:\Users\polih\OneDrive\Desktop\project\data\goodreads.csv"
current_details_window = None 
image_label = None  

try:
    data = pd.read_csv(
        CSV_FILE_PATH,
        on_bad_lines="skip",  
        sep=",", 
        engine="python"  
    )
    print("File loaded successfully.")
except pd.errors.ParserError as e:
    print(f"Parser error: {e}")


def save_table_data(table, selected_columns):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    save_file_path = os.path.join(current_dir, f"table_data_{timestamp}.csv") 
    try:
        with open(save_file_path, "w", encoding="utf-8") as file:
            file.write(",".join(selected_columns) + "\n")
            for row_id in table.get_children():
                row_values = table.item(row_id)["values"]
                file.write(",".join(map(str, row_values)) + "\n")
        
        print(f"Table data saved to {save_file_path}")
    except Exception as e:
        print(f"Error saving table data: {e}")



def update_selected_info(event, table, canvas, rating_text, author_text, pages_text, image_label, popularity_text):
    selected_item = table.selection()
    if selected_item:
        row_values = table.item(selected_item, "values")
        if row_values:
            book_id = row_values[0]
            print(f"Selected book ID: {book_id}")
            book_id = str(book_id)
            book_data = data[data['isbn'].astype(str) == book_id]
            if not book_data.empty:
                book_data = book_data.iloc[0]
                rating = book_data['rating']
                author_name = book_data['author']
                num_pages = book_data['pages']
                book_image_url = book_data['img']
                
                canvas.itemconfig(rating_text, text=f"{rating}/5")
                canvas.itemconfig(author_text, text=f"{author_name}")
                canvas.itemconfig(pages_text, text=f"{num_pages}")

                display_book_image(book_image_url, canvas)  

                update_popularity_score(book_id, popularity_text, canvas, data)

            else:
                canvas.itemconfig(rating_text, text="Rating: Not Found")
                canvas.itemconfig(author_text, text="Author: Not Found")
                canvas.itemconfig(pages_text, text="Pages: Not Found")
                canvas.itemconfig(popularity_text, text="N/A")

def update_popularity_score(book_id, popularity_text, canvas, data):
    book_data = data.loc[data['isbn'].astype(str) == str(book_id)]
    if not book_data.empty:
        book_data = book_data.iloc[0]  
        score = judge_popularity(book_id, data)  
        canvas.itemconfig(popularity_text, text=f"{score['popularity_score']* 100:.0f}/100")
    else:
        canvas.itemconfig(popularity_text, text="N/A")

def show_popularity(table, data):
    selected_item = table.selection()
    if selected_item:
        row_values = table.item(selected_item, "values")
        if row_values:
            book_id = row_values[0]  
            try:
                popularity_details = judge_popularity(str(book_id), data)
                if "error" in popularity_details:
                    messagebox.showerror("Error", popularity_details["error"])
                else:
                    messagebox.showinfo(
                        "Popularity Details",
                        f"Title: {popularity_details['title']}\n"
                        f"Rating: {popularity_details['rating']}/5\n"
                        f"Reviews: {popularity_details['reviews']}\n"
                        f"Total Ratings: {popularity_details['totalratings']}\n"
                        f"Pages: {popularity_details['pages']}\n"
                        f"Popularity Score: {popularity_details['popularity_score']}"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showinfo("No selection", "Please select a book to check its popularity.")
    else:
        messagebox.showinfo("No selection", "Please select a book to check its popularity.")

def judge_popularity(book_id, data):

    try:
        book_data = data[data['isbn'].astype(str) == book_id].iloc[0]
        
        max_rating = 5  
        max_reviews = data['reviews'].max() if 'reviews' in data else 1
        max_totalratings = data['totalratings'].max() if 'totalratings' in data else 1
        max_pages = data['pages'].max() if 'pages' in data else 1
        
        normalized_rating = book_data['rating'] / max_rating
        normalized_reviews = book_data['reviews'] / max_reviews
        normalized_totalratings = book_data['totalratings'] / max_totalratings
        normalized_pages = 1 - (book_data['pages'] / max_pages)  
        
        weights = {
            'rating': 0.3,
            'reviews': 0.2,
            'totalratings': 0.4,
            'pages': 0.1
        }
        
        popularity_score = (
            (normalized_rating * weights['rating']) +
            (normalized_reviews * weights['reviews']) +
            (normalized_totalratings * weights['totalratings']) +
            (normalized_pages * weights['pages'])
        )
        
        return {
            'title': book_data['title'],
            'rating': book_data['rating'],
            'reviews': book_data['reviews'],
            'totalratings': book_data['totalratings'],
            'pages': book_data['pages'],
            'popularity_score': round(popularity_score, 2)
        }
    
    except IndexError:
        return {"error": "Book not found. Please check the book ID."}

    
def display_book_image(image_url, canvas):
    global image_label  
    if pd.isna(image_url) or image_url.strip() == '':
        print("No image URL found, skipping image display.")
        if image_label:  
            canvas.delete(image_label)
        return  
    try:
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))  
        img = img.resize((200, 240))  
        img_tk = ImageTk.PhotoImage(img) 
        if image_label:  
            canvas.delete(image_label)
        image_label = canvas.create_image(826, 370, image=img_tk)  
        canvas.image = img_tk  
    except Exception as e:
        print(f"Error loading image: {e}")
        if image_label:  
            canvas.delete(image_label)
        placeholder_image = PhotoImage(file="path_to_placeholder_image.png")
        image_label = canvas.create_image(826, 370, image=placeholder_image)

def sort_table(column, reverse, table, selected_columns):
    data_list = [(table.item(row)["values"], row) for row in table.get_children()]
    data_list.sort(key=lambda x: x[0][selected_columns.index(column)], reverse=reverse)
    for index, (values, row) in enumerate(data_list):
        table.move(row, "", index)
    table.heading(column, command=lambda: sort_table(column, not reverse, table, selected_columns))

def filter_table(query, table, data, selected_columns):
    for row in table.get_children():
        table.delete(row)
    filtered_data = data[selected_columns][
        data[selected_columns].apply(lambda row: query.lower() in " ".join(row.astype(str)).lower(), axis=1)
    ]
    for _, row in filtered_data.iterrows():
        table.insert("", "end", values=tuple(row))    


def on_item_double_click(event, table, data, window):
    global current_details_window  
    selected_item = table.selection()
    if selected_item:
        row_values = table.item(selected_item, "values")
        if row_values:
            book_id = row_values[0]  
            book_id = str(book_id)  
            data['isbn'] = data['isbn'].astype(str)
            book_data = data[data['isbn'] == book_id]
            if not book_data.empty:
                book_data = book_data.iloc[0]  
                if current_details_window:
                    current_details_window.destroy()  
                current_details_window = show_book_details_window(book_data, window)  
            else:
                print(f"Book with bookID {book_id} not found in the data.")
                messagebox.showerror("Error", f"Book with bookID {book_id} not found in the dataset.")
                return

def show_book_details_window(book_data, window):
    details_window = Toplevel(window)
    details_window.title(f"Details of Book {book_data['isbn']}")

    details_window.configure(bg="black")

    category_colors = {
        "Title": "#FF7F50",  
        "Bookformat": "#6495ED", 
        "Description": "#98FB98", 
        "Genre": "#BA55D3", 
        "ISBN": "#FF8C00",  
        "ISBN13": "#FFA07A", 
        "Pages": "#66CDAA",  
        "Rating": "#FFD700",  
        "Text Reviews Count": "#F08080", 
        "Reviews": "#EE82EE",  
        "Total Ratings": "#98FB98",  
        "Image": "#FFA07A", 
        "Author": "#BA55D3",  
        "Link": "#20B2AA"  
    }

    book_details = [
        ("Title", book_data['title']),
        ("Author", book_data['author']),
        ("Rating", book_data['rating']),
        ("ISBN", book_data['isbn']),
        ("ISBN13", book_data['isbn13']),
        ("Total Ratings", book_data['totalratings']),
        ("Pages", book_data['pages']),
        ("Genre", book_data['genre']),
        ("Description", book_data['desc']),
        ("Bookformat", book_data['bookformat']),
        ("Reviews", book_data['reviews']),
        ("Link", book_data['link']),
        ("Image", book_data['img'])
    ]

    canvas = Canvas(details_window, bg="black")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = Scrollbar(details_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    details_frame = Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=details_frame, anchor="nw")

    for index, (label, value) in enumerate(book_details):
        label_color = category_colors.get(label, "#000000")
        label_widget = Label(details_frame, text=f"{label}: {value}", font=("Arial", 12), fg=label_color, bg="black", wraplength=700)
        label_widget.grid(row=index, column=0, sticky="w", padx=10, pady=5)

    details_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    details_window.geometry("730x400")
    details_window.resizable(True, True)

    return details_window


def open_genre_selection_window(table, data, selected_columns):
    genre_window = Toplevel()
    genre_window.title("Select Genres")
    genre_window.geometry("700x500")
    genre_window.configure(bg="white")

    search_var = StringVar()

    def update_genre_display():
        """Update the displayed checkboxes based on the search query."""
        query = search_var.get().lower().strip()
        for widget in checkbox_frame.winfo_children():
            widget.destroy()  

        row, col = 0, 0
        for genre in sorted(unique_genres):
            if query in genre.lower():
                Checkbutton(
                    checkbox_frame,
                    text=genre,
                    variable=genre_vars[genre],
                    bg="white",
                    anchor="w"
                ).grid(row=row, column=col, sticky="w", padx=10, pady=5)
                col += 1
                if col >= max_columns:  
                    col = 0
                    row += 1

        checkbox_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    search_entry = Entry(genre_window, textvariable=search_var, bg="lightgray", fg="black")
    search_entry.pack(fill="x", padx=10, pady=5)
    search_var.trace("w", lambda *args: update_genre_display()) 

    canvas = Canvas(genre_window, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(genre_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    checkbox_frame = Frame(canvas, bg="white")

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

    unique_genres = set(
        genre.strip()
        for genres in data["genre"].dropna()
        for genre in genres.split(",")
    )

    genre_vars = {genre: IntVar() for genre in unique_genres}

    max_columns = 3

    update_genre_display()

    def apply_genre_filter():
        selected_genres = [genre for genre, var in genre_vars.items() if var.get()]
        if not selected_genres:
            messagebox.showinfo("No Selection", "Please select at least one genre.")
            return

        filtered_data = data[
            data["genre"]
            .fillna("")  
            .apply(
                lambda genres: all(genre.strip() in str(genres).split(",") for genre in selected_genres)
            )
        ]

        for row in table.get_children():
            table.delete(row)
        for _, row in filtered_data[selected_columns].iterrows():
            table.insert("", "end", values=tuple(row))

        genre_window.destroy()

    Button(
        genre_window,
        text="Apply Filter",
        command=apply_genre_filter,
        bg="#6239DB",
        fg="white",
        relief="flat"
    ).pack(side="left", padx=10, pady=10)

    Button(
        genre_window,
        text="Close",
        command=genre_window.destroy,
        bg="gray",
        fg="white",
        relief="flat"
    ).pack(side="right", padx=10, pady=10)

    checkbox_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))







