# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


title = st.text_input("Name on Smoothie")
#st.write("The name on yout Smoothie will be:",title)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)


if ingredients_list :                           
        ingredients_string=''
        for fruit_chosen in ingredients_list:
            ingredients_string+=fruit_chosen + ' '
        #st.write(ingredients_string)
        order_filled=False
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+title+"""')"""

        #st.write(my_insert_stmt)
        submit_button=st.button("Submit Order")
        if submit_button:
          session.sql(my_insert_stmt).collect()
          st.success('Your Smoothie is ordered!,'''+title+'!',icon="✅") 
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

