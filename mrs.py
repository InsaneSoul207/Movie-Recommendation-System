import sys
import pandas as pd
import ast
from PyQt5 import QtWidgets, QtGui, QtCore

# Load the dataset
df = pd.read_csv('tmdb_5000_movies.csv')

class MovieRecommendationApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Movie Recommendation System')
        self.setGeometry(100, 100, 800, 600)

            # Set dark theme with updated fonts and sizes
        self.setStyleSheet("""
            background-color: #2E2E2E; 
            color: #FFFFFF; 
            font-family: 'Helvetica Neue', Arial, sans-serif;  /* Changed font family */
            font-size: 20px;  /* Default font size for the entire application */
            QComboBox {
                background-color: #444444; 
                color: #FFFFFF; 
                border: 1px solid #666666; 
                border-radius: 10px;
                padding: 10px;
                font-size: 20px;  /* Increased font size for ComboBox */
            }
            QLineEdit {
                background-color: #444444; 
                color: #FFFFFF; 
                border: 1px solid #666666; 
                border-radius: 10px;
                padding: 10px;
                font-size: 20px;  /* Increased font size for LineEdit */
            }
            QLineEdit::placeholder {
                color: #AAAAAA;  /* Placeholder text color */
            }
            QPushButton {
                background-color: #555555; 
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
                font-size: 20px;  /* Increased font size for buttons */
            }
            QPushButton:hover {
                background-color: #666666;
                border-radius: 10px;
            }
            QListWidget {
                background-color: #333333; 
                border: 1px solid #666666; 
                border-radius: 10px;
                font-size: 20px;  /* Increased font size for list widget */
            }
            QStatusBar {
                background-color: #444444;
                color: #FFFFFF;
                font-size: 20px;  /* Font size for status bar */
            }
            QLabel {
                font-size: 20px;  /* Increased font size for labels */
                font-weight: bold;  /* Bold font for labels */
            }
        """)
        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Create header
        header = QtWidgets.QLabel("Movie Recommendation System")
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(header)

        # Create input layout
        input_layout = QtWidgets.QGridLayout()
        input_layout.setSpacing(10)

        # Dropdown for categories
        self.category_combo = QtWidgets.QComboBox(self)
        self.category_combo.addItems(["Genre", "Similar Movie"])
        input_layout.addWidget(self.category_combo, 0, 0, 1, 2)

        # Input field for search term
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("Enter your search term...")
        input_layout.addWidget(self.input_field, 1, 0, 1, 2)

        # Input field for number of recommendations
        self.num_recommendations_field = QtWidgets.QLineEdit(self)
        self.num_recommendations_field.setPlaceholderText("Number of movies (default is 5)...")
        input_layout.addWidget(self.num_recommendations_field, 2, 0, 1, 2)

        # Search button
        self.search_button = QtWidgets.QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_movies)
        input_layout.addWidget(self.search_button, 3, 0)

        # Clear button
        self.clear_button = QtWidgets.QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_inputs)
        input_layout.addWidget(self.clear_button, 3, 1)

        # Add input layout to main layout
        self.main_layout.addLayout(input_layout)

        # Movie list
        self.movie_list_widget = QtWidgets.QListWidget(self)
        self.main_layout.addWidget(self.movie_list_widget)

        # Status bar
        self.status_bar = QtWidgets.QStatusBar(self)
        self.main_layout.addWidget(self.status_bar)

        # Set main layout
        self.setLayout(self.main_layout)

    def search_movies(self):
        category = self.category_combo.currentText()
        search_term = self.input_field.text()
        num_recommendations = 5  # Default number of recommendations

        # Get the number of recommendations from the input field
        try:
            if self.num_recommendations_field.text():
                num_recommendations = int(self.num_recommendations_field.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a valid number for recommendations.")
            return

        if category == "Genre":
            recommended_movies = self.recommend_movies_by_genre(search_term, num_recommendations)
        elif category == "Actor":
            recommended_movies = self.recommend_movies_by_actor(search_term, num_recommendations)
        elif category == "Budget":
            try:
                budget = int(search_term)
                recommended_movies = self.recommend_movies_by_budget(budget, num_recommendations)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a valid budget.")
                return
        elif category == "Similar Movie":
            recommended_movies = self.find_similar_movies(search_term, num_recommendations)
        else:
            recommended_movies = []

        self.display_movies(recommended_movies)

    def clear_inputs(self):
        self.input_field.clear()
        self.num_recommendations_field.clear()
        self.movie_list_widget.clear()
        self.status_bar.clearMessage()

    def recommend_movies_by_genre(self, genre, num_recommendations):
        recommendations = df[df['genres'].apply(lambda x: genre.lower() in [g['name'].lower() for g in ast.literal_eval(x)])]
        if recommendations.empty:
            return []
        num_recommendations = min(num_recommendations, len(recommendations))
        recommended_movies = recommendations.sample(n=num_recommendations, random_state=1)
        return recommended_movies[['title']].values.tolist()

    # def recommend_movies_by_actor(self, actor, num_recommendations):
    #     recommendations = df[df['cast'].apply(lambda x: actor.lower() in [a['name'].lower() for a in ast.literal_eval(x)])]
    #     if recommendations.empty:
    #         return []
    #     num_recommendations = min(num_recommendations, len(recommendations))
    #     recommended_movies = recommendations.sample(n=num_recommendations, random_state=1)
    #     return recommended_movies[['title']].values.tolist()

    # def recommend_movies_by_budget(self, budget, num_recommendations):
    #     recommendations = df[df['budget'] <= budget]
    #     if recommendations.empty:
    #         return []
    #     num_recommendations = min(num_recommendations, len(recommendations))
    #     recommended_movies = recommendations.sample(n=num_recommendations, random_state=1)
    #     return recommended_movies[['title']].values.tolist()

    def find_similar_movies(self, movie_title, num_recommendations):
        movie = df[df['title'].str.lower() == movie_title.lower()]
        if movie.empty:
            QtWidgets.QMessageBox.warning(self, "Movie Not Found", "The specified movie was not found.")
            return []

        genres = ast.literal_eval(movie.iloc[0]['genres'])
        genre_names = [g['name'].lower() for g in genres]

        recommendations = df[df['genres'].apply(lambda x: any(genre.lower() in [g['name'].lower() for g in ast.literal_eval(x)] for genre in genre_names))]
        recommendations = recommendations[recommendations['title'].str.lower() != movie_title.lower()]

        if recommendations.empty:
            return []
        num_recommendations = min(num_recommendations, len(recommendations))
        recommended_movies = recommendations.sample(n=num_recommendations, random_state=1)
        return recommended_movies[['title']].values.tolist()

    def display_movies(self, movies):
        self.movie_list_widget.clear()
        for title in movies:
            item = QtWidgets.QListWidgetItem(title[0])
            self.movie_list_widget.addItem(item)
        self.status_bar.showMessage(f"Displayed {len(movies)} recommendations.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MovieRecommendationApp()
    window.show()
    sys.exit(app.exec_())