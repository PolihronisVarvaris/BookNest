from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,ttk,messagebox, Toplevel
from matplotlib.figure import Figure
import pandas as pd 
from data import *
from functions import save_table_data, update_selected_info, sort_table, filter_table, on_item_double_click,open_genre_selection_window, show_popularity
from search_engine import SearchEngine
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize

def preprocess_text(self, text):
    from nltk.tokenize.punkt import PunktSentenceTokenizer
    punkt_tokenizer = PunktSentenceTokenizer()
    
    sentences = punkt_tokenizer.tokenize(text)
    tokens = [word_tokenize(sentence.lower()) for sentence in sentences]


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\polih\OneDrive\Desktop\project\assets\frame0")
CSV_FILE_PATH = r"C:\Users\polih\OneDrive\Desktop\project\data\goodreads.csv"

try:
    data = pd.read_csv(
        CSV_FILE_PATH,
        on_bad_lines="skip",  
        sep=",",  
        engine="python"  
    )
    print("File loaded successfully.")

    data = data[(data['isbn'].notnull() & (data['isbn'] != ''))]

except pd.errors.ParserError as e:
    print(f"Parser error: {e}")



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



window = Tk()

window.geometry("1000x550")
window.configure(bg = "#FFFFFF")

window_width = 1000
window_height = 550
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = int((screen_width - window_width) / 2.0)
y_position = int((screen_height - window_height) / 2.5)
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

search_engine = SearchEngine(data, ["desc", "title", "author"])
print("Building index...")
search_engine.build_index()
print("Index built successfully.")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 550,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    550.0,
    fill="#6239DB",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    500.0,
    275.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    563.0,
    56.0,
    image=entry_image_1
)

def on_entry_click(event):
    if entry_1.get() == "Search":
        entry_1.delete(0, "end")  
        entry_1.config(fg="#FFFFFF")  
def on_focus_out(event):
    if entry_1.get() == "":
        entry_1.insert(0, "Search")  
        entry_1.config(fg="#AAAAAA") 

entry_1 = Entry(
    bd=0,
    bg="#062E44", 
    fg="#FFFFFF",
    highlightthickness=0,
    font=("Inter Italic", 16 * -1),
    insertbackground="#FFFFFF"
)
entry_1.place(
    x=337.0,
    y=45.0,
    width=452.0,
    height=20.0
)

entry_1.insert(0, "Search")

entry_1.bind("<FocusIn>", on_entry_click)
entry_1.bind("<FocusOut>", on_focus_out)

entry_2 = Entry(
    canvas,
    font=("Inter Italic", 16),
    fg="#FFFFFF",
    bg="#062E44",
    bd=0,
    highlightthickness=0
)
entry_2.place(
    x=359.0,
    y=175.0,
    width=200.0,  
    height=25.0  
)

rating_text = canvas.create_text(
    132.0,
    188.0,
    anchor="ne",
    text="/5",
    fill="#062E44",
    font=("Inter Italic", 20 * -1)
)

popularity_text = canvas.create_text(
    262.0,  
    188.0,  
    anchor="ne",
    text="/100",
    fill="#062E44",
    font=("Inter Italic", 20 * -1)
)

canvas.create_text(
    168.0,
    182.0,
    anchor="nw",
    text="",
    fill="#062E44",
    font=("Inter Italic", 16 * -1)
)

author_text = canvas.create_text(
    713.0,
    186.0,
    anchor="nw",
    text="",
    fill="#062E44",
    font=("Inter Italic", 17 * -1),
    width=130,

)

