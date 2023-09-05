import streamlit as st
import pandas as pd
import joblib #to load the recommendation model
from sklearn.metrics.pairwise import cosine_similarity
movies = pd.read_csv('D:/Documents/DataScience2/WBS/MyNotebooks/DataEngineeringProject/Movie/movies.csv')
ratings = pd.read_csv('D:/Documents/DataScience2/WBS/MyNotebooks/DataEngineeringProject/Movie/ratings.csv')
tags = pd.read_csv('D:/Documents/DataScience2/WBS/MyNotebooks/DataEngineeringProject/Movie/tags.csv')
links = pd.read_csv('D:/Documents/DataScience2/WBS/MyNotebooks/DataEngineeringProject/Movie/links.csv')
df = pd.read_csv('D:/Documents/DataScience2/WBS/MyNotebooks/DataEngineeringProject/MovieGenre.csv', encoding="ISO-8859-1", usecols=["imdbId", "Title", "Genre", "Poster"])
df['title']= df['Title']
df.drop('Title', axis =1, inplace=True)

movie_ratings = movies.merge(ratings, how = 'inner', on = 'movieId')


# model = joblib.load('your_model.pkl')

# title of the recommender app
# building the app with Sebastain & Mirella

st.title('Welcome to SMG Movies')
st.text('here we recommend movies based on user rating and popularity')

option = st.selectbox(
    'Please choose a movie that you like',
    movie_ratings['title'].unique())
#st.button('Submit')



def top_rated_movies():
    movie_ratings = movies.merge(ratings, how = 'inner', on = 'movieId')
    average_ratings = movie_ratings.groupby('title').agg({'movieId':'count', 'rating' : 'mean'})\
                              .rename(columns = {'movieId': 'number_of_ratings', 'rating' : 'average_rating'})\
                              .sort_values(by = ['average_rating', 'number_of_ratings'], ascending = [False, False]).reset_index()
    
    average_ratings['popularity_score'] = (average_ratings['average_rating']*0.4 + average_ratings['number_of_ratings']*0.6) / (average_ratings['average_rating'] + average_ratings['number_of_ratings'])
    
    result = average_ratings.loc[average_ratings['average_rating']>=4.5][['title', 'average_rating']].head(15).merge(df, how = 'inner', on = 'title')
    result['average_rating'] = round(result['average_rating'], 1)
    return result[['title', 'average_rating', 'Poster']]


def top_popular_movies():
    movie_ratings = movies.merge(ratings, how = 'inner', on = 'movieId')
    average_ratings = movie_ratings.groupby('title').agg({'movieId':'count', 'rating' : 'mean'})\
                              .rename(columns = {'movieId': 'number_of_ratings', 'rating' : 'average_rating'})\
                              .sort_values(by = 'number_of_ratings', ascending = False).reset_index()  #, 'average_rating']
    
    # average_ratings['popularity_score'] = (average_ratings['average_rating']*0.4 + average_ratings['number_of_ratings']*0.6) / (average_ratings['average_rating'] + average_ratings['number_of_ratings'])
    
    result = average_ratings.loc[average_ratings['average_rating']>=4.5][['title', 'average_rating']].head(15).merge(df, how = 'inner', on = 'title')
    result['average_rating'] = round(result['average_rating'], 1)
    return result[['title', 'average_rating', 'Poster']]


# user-collaborative filtering
def related_movies(title):
    
    movie_ratings = movies.merge(ratings, how = 'inner', on = 'movieId')
    movie = str(title)
    movie_id = movies.loc[movies['title']==movie].iloc[0,0]
    movie_matrix = pd.pivot_table(movie_ratings,
                            columns='movieId',
                            index = 'userId',
                            values = 'rating',
                            aggfunc='mean',
                            fill_value=0)
    
    movie_cosine =pd.DataFrame(cosine_similarity(movie_matrix.T),
                              columns=movie_matrix.columns,
                              index = movie_matrix.columns)
    movie_df = pd.DataFrame(movie_cosine[movie_id]).rename(columns={movie_id : 'cosine_similarity'})
    movie_df = movie_df[movie_df.index != movie_id].sort_values(by = 'cosine_similarity', ascending=False)

    no_of_rating_for_both_movies = [sum((movie_matrix[movie_id] > 0) & (movie_matrix[movie_id])) for movie_ids in movie_df.index]
    movie_df['common_movie_raters'] = no_of_rating_for_both_movies 
    results = movie_df[movie_df['common_movie_raters']>7].head(10).reset_index()\
                .merge(movie_ratings, how='inner', on ='movieId')\
                .groupby(['movieId','title']).agg({'rating':'mean', 'common_movie_raters' : 'mean'}).reset_index()\
                .sort_values('rating', ascending=False).head(15).merge(df, how = 'inner', on = 'title')

    results['rating'] = round(results['rating'], 1)
    return results[['title','rating', 'Poster']]



def app_interaction():
    st.subheader("Top Movies today")
    
    # Call your top_rated_movies function
    top_movies = top_rated_movies()

    
    if not top_movies.empty:
        
        columns = st.columns(len(top_movies))
        
        for index, row in top_movies.iterrows():
            with columns[index]:
                st.image(row['Poster'], caption=row['title'], width=None, use_column_width='auto')
   # else:
    #    st.warning("No top-rated movies found.")
     #   st.dataframe(top_movies)
    else:
        st.warning("No top-rated movies found.")
        
    
    st.subheader('Popular Movies today')
    
    popular_movies = top_popular_movies()
    
    if not popular_movies.empty:
        columns = st.columns(len(popular_movies))
        
        for index, row in popular_movies.iterrows():
            
            with columns[index]:
                
                st.image(row['Poster'], caption=row['title'], width=None, use_column_width='auto')
    else:
        
        st.warning('No Popular movies found')
                
            
    
        
    st.subheader(f"Because you liked {option}, you might also like...")
    
    if option:
        
        movie_rec = related_movies(option)
        
        if not movie_rec.empty:
            columns = st.columns(len(movie_rec))
            for index, row in movie_rec.iterrows():
                
                with columns[index]:
                    st.image(row['Poster'], caption=row['title'], width=None, use_column_width='auto')
               # st.write(f"Title: {row['title']}")
                #st.write(f"Rating: {row['rating']}")
                # st.image(row['Poster'], caption=row['title'], use_column_width=True)
        else:
            st.warning(f"No related movies found for {option}.")

    
    
    
    
    

# option = st.

st.text("")
#st.write('You selected:', option)




if __name__ == "__main__":
    app_interaction()


# Add a footer to your app
st.markdown('------')
st.write("Built with Streamlit by Mirella, Grace and Sebastian")
