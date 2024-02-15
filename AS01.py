import streamlit as st
import pandas as pd
import altair as alt

# Load dataset
data = pd.read_csv('cleaned_food(2).csv')

# Set page layout to wide
st.set_page_config(layout="wide")

# Sidebar with sliders for different filters
fats_range = st.sidebar.slider('Select Fats Range', min_value=data['fats_g'].min(), max_value=data['fats_g'].max(), value=(data['fats_g'].min(), data['fats_g'].max()))
calories_range = st.sidebar.slider('Select Calories Range', min_value=data['calories_kcal'].min(), max_value=data['calories_kcal'].max(), value=(data['calories_kcal'].min(), data['calories_kcal'].max()))
protein_range = st.sidebar.slider('Select Protein Range', min_value=data['protein_g'].min(), max_value=data['protein_g'].max(), value=(data['protein_g'].min(), data['protein_g'].max()))
size_range = st.sidebar.slider('Select Size Range', min_value=data['size'].min(), max_value=data['size'].max(), value=(data['size'].min(), data['size'].max()))

# Filter the DataFrame based on the selected ranges
filtered_df = data[
    (data['fats_g'] >= fats_range[0]) & (data['fats_g'] <= fats_range[1]) &
    (data['calories_kcal'] >= calories_range[0]) & (data['calories_kcal'] <= calories_range[1]) &
    (data['protein_g'] >= protein_range[0]) & (data['protein_g'] <= protein_range[1]) &
    (data['size'] >= size_range[0]) & (data['size'] <= size_range[1])
]

# 1. Scatter Plot with Size and Color Encoding
scatter_chart = alt.Chart(filtered_df).mark_circle().encode(
    x='protein_g',
    y='calories_kcal',
    size='size',
    color='quality',
    tooltip=['size', 'calories_kcal', 'protein_g', 'quality']
).properties(
    width=400,
    height=400
)

# 2. Line Chart Showing Trends Over 'size'
line_chart = alt.Chart(filtered_df).mark_line().encode(
    x='size',
    y='calories_kcal',
    color='quality',
    tooltip=['size', 'calories_kcal', 'quality']
).properties(
    width=400,
    height=400
)

# 3. Histogram of 'calories_kcal'
hist_chart = alt.Chart(filtered_df).mark_bar().encode(
    alt.X('calories_kcal', bin=True),
    y='count()',
    color='quality',
    tooltip=['calories_kcal', 'count()', 'quality']
).properties(
    width=400,
    height=400
)

# 4. Box Plot of 'protein_g' by 'quality'
box_chart = alt.Chart(filtered_df).mark_boxplot().encode(
    x='quality',
    y='protein_g',
    color='quality',
    tooltip=['quality', 'protein_g']
).properties(
    width=400,
    height=400
)

# 5. Pie Chart of 'quality' Distribution
quality_counts = filtered_df['quality'].value_counts().reset_index()
quality_counts.columns = ['quality', 'count']
pie_chart = alt.Chart(quality_counts).mark_circle().encode(
    alt.Size('count:Q', scale=alt.Scale(range=[0, 105000]), legend=None),
    color='quality:N',
    tooltip=['quality', 'count']
).properties(
    width=400,
    height=400
)

# 6. Bar Chart of Average 'calories_kcal' by 'quality'
avg_calories_chart = alt.Chart(filtered_df.groupby('quality')['calories_kcal'].mean().reset_index()).mark_bar().encode(
    x='quality:N',
    y='calories_kcal:Q',
    color='quality:N',
    tooltip=['quality', 'calories_kcal']
).properties(
    width=400,
    height=400
)

# Display the visualizations in a wide layout
col1, col2 = st.columns(2)

with col1:
    st.subheader('Scatter Plot')
    st.altair_chart(scatter_chart)

    st.subheader('Histogram')
    st.altair_chart(hist_chart)

    st.subheader('Pie Chart')
    st.altair_chart(pie_chart)

with col2:
    st.subheader('Line Chart')
    st.altair_chart(line_chart)

    st.subheader('Box Plot')
    st.altair_chart(box_chart)

    st.subheader('Average Calories by Quality')
    st.altair_chart(avg_calories_chart)

# Display correlation matrix as a table
st.subheader('Correlation Matrix')
correlation_matrix = filtered_df.corr()
st.write(correlation_matrix)