pages_text = canvas.create_text(
    878.0,
    192.0,
    anchor="nw",
    text="",
    fill="#062E44",
    font=("Inter Italic", 20 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    174.0,
    368.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    499.0,
    367.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    826.0,
    369.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    bg="#FFFFFF",  
    activebackground="#FFFFFF",  
    command=lambda: save_table_data(table, selected_columns),
    relief="flat"
)
button_1.place(
    x=915.0,
    y=67.0,
    width=30.0,
    height=30.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    bg="#FFFFFF",  
    activebackground="#FFFFFF",  
    command=lambda: on_show_plot_button_click(),
    relief="flat"
)
button_5.place(
    x=950.0,
    y=67.0,
    width=30.0,
    height=30.0
)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))  
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    bg="#FFFFFF",
    activebackground="#FFFFFF",
    command=lambda: print("button_6 clicked"),  
    relief="flat"
)
button_6.place(x=843.0, y=33.0, width=30.0, height=30.0)  


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    bg="#FFFFFF",  
    activebackground="#FFFFFF",
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=843.0,
    y=67.0,
    width=30.0,
    height=30.0
)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    bg="#FFFFFF",  
    activebackground="#FFFFFF",  
    command=lambda: open_genre_selection_window(table, data, selected_columns),
    relief="flat"
)
button_3.place(
    x=881.0,
    y=67.0,
    width=30.0,
    height=30.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    bg="#062E44",  
    activebackground="#062E44",  
    command=lambda: filter_table(entry_1.get(), table, data, selected_columns),
    relief="flat"
)
button_4.place(
    x=782.0,
    y=40.0,
    width=30.0,
    height=30.0
)


selected_columns = ["isbn", "title", "genre"]

table = ttk.Treeview(window, columns=selected_columns, show="headings")




def search_and_update_with_relevance():
    search_term = entry_2.get().strip()
    if not search_term:
        messagebox.showinfo("Input Error", "Please enter a search term.")
        return

    try:
        search_results = search_engine.search(search_term, top_n=30)

        for item in table.get_children():
            table.delete(item)

        if not search_results:
            messagebox.showinfo("No Results", "No matching documents found.")
            return

        for result in search_results:
            table.insert("", "end", values=(result["isbn"], result["title"], result["genre"], f"{result['relevance']}%"))

        print("Top Relevant Books:")
        for result in search_results:
            print(f"Title: {result['title']}, Relevance: {result['relevance']}%")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

from tkinter import Toplevel

