import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard_page():
    """render content of Dashboard page"""
    st.title("📈 Dashboard")
    st.markdown("---")

    # 1. read data
    # use @st.cache_data to cache the data to avoid slow
    @st.cache_data
    def load_data():
        file_path = "Note-Taking Application Selection (Responses) - Form responses 1.csv"
        df = pd.read_csv(file_path)
        return df

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("cant find CSV file，please make sure the file is at the same location.")
        return

    # -------------------------------------------------------
    # First Part：KPI Cards
    # -------------------------------------------------------
    st.subheader("📊 Key Indicators Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_respondents = len(df)
        st.metric(label="Total number of respondents", value=total_respondents)
    
    with col2:
        # Statistics on the most frequently used apps
        top_app = df['Which Note-Taking App are you currently using? '].mode()[0]
        # If multiple selections are made, only the primary one will be displayed, or a simple selection will be displayed.
        st.metric(label="Respondents' Favorite App", value=top_app.split(',')[0])

    with col3:
        # Statistics on the most which year of students
        top_year = df['Year of Study '].mode()[0]
        st.metric(label="Most Respondents from", value=top_year)

    st.markdown("---")

    # -------------------------------------------------------
    # Second part: Visualisation
    # -------------------------------------------------------
    
    # --- Row 1: Gender Distribution & Grade Distribution ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("### 🧑‍🤝‍🧑 Gender Distribution")
        # Data Cleanning：count gender
        gender_counts = df['What is your gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        
        # use Plotly to draw piechart
        fig_gender = px.pie(gender_counts, values='Count', names='Gender', 
                            color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_gender, use_container_width=True)

    with row1_col2:
        st.markdown("### 🎓 Grade Distribution (Sem/Year)")
        # Statistic on grade
        year_counts = df['Year of Study '].value_counts().reset_index()
        year_counts.columns = ['Year', 'Count']
        
        # use Plotly to draw bar chart
        fig_year = px.bar(year_counts, x='Year', y='Count', 
                          color='Count', 
                          color_continuous_scale='Viridis')
        st.plotly_chart(fig_year, use_container_width=True)

    # --- Row 2: devices & App preferences ---
    st.markdown("### 📱Device and App preferences")
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("**Device and App preferences**")
        device_counts = df['Primary Device used for Note-Taking '].value_counts().reset_index()
        device_counts.columns = ['Device', 'Count']
        
        fig_device = px.bar(device_counts, x='Count', y='Device', orientation='h',
                            text_auto=True)
        st.plotly_chart(fig_device, use_container_width=True)

    with row2_col2:
        st.markdown("**Top 5 Note-Taking Apps Using**")
        # Data cleanning: Handling multiple-choice answers (e.g., "GoodNotes, Notability")
        # 1. Discard empty values ​​-> 2. Convert to string -> 3. Split by commas -> 4. Explode into multiple lines
        all_apps = df['Which Note-Taking App are you currently using? '].dropna().astype(str).str.split(', ').explode()
        
        # Simple formatting cleanup (remove spaces, capitalize the first letter)
        all_apps = all_apps.str.strip().str.title()
        
        # Top five ranking
        app_counts = all_apps.value_counts().head(5).reset_index()
        app_counts.columns = ['App', 'Count']

        fig_app = px.bar(app_counts, x='App', y='Count', color='App')
        st.plotly_chart(fig_app, use_container_width=True)