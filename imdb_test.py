from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Correct headers to act like a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# Downloading IMDb Top 250 movie's data with headers
url = 'https://www.imdb.com/chart/top'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extracting data
movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.strong.text if b.strong else "" for b in soup.select('td.imdbRating')]

# Store data in a list
movie_list = []

for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    match = re.search(r'\((.*?)\)', movie_string)
    year = match.group(1) if match else ""
    place = index + 1  # Fixed place numbering
    data = {
        "place": place,
        "movie_title": movie_title,
        "rating": ratings[index],
        "year": year,
        "star_cast": crew[index],
    }
    movie_list.append(data)

# Display results
for movie in movie_list:
    print(f"{movie['place']} - {movie['movie_title']} ({movie['year']}) - Starring: {movie['star_cast']} - Rating: {movie['rating']}")

# Save to CSV
df = pd.DataFrame(movie_list)
df.to_csv('imdb_top_250_movies.csv', index=False)
print(df)
print(response.text[:500])
#print (data)
print(len(movies), len(crew), len(ratings))
print("Movies found:", len(movies))
print("Crew found:", len(crew))
print("Ratings found:", len(ratings))
print(response.text[:500])  # See what you actually got