def search_and_display_all():
    search_term = entry_2.get().strip()
    if not search_term:
        messagebox.showinfo("Input Error", "Please enter a search term.")
        return

    try:
        search_results = search_engine.search(search_term, top_n=None)  # Set top_n to None to get all results

        if not search_results:
            messagebox.showinfo("No Results", "No matching documents found.")
            return

        results_window = Toplevel(window)
        results_window.title(f"Search Results for '{search_term}'")
        results_window.geometry("800x600")

        results_table = ttk.Treeview(results_window, columns=["isbn", "title", "genre", "relevance"], show="headings")
        results_table.heading("isbn", text="ISBN")
        results_table.heading("title", text="Title")
        results_table.heading("genre", text="Genre")
        results_table.heading("relevance", text="Relevance")

        results_table.column("isbn", width=100, anchor="center")
        results_table.column("title", width=300, anchor="w")
        results_table.column("genre", width=100, anchor="center")
        results_table.column("relevance", width=100, anchor="center")

        for result in search_results:
            results_table.insert("", "end", values=(result["isbn"], result["title"], result["genre"], f"{result['relevance']}%"))

        scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=results_table.yview)
        results_table.configure(yscrollcommand=scrollbar.set)

        results_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        print(f"Found {len(search_results)} relevant books.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


button_6.config(command=search_and_display_all)



# def update_table_with_results(search_results):
#     start_index = (current_page - 1) * results_per_page
#     end_index = min(current_page * results_per_page, total_results)

#     for item in table.get_children():
#         table.delete(item)

#     for result, relevance in search_results[start_index:end_index]:
#         table.insert("", "end", values=(result['isbn'], result['title'], result['genre'], f"{relevance:.2%}"))

#     update_pagination_buttons()

# def update_pagination_buttons():
#     next_button.config(state="normal" if current_page * results_per_page < total_results else "disabled")
#     previous_button.config(state="normal" if current_page > 1 else "disabled")


# def search_and_update2():
#     query = entry_2.get().strip()
#     if not query:
#         messagebox.showinfo("Input Error", "Please enter a search term.")
#         return

#     results = search_engine.search(query)

#     for item in table.get_children():
#         table.delete(item)

#     if not results:
#         messagebox.showinfo("No Results", "No matching documents found.")
#         return

#     for idx, score in results:
#         row = data.iloc[idx]
#         table.insert("", "end", values=(row["isbn"], row["title"], row["genre"]))

# def calculate_relevance_example(doc_text):
#     keyword = "example"  
#     return doc_text.lower().count(keyword)

# index_stats_button = Button(window, text="Show Index Stats", command=show_index_stats)
# index_stats_button.place(x=415, y=460)


def sort_table(column, reverse=False):
    table_data = [(table.set(item, column), item) for item in table.get_children()]
    sorted_data = sorted(table_data, key=lambda x: x[0], reverse=reverse)
    for index, (_, item) in enumerate(sorted_data):
        table.move(item, '', index)
    table.heading(column, command=lambda c=column: sort_table(c, not reverse))

for col in selected_columns:
    table.heading(col, text=col.title(), command=lambda c=col: sort_table(c))


table.heading("isbn", text="ISBN")
table.column("isbn", width=50, anchor="center")  

table.heading("title", text="Title")
table.column("title", width=245, anchor="w")

table.heading("genre", text="Genre")
table.column("genre", width=50, anchor="center") 


for _, row in data[selected_columns].iterrows():
    table.insert("", "end", values=tuple(row))

style = ttk.Style()
style.theme_use("default")


style.configure("Treeview", 
                background="#062E44", 
                fieldbackground="#062E44",  
                foreground="white") 


style.configure("Treeview.Heading", 
                background="#062E44",  
                foreground="white")  


style.map("Treeview", 
          background=[("selected", "#41b8d5")],  
          foreground=[("selected", "white")])  

image_label = None


def search_and_update():
    search_term = entry_2.get().strip().lower()
    if not search_term or search_term == "search":
        messagebox.showinfo("Input Error", "Please enter a search term.")
        return

    filtered_data = data[data['desc'].str.contains(search_term, case=False, na=False)]

    for item in table.get_children():
        table.delete(item)

    for _, row in filtered_data[selected_columns].iterrows():
        table.insert("", "end", values=tuple(row))

    if not filtered_data.empty:
        first_match_desc = filtered_data.iloc[0]['desc']
        display_highlighted_text(first_match_desc, search_term)
    else:
        display_highlighted_text("No matching descriptions found.", "")

def display_highlighted_text(text, search_term):
    description_text.delete("1.0", "end")  
    description_text.insert("1.0", text)  
    if search_term:
        start = "1.0"
        while True:
            start = description_text.search(search_term, start, stopindex="end", nocase=True)
            if not start:
                break
            end = f"{start}+{len(search_term)}c"
            description_text.tag_add("highlight", start, end)
            start = end
    description_text.tag_config("highlight", foreground="red")

description_text = Text(window, wrap="word", bg="white", fg="black", font=("Inter", 12), height=10)
description_text.place(x=61, y=250, width=225, height=235)

def on_table_select(event):
    selected_item = table.selection()
    if selected_item:
        item_data = table.item(selected_item[0], "values")
        if item_data:
            book_id = item_data[0]  
            
            book_data = data[data['isbn'].astype(str) == str(book_id)]
            if not book_data.empty:
                description = book_data.iloc[0]['desc']  
                display_highlighted_text(description, entry_2.get().strip().lower()) 
            
            update_selected_info(event, table, canvas, rating_text, author_text, pages_text, image_label, popularity_text)

            
            
button_2.config(command=search_and_update)
button_6.config(command=search_and_update_with_relevance)

def update_table_with_results():
    global current_page, search_results

    # Clear the table
    for item in table.get_children():
        table.delete(item)

    # Calculate start and end indices for the current page
    start_index = (current_page - 1) * results_per_page
    end_index = min(start_index + results_per_page, len(search_results))

    # Insert relevant results into the table
    for result in search_results[start_index:end_index]:
        table.insert("", "end", values=(result["isbn"], result["title"], result["genre"]))

    # Update the pagination buttons
    update_pagination_buttons()
    
def open_plot_window(selected_book_rating, selected_book_format):
    plot_window = Toplevel()
    plot_window.title("Average Rating Curve")
    plot_window.configure(bg="black")

    fig_1 = Figure(figsize=(5, 4), facecolor="#062E44")
    ax_1 = fig_1.add_subplot()

    ax_1.set_facecolor("#062E44")

    bookformat_avg_ratings = data.groupby('bookformat')['rating'].mean()

    rating_range = np.linspace(0, 5, 100)

    ax_1.plot(bookformat_avg_ratings.index, bookformat_avg_ratings.values, label="Avg. Ratings", color="deepskyblue", marker="o")

    ax_1.scatter(selected_book_format, selected_book_rating, color='red', label=f'Selected Book Rating: {selected_book_rating}')

    ax_1.set_xlabel('Book Format', color="white")
    ax_1.set_ylabel('Average Rating', color="white")
    ax_1.set_title('Average Rating Curve with Selected Rating', color="white")
    ax_1.legend()

    ax_1.tick_params(labelsize=7, colors="white")
    ax_1.set_ylim([0, 5])  
    ax_1.grid(visible=True, color='white', linestyle='--', linewidth=0.5)

    plot_canvas = FigureCanvasTkAgg(fig_1, master=plot_window)
    plot_canvas.draw()
    plot_canvas.get_tk_widget().pack()

def on_show_plot_button_click():
    selected_item = table.selection()  
    if not selected_item:
        messagebox.showinfo("No Selection", "Please select a book to view its rating on the curve.")
        return

    row_values = table.item(selected_item, "values")  
    if not row_values or len(row_values) < 1:
        messagebox.showerror("Invalid Selection", "The selected row does not contain enough data.")
        return

    try:
        
        selected_book_id = row_values[0]  
        print(f"Selected book ID: {selected_book_id}")

        selected_book_data = data.loc[data['isbn'] == selected_book_id]  
        if selected_book_data.empty:
            messagebox.showerror("Invalid ID", "The selected book ID was not found in the dataset.")
            return

        selected_book_rating = selected_book_data.iloc[0]['rating']  
        selected_book_format = selected_book_data.iloc[0]['bookformat']  

        print(f"Selected Book Rating: {selected_book_rating}")
        print(f"Selected Book Format: {selected_book_format}")

        if pd.isna(selected_book_rating) or selected_book_rating == '':
            messagebox.showerror("Invalid Rating", "The selected book does not have a valid numeric rating.")
            return
        selected_book_rating = float(selected_book_rating) 
        
        if pd.isna(selected_book_format) or selected_book_format == '':
            messagebox.showerror("Invalid Book Format", "The selected book does not have a valid book format.")
            return
        
        open_plot_window(selected_book_rating, selected_book_format)

    except ValueError as e:
        print(f"Error converting rating to float: {e}")
        messagebox.showerror("Invalid Rating", "The selected book has an invalid rating format.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        messagebox.showerror("Error", "An unexpected error occurred.")


current_page = 1
results_per_page = 10  
total_results = 0





total_docs, top_terms = search_engine.get_index_stats()
print(f"Total Documents: {total_docs}")
print("Top Terms (Weighted Scores and Percentages):")
for term, weight, percentage in top_terms:
    print(f"{term}: {weight:.2f} (Weighted Score), {percentage:.2f}%")


table.place(x=326, y=245, height=240)
table.bind("<<TreeviewSelect>>", lambda event: update_selected_info(event, table, canvas, rating_text, author_text, pages_text, image_label, popularity_text))
table.bind("<Double-1>", lambda event: on_item_double_click(event, table, data, window))

window.resizable(False, False)
window.mainloop()
