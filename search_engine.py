import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from collections import Counter

class SearchEngine:
    def __init__(self, dataframe, text_columns):
        self.dataframe = dataframe  
        self.text_columns = text_columns  
        self.vectorizer = TfidfVectorizer(
            max_df=0.85,  # Lower max_df to ignore very common terms
            min_df=2,  # Require terms to appear in at least 2 documents
            ngram_range=(1, 3),  # Include trigrams for better context
            stop_words="english"  # Remove English stop words
        )
        self.documents = []  
        self.tfidf_matrix = None  
        self.stop_words = set(stopwords.words("english"))  
        self.lemmatizer = WordNetLemmatizer()  
        self.indexed_data = None  
        self.index_terms = None  

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        return " ".join(lemmatized_tokens)

    def build_index(self):
        all_documents = self.dataframe[self.text_columns[0]].fillna("").apply(self.preprocess_text).tolist()
        self.indexed_data = self.vectorizer.fit_transform(all_documents)
        self.index_terms = self.vectorizer.get_feature_names_out()
        self.tfidf_matrix = self.indexed_data  # Add this line

    def search_with_relevance(self, query, page=1, results_per_page=10):
        if self.tfidf_matrix is None:
            raise ValueError("Index not built yet. Call `build_index` first.")

        processed_query = self.preprocess_text(query)
        query_vector = self.vectorizer.transform([processed_query])
        
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        relevant_indices = similarities.argsort()[::-1]
        total_relevant_docs = (similarities > 0).sum()        
        start_idx = (page - 1) * results_per_page
        end_idx = start_idx + results_per_page
        paginated_results = relevant_indices[start_idx:end_idx]
        
        results = [
            {
                "title": self.dataframe.iloc[idx]["title"],
                "relevance": round(similarities[idx] * 100, 2)
            }
            for idx in paginated_results if similarities[idx] > 0
        ]
        
        return results, total_relevant_docs


    def get_index_stats(self):
        if self.indexed_data is None:
            raise ValueError("Index not built yet. Call `build_index` first.")
        
        # Calculate term frequencies from the TF-IDF matrix
        term_frequencies = self.indexed_data.sum(axis=0).A1  # Sum along columns
        term_frequency_dict = dict(zip(self.vectorizer.get_feature_names_out(), term_frequencies))
        
        # Get the total sum of all term frequencies for normalization
        total_frequency_sum = sum(term_frequency_dict.values())
        
        # Get the top terms based on raw weights
        top_terms_with_weights = Counter(term_frequency_dict).most_common(10)
        
        # Calculate percentages for the top terms
        top_terms_with_percentages = [
            (term, freq, (freq / total_frequency_sum) * 100)  # Include term, raw weight, and percentage
            for term, freq in top_terms_with_weights
        ]
        
        # Total number of documents in the dataset
        total_docs = self.indexed_data.shape[0]

        return total_docs, top_terms_with_percentages
    
    def search(self, query, top_n=None):
        if not hasattr(self, 'indexed_data'):
            raise ValueError("Index not built yet. Call `build_index` first.")

        processed_query = self.preprocess_text(query)
        query_vector = self.vectorizer.transform([processed_query])
        
        similarities = cosine_similarity(query_vector, self.indexed_data).flatten()
        
        relevant_indices = similarities.argsort()[::-1]
        
        results = []
        for i in relevant_indices:
            if similarities[i] > 0:
                results.append({
                    "isbn": self.dataframe.iloc[i]["isbn"],
                    "title": self.dataframe.iloc[i]["title"],
                    "author": self.dataframe.iloc[i]["author"],
                    "genre": self.dataframe.iloc[i]["genre"],
                    "desc": self.dataframe.iloc[i]["desc"],
                    "relevance": round(similarities[i] * 100, 2)
                })
            if top_n is not None and len(results) == top_n:
                break
        
        return results

    


    
   