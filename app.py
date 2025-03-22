





from flask import Flask, request, render_template_string
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from pinecone import Pinecone

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("anime.csv")  # Make sure the dataset is in the same directory

# Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone
pc = Pinecone(api_key="pcsk_75FpV7_93gHSL6Jzngiboc6SwrmWXrUbFFH7e5YmCJLQwVEZPyo9ujpS6q4A4NK6qLqvtE")  # Replace with your API key
index = pc.Index("anime-search")  # Your Pinecone index name

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Anime Recommendation</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h2>🔥 Anime Recommendation System</h2>
        <form method="POST">
            <input type="text" name="anime" placeholder="Enter Anime Name" required>
            <button type="submit">Recommend</button>
        </form>
        {% if recommendations %}
            <h3>Top Recommendations:</h3>
            <ul>
                {% for anime in recommendations %}
                    <li>{{ anime }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
</body>
</html>
"""


def get_similar_anime(anime_name, top_k=5):
    """Finds similar anime based on the given anime name."""
    anime_name = anime_name.strip().lower()
    
    # Find the anime in the dataset
    anime_row = df[df['name'].str.lower() == anime_name]

    if anime_row.empty:
        return ["❌ Anime not found in the dataset."]
    
    # Get genre and encode it
    genre = anime_row.iloc[0]['genre']
    query_embedding = model.encode(genre).tolist()

    # Query Pinecone
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    # Convert IDs to anime names
    anime_ids = [match['id'] for match in results['matches']]
    anime_names = df[df['anime_id'].astype(str).isin(anime_ids)]['name'].tolist()

    # Format the output
    formatted_output = [f"🔥 {i+1}. {name}" for i, name in enumerate(anime_names)]
    
    return formatted_output

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    if request.method == "POST":
        anime_name = request.form.get("anime")
        try:
            recommendations = get_similar_anime(anime_name)
        except Exception as e:
            recommendations = [f"Error: {str(e)}"]
    return render_template_string(HTML_TEMPLATE, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
