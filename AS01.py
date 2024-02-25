import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
# Load dataset
data = pd.read_csv('cleaned_food(2).csv')

# Set page layout to wide
st.set_page_config(layout="wide")

# Define a function to create the visualization based on user input
def create_dashboard_1():
    # Dashboard 1
    st.subheader('Dashboard 1 - Visualizations')

    # Visualization 1: Scatter Plot
    st.subheader('Scatter Plot')
    fats_range = st.slider('Select Fats Range', min_value=data['fats_g'].min(), max_value=data['fats_g'].max(), value=(data['fats_g'].min(), data['fats_g'].max()))
    calories_range = st.slider('Select Calories Range', min_value=data['calories_kcal'].min(), max_value=data['calories_kcal'].max(), value=(data['calories_kcal'].min(), data['calories_kcal'].max()))
    protein_range = st.slider('Select Protein Range', min_value=data['protein_g'].min(), max_value=data['protein_g'].max(), value=(data['protein_g'].min(), data['protein_g'].max()))
    size_range = st.slider('Select Size Range', min_value=data['size'].min(), max_value=data['size'].max(), value=(data['size'].min(), data['size'].max()))

    # Filter the DataFrame based on the selected ranges
    filtered_df_scatter = data[
        (data['fats_g'] >= fats_range[0]) & (data['fats_g'] <= fats_range[1]) &
        (data['calories_kcal'] >= calories_range[0]) & (data['calories_kcal'] <= calories_range[1]) &
        (data['protein_g'] >= protein_range[0]) & (data['protein_g'] <= protein_range[1]) &
        (data['size'] >= size_range[0]) & (data['size'] <= size_range[1])
    ]

    scatter_chart = alt.Chart(filtered_df_scatter).mark_circle().encode(
        x='protein_g',
        y='calories_kcal',
        size='size',
        color='quality',
        tooltip=['size', 'calories_kcal', 'protein_g', 'quality']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(scatter_chart)

    
   # Visualization 2: Bar Chart
    st.subheader('Bar Chart')

    # Add an interactive filter for Size range using slider
    size_range_bar = st.slider('Select Size Range for Bar Chart', min_value=data['size'].min(), max_value=data['size'].max(), value=(data['size'].min(), data['size'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_bar = sorted(data['quality'].unique())
    selected_quality_bar = st.multiselect('Select Quality for Bar Chart', quality_values_bar, default=quality_values_bar)

    # Filter the DataFrame for Bar Chart
    filtered_df_bar_chart = data[(data['size'] >= size_range_bar[0]) & (data['size'] <= size_range_bar[1]) & (data['quality'].isin(selected_quality_bar))]

    # Create the Bar Chart
    bar_chart = alt.Chart(filtered_df_bar_chart).mark_bar().encode(
        x='size:O',  # Use ordinal scale for discrete values like 'size'
        y='mean(calories_kcal):Q',  # Use mean instead of raw values for better representation
        color='quality:N',
        tooltip=['size:O', 'mean(calories_kcal):Q', 'quality:N']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(bar_chart)




    # Visualization 3: Histogram
    st.subheader('Histogram')

    # Add an interactive filter for Calories range using slider
    calories_hist_range = st.slider('Select Calories Range for Histogram', min_value=data['calories_kcal'].min(), max_value=data['calories_kcal'].max(), value=(data['calories_kcal'].min(), data['calories_kcal'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_hist = sorted(data['quality'].unique())
    selected_quality_hist = st.multiselect('Select Quality for Histogram', quality_values_hist, default=quality_values_hist)

    # Filter the DataFrame for Histogram
    filtered_df_hist = data[(data['calories_kcal'] >= calories_hist_range[0]) & (data['calories_kcal'] <= calories_hist_range[1]) & (data['quality'].isin(selected_quality_hist))]

    hist_chart = alt.Chart(filtered_df_hist).mark_bar().encode(
        alt.X('calories_kcal', bin=True),
        y='count()',
        color='quality:N',
        tooltip=['calories_kcal', 'count()', 'quality:N']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(hist_chart)



    # Visualization 4: Box Plot
    st.subheader('Box Plot - Carbs')

    # Add an interactive filter for Carbs range using slider
    carb_box_range = st.slider('Select Carbs Range for Box Plot', min_value=data['carb_g'].min(), max_value=data['carb_g'].max(), value=(data['carb_g'].min(), data['carb_g'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_box = sorted(data['quality'].unique())
    selected_quality_box = st.multiselect('Select Quality for Box Plot - Carbs', quality_values_box, default=quality_values_box)

    # Filter the DataFrame for Box Plot
    filtered_df_box = data[(data['carb_g'] >= carb_box_range[0]) & (data['carb_g'] <= carb_box_range[1]) & (data['quality'].isin(selected_quality_box))]

    box_chart = alt.Chart(filtered_df_box).mark_boxplot().encode(
        x='quality:N',
        y='carb_g:Q',
        color='quality:N',
        tooltip=['quality:N', 'carb_g:Q']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(box_chart)


    # Visualization 5: Bar Chart - Sugar
    st.subheader('Bar Chart - Distribution of Sugar by Quality')

    # Add an interactive filter for Sugar range using slider
    sugar_bar_range = st.slider('Select Sugar Range for Bar Chart', min_value=data['sugar_g'].min(), max_value=data['sugar_g'].max(), value=(data['sugar_g'].min(), data['sugar_g'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_sugar = sorted(data['quality'].unique())
    selected_quality_sugar = st.multiselect('Select Quality for Bar Chart - Sugar', quality_values_sugar, default=quality_values_sugar)

    # Filter the DataFrame for Bar Chart
    filtered_df_bar_sugar = data[(data['sugar_g'] >= sugar_bar_range[0]) & (data['sugar_g'] <= sugar_bar_range[1]) & (data['quality'].isin(selected_quality_sugar))]

    # Create the Bar Chart for distribution of Quality by Sugar Filter and Quality Filter
    bar_chart_sugar_distribution = alt.Chart(
        filtered_df_bar_sugar.groupby('quality').size().reset_index(name='count')
    ).mark_bar().encode(
        x='quality:N',
        y='count:Q',
        color='quality:N',
        tooltip=['quality:N', 'count:Q']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(bar_chart_sugar_distribution)

    


    # Visualization 6: Line Chart - Vitamins A vs. C
    st.subheader('Line Chart - Vitamins A vs. C')

    # Add an interactive filter for Vitamin A range
    vitamin_a_range_line_chart = st.slider('Select Vitamin A Range for Line Chart - Vitamins A vs. C', min_value=data['vitA_g'].min(), max_value=data['vitA_g'].max(), value=(data['vitA_g'].min(), data['vitA_g'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_line_chart = sorted(data['quality'].unique())
    selected_quality_line_chart = st.multiselect('Select Quality for Line Chart - Vitamins A vs. C', quality_values_line_chart, default=quality_values_line_chart)

    # Filter the DataFrame based on the selected Vitamin A range and Quality
    filtered_df_vitamins_ac_line_chart = data[(data['vitA_g'] >= vitamin_a_range_line_chart[0]) & (data['vitA_g'] <= vitamin_a_range_line_chart[1]) & (data['quality'].isin(selected_quality_line_chart))]

    # Create the Line Chart
    line_chart_vitamins_ac = alt.Chart(filtered_df_vitamins_ac_line_chart).mark_line().encode(
        x='vitA_g',
        y='vitC_mg',
        color='quality',
        tooltip=['vitA_g', 'vitC_mg', 'quality']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(line_chart_vitamins_ac)

   



def create_dashboard_2():
    # Dashboard 2
    st.subheader('Dashboard 2 - Visualizations')

    # Visualization 7: Bar Chart - Quality Distribution
    quality_count_filter = st.slider('Select Quality Count Range for Bar Chart', min_value=0, max_value=240, value=(0, 240))

    # Add an interactive filter for Quality using multiselect
    quality_values_bar_chart = sorted(data['quality'].unique())
    selected_quality_bar_chart = st.multiselect('Select Quality for Bar Chart - Quality Distribution', quality_values_bar_chart, default=quality_values_bar_chart)

    # Filter the DataFrame based on the selected quality count range and Quality
    filtered_df_quality_count = data['quality'].value_counts().reset_index()
    filtered_df_quality_count.columns = ['quality', 'count']
    filtered_df_quality_count = filtered_df_quality_count[(filtered_df_quality_count['count'] >= quality_count_filter[0]) & (filtered_df_quality_count['count'] <= quality_count_filter[1]) & (filtered_df_quality_count['quality'].isin(selected_quality_bar_chart))]

    # Create the bar chart
    bar_chart_quality = alt.Chart(filtered_df_quality_count).mark_bar().encode(
        x='quality:N',
        y='count:Q',
        color='quality:N',
        tooltip=['quality:N', 'count:Q']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(bar_chart_quality)


   # Visualization 8: Bar Chart - Average Calcium by Quality
    st.subheader('Bar Chart - Average Calcium by Quality')

    # Add an interactive filter for calcium range
    calcium_range = st.slider('Select Calcium Range for Bar Chart', min_value=data['calcium_mg'].min(), max_value=data['calcium_mg'].max(), value=(data['calcium_mg'].min(), data['calcium_mg'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_calcium = sorted(data['quality'].unique())
    selected_quality_calcium = st.multiselect('Select Quality for Bar Chart - Average Calcium by Quality', quality_values_calcium, default=quality_values_calcium)

    # Filter the DataFrame based on the selected calcium range and Quality
    filtered_df_calcium = data[(data['calcium_mg'] >= calcium_range[0]) & (data['calcium_mg'] <= calcium_range[1]) & (data['quality'].isin(selected_quality_calcium))]

    avg_calcium_chart = alt.Chart(
        filtered_df_calcium.groupby('quality')['calcium_mg'].mean().reset_index()
    ).mark_bar().encode(
        x='quality:N',
        y='calcium_mg:Q',
        color='quality:N',
        tooltip=['quality', 'calcium_mg']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(avg_calcium_chart)

   
    
   # Visualization 9: Bar Chart - Protein Distribution by Quality
    st.subheader('Bar Chart - Protein Distribution by Quality')

    # Add interactive filter for Protein range
    protein_range = st.slider('Select Protein Range for Bar Chart', min_value=data['protein_g'].min(), max_value=data['protein_g'].max(), value=(data['protein_g'].min(), data['protein_g'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_protein = sorted(data['quality'].unique())
    selected_quality_protein = st.multiselect('Select Quality for Bar Chart - Protein Distribution', quality_values_protein, default=quality_values_protein)

    # Filter the DataFrame for Bar Chart - Protein Distribution
    filtered_df_protein = data[
        (data['protein_g'] >= protein_range[0]) & (data['protein_g'] <= protein_range[1]) &
        (data['quality'].isin(selected_quality_protein))
    ]

    # Create bar chart for Protein Distribution using Altair
    protein_chart = alt.Chart(filtered_df_protein).mark_bar().encode(
        x=alt.X('quality:N', title='Quality'),
        y=alt.Y('mean(protein_g):Q', title='Mean Protein (g)'),
        color='quality:N',
        tooltip=['quality:N', alt.Tooltip('mean(protein_g):Q', title='Mean Protein (g)')]
    ).properties(
        width=600,
        height=400
    )

    # Display the Altair chart
    st.altair_chart(protein_chart)


  # Visualization 10: Bar Chart - Zinc Distribution by Quality
    st.subheader('Bar Chart - Zinc Distribution by Quality')

    # Add an interactive filter for Size range
    size_range_bar_chart_zinc = st.slider('Select Size Range for Bar Chart - Zinc Distribution', min_value=data['size'].min(), max_value=data['size'].max(), value=(data['size'].min(), data['size'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_bar_chart_zinc = sorted(data['quality'].unique())
    selected_quality_bar_chart_zinc = st.multiselect('Select Quality for Bar Chart - Zinc Distribution', quality_values_bar_chart_zinc, default=quality_values_bar_chart_zinc)

    # Filter the DataFrame for Bar Chart - Zinc Distribution by Quality
    filtered_df_bar_chart_zinc = data[
        (data['size'] >= size_range_bar_chart_zinc[0]) & (data['size'] <= size_range_bar_chart_zinc[1]) &
        (data['quality'].isin(selected_quality_bar_chart_zinc))
    ]

    bar_chart_zinc = alt.Chart(filtered_df_bar_chart_zinc).mark_bar().encode(
        x='quality:N',
        y='mean(zinc_mg):Q',
        color='quality:N',
        tooltip=['quality:N', 'mean(zinc_mg):Q']
    ).properties(
        width=400,
        height=400
    )

    # Display the Altair chart
    st.altair_chart(bar_chart_zinc)

  # Visualization 11: Histogram - Cholesterol 
    st.subheader('Histogram - Cholesterol')

    # Add an interactive filter for Cholesterol range
    cholesterol_range_hist_chart = st.slider('Select Cholesterol Range for Histogram', min_value=data['cholesterol_mg'].min(), max_value=data['cholesterol_mg'].max(), value=(data['cholesterol_mg'].min(), data['cholesterol_mg'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_hist_chart_cholesterol = sorted(data['quality'].unique())
    selected_quality_hist_chart_cholesterol = st.multiselect('Select Quality for Histogram - Cholesterol', quality_values_hist_chart_cholesterol, default=quality_values_hist_chart_cholesterol)

    # Filter the DataFrame for Histogram - Cholesterol with Quality Filter
    filtered_df_hist_chart_cholesterol = data[
        (data['cholesterol_mg'] >= cholesterol_range_hist_chart[0]) & (data['cholesterol_mg'] <= cholesterol_range_hist_chart[1]) &
        (data['quality'].isin(selected_quality_hist_chart_cholesterol))
    ]

    hist_chart_cholesterol = alt.Chart(filtered_df_hist_chart_cholesterol).mark_bar().encode(
        alt.X('cholesterol_mg', bin=True),
        y='count()',
        color='quality',
        tooltip=['cholesterol_mg', 'count()', 'quality']
    ).properties(
        width=400,
        height=400
    )

    # Display the Altair chart
    st.altair_chart(hist_chart_cholesterol)


    # Visualization 12: Bar Chart - Distribution of Fiber
    st.subheader('Bar Chart - Distribution of Fiber with Quality')

    # Add an interactive filter for Fiber range using slider
    fiber_range = st.slider('Select Fiber Range for Bar Chart', min_value=data['fiber_g'].min(), max_value=data['fiber_g'].max(), value=(data['fiber_g'].min(), data['fiber_g'].max()))

    # Add an interactive filter for Quality using multiselect
    quality_values_fiber = sorted(data['quality'].unique())
    selected_quality_distribution_fiber = st.multiselect('Select Quality for Bar Chart - Distribution of Fiber', quality_values_fiber, default=quality_values_fiber)

    # Filter the DataFrame for Bar Chart - Distribution of Fiber
    filtered_df_bar_chart_fiber = data[(data['fiber_g'] >= fiber_range[0]) & (data['fiber_g'] <= fiber_range[1]) & (data['quality'].isin(selected_quality_distribution_fiber))]

    # Create the Bar Chart for distribution of Fiber with Quality
    st.bar_chart(filtered_df_bar_chart_fiber.groupby('quality')['fiber_g'].sum())

# Main app
st.title("Food Data Analysis App")

# Create tabs using st.columns
tabs = st.columns(2)
selected_tab = tabs[0].radio("Select Dashboard", ["Dashboard 1", "Dashboard 2"])

# Display selected tab and visualizations
st.markdown("---")  # Adding a separator for better readability

# Display selected tab and visualizations
if selected_tab == "Dashboard 1":
    create_dashboard_1()
elif selected_tab == "Dashboard 2":
    create_dashboard_2()
