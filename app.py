import streamlit as st
import pickle
import numpy as np
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import requests

st.set_page_config(page_title="Book Recommendation System", page_icon="📚")
#load Pickle files
popular_df=pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
ratings_df=pickle.load(open('ratings.pkl','rb'))

def lottie_url(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()
lottie_hello = lottie_url('https://assets2.lottiefiles.com/packages/lf20_1a8dx7zj.json')
lottie_contact=lottie_url('https://assets9.lottiefiles.com/packages/lf20_isbiybfh.json')


def recommendation(book_name):
    index = np.where(pt.index == book_name)[0][0]
    distance = similarity_score[index]
    similar_items = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    return data

#navigation bar
selected = option_menu(
    menu_title="Main Menu",
    options=['Home','Top-50 books','Recommend','Contact'],
    icons=['house','bookmark-heart','book','envelope'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal',
)

if selected=='Home':
    st.title("Welcome to the Book Recommendation Application")
    st_lottie(lottie_hello, key='hello')
    st.header('App created by Ronak Pandya')

if selected=='Top-50 books':
    #st.dataframe(popular_df)
    book_title=popular_df['Book-Title'].values
    author = popular_df['Book-Author'].values
    image = popular_df['Image-URL-M'].values
    book_ratings = popular_df['Avg_ratings'].values

    j=0
    for i in range(10):
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            with st.container():
                st.image(image[j])
                st.caption(book_title[j])
                st.caption(f"Author: {author[j]}")
                st.caption(f"Ratings: {book_ratings[j]:0.2f}/10")
            j+=1
        with col2:
            with st.container():
                st.image(image[j])
                st.caption(book_title[j])
                st.caption(f"Author: {author[j]}")
                st.caption(f"Ratings: {book_ratings[j]:0.2f}/10")
            j+=1
        with col3:
            with st.container():
                st.image(image[j])
                st.caption(book_title[j])
                st.caption(f"Author: {author[j]}")
                st.caption(f"Ratings: {book_ratings[j]:0.2f}/10")
            j+=1
        with col4:
            with st.container():
                st.image(image[j])
                st.caption(book_title[j])
                st.caption(f"Author: {author[j]}")
                st.caption(f"Ratings: {book_ratings[j]:0.2f}/10")
            j+=1
        with col5:
            with st.container():
                st.image(image[j])
                st.caption(book_title[j])
                st.caption(f"Author: {author[j]}")
                st.caption(f"Ratings: {book_ratings[j]:0.2f}/10")
            j+=1
        st.markdown("---")

    st.subheader("* Data is taken from kaggle competition. visit: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset for more information")
    st.subheader('** For top 50 criteria, we have choosen only that books which is having number of ratings > 250')

if selected=='Recommend':
    st.title("Select Any Book 📚")
    b_name=list(pt.index)
    option=st.selectbox("",b_name)
    result=recommendation(option)[:5]
    with st.container():
        col1,col2=st.columns(2)
        with col1:
            url=list(books[books['Book-Title']==option]['Image-URL-M'])[0]
            st.image(url, use_column_width='always')
        with col2:
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            b_title= list(books[books['Book-Title']==option]['Book-Title'])[0]
            st.subheader(f"Title: {b_title}")
            b_isbn= list(books[books['Book-Title']==option]['ISBN'])[0]
            st.subheader(f"ISBN: {b_isbn}")
            b_author=list(books[books['Book-Title']==option]['Book-Author'])[0]
            st.subheader(f"Author: {b_author}")
            b_year=list(books[books['Book-Title']==option]['Year-Of-Publication'])[0]
            st.subheader(f"Year of Publication: {b_year}")
            b_publisher=list(books[books['Book-Title']==option]['Publisher'])[0]
            st.subheader(f"Publisher: {b_publisher}")

    st.markdown("----")

    st.header(f"Books similar to {option}")
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(result[0][2])
            st.caption(result[0][0])
            st.caption(f"Authpr: {result[0][1]}")

        with col2:
            st.image(result[1][2])
            st.caption(result[1][0])
            st.caption(f"Authpr: {result[1][1]}")

        with col3:
            st.image(result[2][2])
            st.caption(result[2][0])
            st.caption(f"Authpr: {result[2][1]}")

        with col4:
            st.image(result[3][2])
            st.caption(result[3][0])
            st.caption(f"Authpr: {result[3][1]}")

        with col5:
            st.image(result[4][2])
            st.caption(result[4][0])
            st.caption(f"Authpr: {result[4][1]}")

if selected=='Contact':
    st_lottie(lottie_contact, key='contact')
    st.title("You can Find me on")
    selected_item = option_menu(
        menu_title="Contact me",
        options=['Email', 'Facebook', 'Instagram', 'Twitter','Linkedin', "Github"],
        icons=['envelope', 'facebook', 'instagram', 'twitter','linkedin','github'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal',
    )
#End