from basket_analysis import *
import streamlit as st
# set the app title
st.title('Market Basket Recommender')

items=get_items()
items.insert(0, None)
    
selected_item = st.selectbox('Select an item:',items)
if selected_item is not None:
    st.write('You Can Also buy : ')
    df=find_combos(selected_item)
    name_column_html = df['consequents'].to_frame().to_html(index=False, header=False)
    st.markdown(name_column_html, unsafe_allow_html=True)