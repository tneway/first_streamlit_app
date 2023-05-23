import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title("My parents healthy diner")

# streamlit.header('Breakfast Menu')
# streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
# streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
# streamlit.text('🐔 Hard-Boiled Free-Range Egg')
# streamlit.text('🥑🍞 Avocado toast')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
#streamlit.dataframe(my_fruit_list)
# display the table on the page
st.dataframe(fruits_to_show)

#import requests

def get_fruityvice_data(fruit_choice):        
    # write your own comment -what does the next line do? 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
        # write your own comment - what does this do?
    return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?','')
    if not fruit_choice:
        st.error("please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()

# don't run anythng below
#st.stop()

st.header("The furit load list contains:")
# snowflake related function 
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# Add a button to load the fruit
if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('from streamlit');")
        return "Thanks for adding " + new_fruit
    
add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    st.text(back_from_function)

# my_cur.execute("select * from fruit_load_list")
# my_data_rows=my_cur.fetchall()
# st.header("The fruit load list contains:")
# st.dataframe(my_data_rows)
# second_choice = st.text_input("What fruit would you like to add","kiwi")
# st.write("enteer fruit", second_choice)
# st.text("Thanks for enrering : " + second_choice)
# my_cur.execute("insert into fruit_load_list values('from streamlit');")