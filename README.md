# 📚 BookNest – Book Search Engine

**BookNest** is a powerful desktop application for searching and exploring books using advanced Natural Language Processing (NLP) techniques. Built with Python and leveraging the **Goodreads Books 100k** dataset, the application offers keyword search, tag-based filtering, statistical visualizations, and intelligent text-based matching using **TF-IDF** and **Cosine Similarity**.

> 👤 **Presented by:** Polihronis Varvaris  
> 💻 **Tools Used:** Python, Keras, NLTK, Pandas, VS Code  

---

## 🗂️ Features

### 🔍 Search Functionality

- **Basic Search (button_1):**  
  Search using title, ISBN, or genre keywords from a user input field (`entry_1`). Results are filtered strictly based on table content.

- **Description Search (button_2):**  
  Full-text search in the `description` field. Matching keywords are **highlighted** in the results for better clarity.

- **Advanced NLP Search (button_6):**  
  Uses techniques like **TF-IDF**, **lemmatization**, **stemming**, and **stop-word removal** to find the top 30 most relevant books based on user input (`entry_2`). Relevance percentages are shown in the terminal.

---

## 🔎 Tag-Based Filtering

Users can select **multiple tags** (genres) to filter books more precisely. Ideal for discovering books by category or specific characteristics.

---

## 📊 Graphical Statistics

Interactive visualizations provide insights based on book metadata:
- Rating distributions
- Popular genres
- Page counts
- Trending titles

---

## 💾 Export Functionality

- Export the current book table view to a **CSV file**, enabling further analysis, sharing, or offline use.

---

## 📂 Dataset: Goodreads Books 100k

- 📥 Source: [Kaggle – Goodreads Books 100k](https://www.kaggle.com/datasets/mdhamani/goodreads-books-100k/data)  
- 📘 Contains metadata for 100,000 books including:

| Field        | Description |
|--------------|-------------|
| `Title`         | Title of the book |
| `Author`        | Author(s) of the book |
| `Genre`         | Categories such as fiction, fantasy, sci-fi, etc. |
| `BookFormat`    | Physical or digital |
| `Desc`          | Short description |
| `Pages`         | Page count |
| `Rating`        | Average Goodreads rating |
| `Reviews`       | Number of user reviews |
| `TotalRatings`  | Total number of ratings |
| `ISBN`, `ISBN13`| Identifiers |
| `Img`           | Cover image URL |
| `Link`          | Link to Goodreads page |

---

## 🧠 NLP Pipeline

The application incorporates a multi-step **text preprocessing pipeline** for advanced search:

### 📌 `preprocess_text()`
- **Tokenization:** Splits text into words
- **Stop-Words Removal:** Removes unimportant common words (e.g. *the*, *and*)
- **Lemmatization:** Returns words to their base form
- **Stemming:** Strips suffixes to obtain root words

### 🧾 `build_index()`
- Uses **TF-IDF Vectorizer** to build a document-term matrix
- Stores indexed vectors for fast similarity computation

### 🔎 `search_with_relevance()`
- Matches queries using **Cosine Similarity**
- Displays top 30 most relevant books based on vector similarity

---

## 📈 Accuracy & Performance

| NLP Technique          | Description                                             | Accuracy |
|------------------------|---------------------------------------------------------|----------|
| Tokenization           | Word segmentation                                       | >99%     |
| Stop-Words Removal     | Filter non-informative words                            | >99%     |
| Lemmatization          | Base form of words considering syntax                   | >95%     |
| Stemming               | Root extraction by suffix removal                       | ~90%     |
| POS Tagging            | Part-of-speech tagging                                  | ~92-95%  |
| Synonym Detection      | Recognizing similar meaning words                       | ~88%     |
| Cosine Similarity (TF-IDF) | Semantic relevance calculation                      | ~90-95%  |

---

## 🏁 How to Run

```bash
git clone https://github.com/yourusername/BookNest.git
cd BookNest
pip install -r requirements.txt
python main.py

    Make sure the Goodreads 100k dataset CSV is placed correctly in the project folder.

📝 License

This project is licensed under the MIT License.
🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or improve.
👤 Author

Polihronis Varvaris
