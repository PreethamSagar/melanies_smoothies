# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
connection = st.connection("snowflake")
session = connection.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """**Choose the fruits you want in your customer**"""
)
title = st.text_input('Name on Smoothie:','')
st.write('The name on Smoothie will be: ',title)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data = my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)
if len(ingredients_list) != 0:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+ ' '
        st.subheader(fruit_choosen+' Nutrition Informaion')
        search_on = session.table("smoothies.public.FRUIT_OPTIONS").filter(col("FRUIT_NAME")==fruit_choosen).select(col("SEARCH_ON")).collect()
        dummy = search_on[0]
        st.write(search_on)
        st.write(dummy)
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        fv_df = st.data_editor(data = fruityvice_response.json(), use_container_width = True)
    # st.write(ingredients_string)
    my_insert_statement = "insert into smoothies.public.orders(ingredients, name_on_order) values ('"+ingredients_string+"','"+title+"')"
    submit_button = st.button('Submit Order')
    
    # st.write(my_insert_statement)
    if submit_button:
        session.sql(my_insert_statement).collect()
        st.success(f'Your Smoothie is Ordered, {title}!', icon='✅')
