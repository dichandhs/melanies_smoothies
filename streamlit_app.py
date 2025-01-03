# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie ! :cup_with_straw:")
st.write(
    """Choose the furits you want to in your custom smoothie!
    """
)


# option = st.selectbox(
#     "What is your favorite fruit ?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favorite fruit is:", option)

name_on_order = st.text_input("Name on Smoothie:")
st.write("Name on your Smoothie will be: ", name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session=cnx.session() 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingradient_list = st.multiselect('Choose upto 5 ingradients:',my_dataframe,max_selections=5)

if ingradient_list:
    # st.write(ingradient_list)
    # st.text(ingradient_list)
    
    ingredients_string=''
    for fruit_choosen in ingradient_list:
        ingredients_string += fruit_choosen + ' '
    
    # st.write(ingredients_string) 
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

