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


st.header("Fruityvice Fruit Advice!")
try:
   # fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        st.write('The user entered ', fruit_choice)
    else:
        # write your own comment -what does the next line do? 
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
        # write your own comment - what does this do?
        st.dataframe(fruityvice_normalized)
except URLError as e:
    st.error()

# don't run anythng below
st.stop()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
st.text("Hello from Snowflake:")
st.text(my_data_row)


my_cur.execute("select * from fruit_load_list")
my_data_rows=my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)
second_choice = st.text_input("What fruit would you like to add","kiwi")
st.write("enteer fruit", second_choice)
st.text("Thanks for enrering : " + second_choice)
my_cur.execute("insert into fruit_load_list values('from streamlit');")