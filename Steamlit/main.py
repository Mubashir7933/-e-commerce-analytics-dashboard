# Step 1: Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.express as px

# Step 2: Set Page Configuration for Layout, Title, and Icon
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="📊")

# Step 3: Load Dataset
data = pd.read_excel('Enhanced_ECommerce_Dataset.xlsx', sheet_name='Sheet1')

# Step 4: Preprocessing - Convert 'Order Date' to datetime format
data['Order Date'] = pd.to_datetime(data['Order Date'])

# Sidebar for Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", ("Dashboard", "Forecasting"))

# Sidebar Filters
st.sidebar.header('Filters')
selected_month = st.sidebar.multiselect('Select Month-Year', data['Month-Year'].unique())
selected_category = st.sidebar.multiselect('Select Category', data['Category'].unique())
selected_city = st.sidebar.multiselect('Select City', data['City'].unique())

# Apply Filters
filtered_data = data.copy()
if selected_month:
    filtered_data = filtered_data[filtered_data['Month-Year'].isin(selected_month)]
if selected_category:
    filtered_data = filtered_data[filtered_data['Category'].isin(selected_category)]
if selected_city:
    filtered_data = filtered_data[filtered_data['City'].isin(selected_city)]

# Main Title
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📊 E-Commerce Analytics Dashboard</h1>", unsafe_allow_html=True)

# Description
st.markdown("""
    This dashboard provides an overview of the sales performance, product trends, and regional insights.
    You can filter the data by **Month**, **Product Category**, and **City** to tailor the analysis to your needs.
    It also includes **Sales Forecasting** for better business decision-making.
""")

# Dashboard Page
if option == "Dashboard":
    st.subheader('Key Performance Indicators (KPIs)')
    col1, col2, col3 = st.columns(3)
    with col1:
        total_sales = filtered_data['Amount'].sum()
        st.metric('Total Sales', f"${total_sales:,.2f}")
    with col2:
        total_profit = filtered_data['Profit'].sum()
        st.metric('Total Profit', f"${total_profit:,.2f}")
    with col3:
        total_orders = filtered_data['Total Orders'].sum()
        avg_order_value = total_sales / total_orders if total_orders != 0 else 0
        st.metric('Average Order Value', f"${avg_order_value:,.2f}")

    st.subheader('📈 Monthly Sales Trend')
    monthly_sales = filtered_data.groupby('Month-Year')['Amount'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_sales.plot(kind='line', marker='o', ax=ax, color='royalblue', linewidth=2.5)
    ax.set_title('Monthly Sales Trend', fontsize=16)
    ax.set_xlabel('Month-Year', fontsize=12)
    ax.set_ylabel('Sales Amount ($)', fontsize=12)
    ax.grid(True)
    st.pyplot(fig)

    st.subheader('🏆 Top Selling Categories')
    top_categories = filtered_data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    top_categories.plot(kind='bar', color='skyblue', ax=ax2)
    ax2.set_title('Top Selling Categories', fontsize=16)
    ax2.set_xlabel('Category', fontsize=12)
    ax2.set_ylabel('Sales Amount ($)', fontsize=12)
    ax2.grid(True)
    st.pyplot(fig2)

    st.subheader('🏙️ Top 10 Cities by Sales')
    top_cities = filtered_data.groupby('City')['Amount'].sum().sort_values(ascending=False).head(10)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    top_cities.plot(kind='bar', color='coral', ax=ax3)
    ax3.set_title('Top 10 Cities by Sales', fontsize=16)
    ax3.set_xlabel('City', fontsize=12)
    ax3.set_ylabel('Sales Amount ($)', fontsize=12)
    ax3.grid(True)
    st.pyplot(fig3)

    st.subheader('📋 Filtered Data Preview')
    st.dataframe(filtered_data)

    st.download_button(
        label="Download Filtered Data as CSV",
        data=filtered_data.to_csv(index=False),
        file_name='filtered_ecommerce_data.csv',
        mime='text/csv'
    )

# Forecasting Page
elif option == "Forecasting":
    st.subheader('📈 Sales Forecasting')

    forecast_data = filtered_data.groupby('Order Date')['Amount'].sum().resample('M').sum()

    if len(forecast_data) < 2:
        st.warning("Not enough data to generate a forecast. Need at least 2 data points.")
    else:
        model = ExponentialSmoothing(forecast_data, trend='add', seasonal=None)
        fit_model = model.fit()
        forecast = fit_model.forecast(3)

        fig4, ax4 = plt.subplots(figsize=(10, 6))
        forecast_data.plot(label='Actual Sales', marker='o', ax=ax4)
        forecast.plot(label='Forecasted Sales', marker='x', ax=ax4, color='red')
        ax4.set_title('Sales Forecast for Next 3 Months', fontsize=16)
        ax4.set_xlabel('Month', fontsize=12)
        ax4.set_ylabel('Sales Amount ($)', fontsize=12)
        ax4.legend()
        ax4.grid(True)
        st.pyplot(fig4)

        st.write("### Forecasted Sales for Next 3 Months:")
        st.dataframe(forecast.reset_index().rename(columns={0: 'Forecasted Sales'}))

# Footer
st.markdown("""
    <footer style="text-align: center; font-size: 12px; color: grey;">
        Built by Your Syed Mubashir Ahmed - E-Commerce Dashboard Project | Contact: 21051350129
    </footer>
""", unsafe_allow_html=True)
