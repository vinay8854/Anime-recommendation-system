# ⚡ Ultra-Fast Anime Recommendation System (v2) ⚡

A high-performance, content-based recommendation system that finds similar anime in **under one second** by analyzing the *semantic meaning of their genres*.

This project uses a **Sentence Transformer** model to convert genre combinations (e.g., "Action, Adventure, Shounen") into vector embeddings. These are stored and indexed in a **Pinecone** vector database for ultra-fast "nearest neighbor" search.

**Live Demo:** https://anime-recommendation-system-6860.onrender.com/
*(Note: The app may take 30-60 seconds to "wake up".)*



---

## 📖 Overview

The goal was to build a recommendation system that was both fast and intelligent. This project solves that by focusing on the *content* of the anime, specifically its **genres**.

The core idea is that genres like "Action, Adventure" are semantically closer to "Action, Sci-Fi" than they are to "Romance, Slice of Life." This model "understands" that relationship.

This project is built in two phases:
1.  **Indexing:** A one-time process where the genre string for *every* anime in the dataset is converted into a vector embedding using the `all-MiniLM-L6-v2` model. These vectors are then stored in Pinecone.
2.  **Querying:** A live Flask app that takes a user's input, finds that anime's genre vector, and then instantly queries Pinecone to find the 5 "closest" vectors (i.e., the most similar anime).

## ✨ Features

* **Sub-Second Speed:** Returns the top 5 recommendations in less than 1 second.
* **Vector Search:** Uses a **Pinecone** vector database for state-of-the-art "Approximate Nearest Neighbor" (ANN) search.
* **Semantic Genre Matching:** Uses the `all-MiniLM-L6-v2` Sentence Transformer to understand the *meaning* and *relationship* between genres, providing smarter recommendations than simple keyword matching.
* **Scalable:** This architecture can scale to millions of anime with minimal loss in performance.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Vector Database:** **Pinecone**
* **NLP / Vectorization:** **Sentence-Transformers** (`all-MiniLM-L6-v2`)
* **Data Handling:** Pandas, NumPy
* **Deployment:** Render

---

## 🚀 How It Works: The Architecture

### 1. The Indexing Pipeline (Done once, offline)
This is how we "teach" the system about the anime.

1.  **Load Data:** Load the raw `anime.csv` into a Pandas DataFrame.
2.  **Load Model:** Load the `all-MiniLM-L6-v2` model.
3.  **Create Embeddings:** For *each* anime, get its `genre` string (e.g., "Action, Fantasy, Magic"). Use the model to encode this string into a 384-dimension vector embedding.
4.  **Upload to Pinecone:** Create an index in Pinecone and "upsert" (upload) all the vectors, each one mapped to its unique `anime_id`.

### 2. The Recommendation App (The live app)
This is what the user interacts with (your `app.py`).

1.  **User Input:** The user types in an anime name (e.g., "Naruto").
2.  **Find Genre:** The app finds "Naruto" in the `anime.csv` and gets its corresponding genre string: `"Action, Adventure, Martial Arts"`.
3.  **Create Query Vector:** The app uses the *same* `all-MiniLM-L6-v2` model to encode this *single* genre string into a query vector, on the fly.
4.  **Query Pinecone:** The app sends this query vector to Pinecone and asks, "Find the Top 5 vectors in the database that are *closest* to this one."
5.  **Return Results:** Pinecone instantly returns the `anime_id`s of the 5 most similar anime. The app looks up their names from the `df` and displays them to the user.

---

Screenshots
<img width="1907" height="956" alt="image" src="https://github.com/user-attachments/assets/42dcda98-761d-4737-90cd-95bac47c9af8" />
<img width="1889" height="882" alt="image" src="https://github.com/user-attachments/assets/9040fac4-751c-4607-956f-417054d46cb2" />

