# Import Python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Initialize Snowflake session
session = get_active_session()

# Set up the Streamlit app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Text input for the name on the smoothie
smoothie_name = st.text_input("Name on smoothie:")

if smoothie_name:
    st.write(f"The name on your smoothie will be: **{smoothie_name}**")

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert Snowflake DataFrame to a list
fruit_options = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Display multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    options=fruit_options,
    max_selections=5
)

# Initialize the ingredients_string variable
ingredients_string = ''

# Process the selected ingredients
if ingredients_list:
    # Join selected fruits with commas
    ingredients_string = ', '.join(ingredients_list)
    st.write(f"You've selected: {ingredients_string}")

# Add a "Submit Order" button
if st.button('Submit Order'):
    if smoothie_name and ingredients_string:
        # Prepare SQL statement
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (smoothie_name, ingredients)
        VALUES ('{smoothie_name}', '{ingredients_string}');
        """
        
        st.write(f"SQL Statement: {my_insert_stmt}")

        # Execute SQL statement and provide feedback
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your smoothie is ordered! ✅')
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif not smoothie_name:
        st.warning('Please enter a name for your smoothie before submitting your order.')
    else:
        st.warning('Please select at least one ingredient before submitting your order.')
