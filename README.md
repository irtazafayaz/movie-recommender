# 🎬 Movie Recommender System

A content-based movie recommendation system built with Python and Streamlit that suggests movies based on your preferences using machine learning.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **Smart Recommendations**: Get personalized movie suggestions based on content similarity
- **Rich Movie Details**: View posters, ratings, genres, runtime, and descriptions
- **Interactive UI**: Clean and intuitive interface built with Streamlit
- **Customizable Results**: Choose how many recommendations you want (3-10)
- **TMDB Integration**: Real-time movie data and posters from The Movie Database

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/irtazafayaz/movie-recommender.git
   cd movie-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the required pickle files**
   
   The `movies.pkl` and `similarity.pkl` files are not included in the repository due to their large size. You need to generate them by running the Jupyter notebook:
   
   ```bash
   jupyter notebook movie-recommender-system.ipynb
   ```
   
   **Important**: Run all cells in the notebook, especially the **last cell** which saves the pickle files:
   ```python
   pickle.dump(movies, open('movies.pkl', 'wb'))
   pickle.dump(similarity, open('similarity.pkl', 'wb'))
   ```
   
   This will create:
   - `movies.pkl` - Contains the movie dataset
   - `similarity.pkl` - Contains the similarity matrix for recommendations

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
movie-recommender/
│
├── app.py                          # Main Streamlit application
├── movie-recommender-system.ipynb  # Jupyter notebook for data processing
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
│
└── (Generated files - not in repo)
    ├── movies.pkl                  # Movie dataset (generated)
    └── similarity.pkl              # Similarity matrix (generated)
```

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning for similarity computation
- **Requests**: API calls to TMDB
- **Pickle**: Serialization of data structures

## 🎯 How It Works

1. **Data Processing**: The notebook processes movie data and creates a similarity matrix using content-based filtering
2. **Recommendation Engine**: Calculates cosine similarity between movies based on features like genres, cast, crew, and keywords
3. **User Interface**: Streamlit provides an interactive interface to select movies and view recommendations
4. **Movie Details**: Real-time data fetched from TMDB API for rich movie information

## 📝 Usage

1. Select a movie from the dropdown menu
2. Adjust the number of recommendations using the slider
3. Click "Get Recommendations" button
4. Browse through personalized movie suggestions with detailed information

## 🔑 API Key

The app uses The Movie Database (TMDB) API. The API key is included in the code for demo purposes. For production use, please:

1. Get your own API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Replace the API key in `app.py`
3. Consider using environment variables to store sensitive keys

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the movie data API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- All contributors and supporters of this project

## 📧 Contact

Irtaza Fayaz - [@irtazafayaz](https://github.com/irtazafayaz)

Project Link: [https://github.com/irtazafayaz/movie-recommender](https://github.com/irtazafayaz/movie-recommender)

---

⭐ If you found this project helpful, please give it a star!
