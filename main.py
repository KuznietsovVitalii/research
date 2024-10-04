import streamlit as st
import pandas as pd
import os
import altair as alt

# Путь к файлу данных
DATA_FILE = 'data.csv'

# Инициализация данных
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        'Product Link', 'Product name', 'Date of item found', 'Quality', 'Price', 
        'Reviews&Rating', 'Functionality', 'niche filling', 'potential for improvement', 
        'Environmental friendliness and safety', 'Aesthetics', 'Price-performance ratio', 
        'Trend', 'Total points'
    ])

# Заголовок приложения
st.title('Product Review Analyzer')

# Вкладки для организации содержимого
tab1, tab2, tab3, tab4 = st.tabs(["Add product", "Current products", "Product filter", "Remove product"])

with tab1:
    st.header('Enter new product data')
    col1, col2 = st.columns(2)

    with col1:
        product_link = st.text_input('Product Link')
        product_name = st.text_input('Product name')
        date_of_item_found = st.date_input('Date of item found')
        quality = st.number_input('Quality', min_value=1, max_value=10)
        price = st.number_input('Price', min_value=1, max_value=10)
        reviews_rating = st.number_input('Reviews&Rating', min_value=1, max_value=10)

    with col2:
        functionality = st.number_input('Functionality', min_value=1, max_value=10)
        niche_filling = st.number_input('niche filling', min_value=1, max_value=10)
        potential_for_improvement = st.number_input('potential for improvement', min_value=1, max_value=10)
        environmental_friendliness = st.number_input('Environmental friendliness and safety', min_value=1, max_value=10)
        aesthetics = st.number_input('Aesthetics', min_value=1, max_value=10)
        price_performance_ratio = st.number_input('Price-performance ratio', min_value=1, max_value=10)
        trend = st.number_input('Trend', min_value=1, max_value=10)

    total_points = (quality + price + reviews_rating + functionality + niche_filling + 
                    potential_for_improvement + environmental_friendliness + aesthetics + 
                    price_performance_ratio + trend)

    if st.button('Add Product'):
        new_data = pd.DataFrame([{
            'Product Link': product_link,
            'Product name': product_name,
            'Date of item found': date_of_item_found,
            'Quality': quality,
            'Price': price,
            'Reviews&Rating': reviews_rating,
            'Functionality': functionality,
            'niche filling': niche_filling,
            'potential for improvement': potential_for_improvement,
            'Environmental friendliness and safety': environmental_friendliness,
            'Aesthetics': aesthetics,
            'Price-performance ratio': price_performance_ratio,
            'Trend': trend,
            'Total points': total_points
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success('Product added successfully!')

with tab2:
    st.header('Current Products Data')

    # Функция для цветовой кодировки
    def color_code(val):
        color = ''
        if 1 <= val <= 3:
            color = 'red'
        elif 4 <= val <= 7:
            color = 'yellow'
        elif 8 <= val <= 10:
            color = 'green'
        return f'background-color: {color}'

    # Применение цветовой кодировки только к числовым столбцам
    styled_df = df.style.applymap(color_code, subset=[
        'Quality', 'Price', 'Reviews&Rating', 'Functionality', 'niche filling', 
        'potential for improvement', 'Environmental friendliness and safety', 
        'Aesthetics', 'Price-performance ratio', 'Trend'
    ])

    st.dataframe(styled_df)

with tab3:
    st.header('Filter products data')
    quality_filter = st.slider('Quality filter', 1, 10, (1, 10))
    price_filter = st.slider('Price filter', 1, 10, (1, 10))

    filtered_df = df[(df['Quality'] >= quality_filter[0]) & (df['Quality'] <= quality_filter[1]) &
                     (df['Price'] >= price_filter[0]) & (df['Price'] <= price_filter[1])]

    st.dataframe(filtered_df)

    # Визуализация данных
    st.header('Data Visualization')

    chart = alt.Chart(df).mark_bar().encode(
        x='Product name',
        y='Total points',
        color='Total points'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

with tab4:
    st.header('Delete a product')
    index_to_delete = st.number_input('Enter the index of the product to delete', min_value=0, max_value=len(df)-1, step=1)

    if st.button('Delete Product'):
        if len(df) > 0:
            df = df.drop(index_to_delete).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f'Product at index {index_to_delete} deleted successfully!')
        else:
            st.error('No products to delete.')

    # Перезагрузка таблицы после удаления
    styled_df = df.style.applymap(color_code, subset=[
        'Quality', 'Price', 'Reviews&Rating', 'Functionality', 'niche filling', 
        'potential for improvement', 'Environmental friendliness and safety', 
        'Aesthetics', 'Price-performance ratio', 'Trend'
    ])

    st.dataframe(styled_df)
