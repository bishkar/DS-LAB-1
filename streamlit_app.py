"""
Streamlit Dashboard for MLDS Week 1 - Data Collection and Processing
Visualizes results from all tasks including web scraping, API data, and weather analysis.
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

# Page configuration
st.set_page_config(
    page_title="MLDS Week 1 Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-header {
        font-size: 2rem;
        color: #2ca02c;
        border-bottom: 2px solid #2ca02c;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def load_json_safe(filepath: str):
    """Safely load JSON file with error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def load_csv_safe(filepath: str):
    """Safely load CSV file with error handling."""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return None
    except Exception:
        return None


def task1_web_scraping():
    """Display Task 1 - Web Scraping results."""
    st.markdown('<div class="task-header">📰 Task 1: Web Scraping</div>', unsafe_allow_html=True)
    
    data = load_json_safe('extracted_wikipedia_data.json')
    
    if data:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Status", "✅ Completed")
            st.metric("Data Source", "Wikipedia")
        
        with col2:
            st.subheader("Extracted Data")
            st.info(f"**Title:** {data.get('title', 'N/A')}")
            st.write(f"**First Sentence:** {data.get('first_sentence', 'N/A')}")
        
        # Show raw JSON
        with st.expander("View Raw JSON Data"):
            st.json(data)
    else:
        st.warning("⚠️ No data found. Run `python src/task1_scrape.py` to generate results.")


def task2_api_data():
    """Display Task 2 - API Data Collection results."""
    st.markdown('<div class="task-header">🌐 Task 2: API Data Collection</div>', unsafe_allow_html=True)
    
    data = load_json_safe('tokyo_weather.json')
    
    if data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", "✅ Completed")
        
        with col2:
            st.metric("Date", data.get('date', 'N/A'))
        
        with col3:
            temp = data.get('max_temperature', 0)
            st.metric("Max Temperature", f"{temp}°C", delta=None)
        
        # Temperature gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=temp,
            title={'text': "Maximum Temperature (°C)"},
            delta={'reference': 30, 'suffix': "°C from threshold"},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 20], 'color': "lightblue"},
                    {'range': [20, 30], 'color': "lightyellow"},
                    {'range': [30, 50], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Raw JSON Data"):
            st.json(data)
    else:
        st.warning("⚠️ No data found. Run `python src/task2_fetch_tokyo_weather.py` to generate results.")


def task3_weather_analysis():
    """Display Task 3 - Complex Weather Analysis results."""
    st.markdown('<div class="task-header">🌦️ Task 3: Complex Weather Analysis</div>', unsafe_allow_html=True)
    
    data = load_json_safe('src/tokyo_weather_complex.json')
    
    if data and 'daily' in data:
        daily_data = data['daily']
        df = pd.DataFrame(daily_data)
        
        # City information
        st.subheader(f"📍 {data.get('city', 'Tokyo')}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latitude", data.get('latitude', 'N/A'))
        with col2:
            st.metric("Longitude", data.get('longitude', 'N/A'))
        with col3:
            st.metric("Timezone", data.get('timezone', 'N/A'))
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Max Temp", f"{df['max_temperature'].mean():.1f}°C")
        with col2:
            st.metric("Avg Min Temp", f"{df['min_temperature'].mean():.1f}°C")
        with col3:
            st.metric("Total Precipitation", f"{df['precipitation'].sum():.1f}mm")
        with col4:
            st.metric("Avg Humidity", f"{df['humidity'].mean():.0f}%")
        
        # Temperature chart
        st.subheader("🌡️ Temperature Trends")
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=df['date'], y=df['max_temperature'],
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='red', width=2)
        ))
        fig_temp.add_trace(go.Scatter(
            x=df['date'], y=df['min_temperature'],
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='blue', width=2)
        ))
        fig_temp.update_layout(
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Multi-metric analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💨 Wind Speed")
            fig_wind = px.bar(df, x='date', y='wind_speed', 
                             color='wind_speed',
                             color_continuous_scale='Blues')
            fig_wind.update_layout(showlegend=False)
            st.plotly_chart(fig_wind, use_container_width=True)
        
        with col2:
            st.subheader("💧 Precipitation")
            fig_precip = px.bar(df, x='date', y='precipitation',
                               color='precipitation',
                               color_continuous_scale='Blues')
            fig_precip.update_layout(showlegend=False)
            st.plotly_chart(fig_precip, use_container_width=True)
        
        # Weather conditions breakdown
        st.subheader("🌤️ Weather Conditions")
        hot_days = (df['max_temperature'] > 30).sum()
        windy_days = (df['wind_speed'] > 15).sum()
        rainy_days = (df['precipitation'] > 0).sum()
        humid_days = (df['humidity'] > 70).sum()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Hot Days (>30°C)", hot_days)
        with col2:
            st.metric("Windy Days (>15km/h)", windy_days)
        with col3:
            st.metric("Rainy Days", rainy_days)
        with col4:
            st.metric("Humid Days (>70%)", humid_days)
        
        # Detailed data table
        with st.expander("📋 View Detailed Weather Data"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No complex weather data found. Check `src/tokyo_weather_complex.json`.")


def task4_csv_export():
    """Display Task 4 - CSV Export results."""
    st.markdown('<div class="task-header">📁 Task 4: Weather Data Export</div>', unsafe_allow_html=True)
    
    df = load_csv_safe('tokyo_weather_summary.csv')
    
    if df is not None:
        st.success(f"✅ Successfully loaded CSV with {len(df)} records")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            if 'Is Hot Day' in df.columns:
                hot_count = df['Is Hot Day'].sum() if df['Is Hot Day'].dtype == bool else (df['Is Hot Day'] == 'True').sum()
                st.metric("Hot Days", hot_count)
        with col3:
            if 'Is Rainy Day' in df.columns:
                rainy_count = df['Is Rainy Day'].sum() if df['Is Rainy Day'].dtype == bool else (df['Is Rainy Day'] == 'True').sum()
                st.metric("Rainy Days", rainy_count)
        
        # Display table
        st.subheader("📊 Exported Data Preview")
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f'tokyo_weather_summary_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )
    else:
        st.warning("⚠️ No CSV data found. Run `python src/task4_weather_summary_export.py` to generate results.")


def task5_xml_parsing():
    """Display Task 5 - XML Parsing results."""
    st.markdown('<div class="task-header">📄 Task 5: XML Parsing</div>', unsafe_allow_html=True)
    
    df = load_csv_safe('parsed_weather_data.csv')
    
    if df is not None:
        st.success(f"✅ Successfully parsed XML data: {len(df)} records")
        
        # Temperature distribution
        fig = px.histogram(df, x='Temperature', nbins=20,
                          title='Temperature Distribution',
                          labels={'Temperature': 'Temperature (°C)', 'count': 'Frequency'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Humidity vs Precipitation scatter
        fig2 = px.scatter(df, x='Humidity', y='Precipitation',
                         size='Temperature', color='Temperature',
                         title='Humidity vs Precipitation',
                         labels={'Humidity': 'Humidity (%)', 'Precipitation': 'Precipitation (mm)'})
        st.plotly_chart(fig2, use_container_width=True)
        
        # Data table
        with st.expander("📋 View Parsed XML Data"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No parsed XML data found. Run `python src/task5_parse_weather_xml.py` to generate results.")


def task6_regex_extraction():
    """Display Task 6 - Regex Extraction results."""
    st.markdown('<div class="task-header">🔍 Task 6: Regex Data Extraction</div>', unsafe_allow_html=True)
    
    df = load_csv_safe('extracted_weather_data.csv')
    
    if df is not None:
        st.success(f"✅ Successfully extracted {len(df)} records using regex")
        
        # Temperature range analysis
        if 'Max Temperature' in df.columns and 'Min Temperature' in df.columns:
            df['Temperature Range'] = df['Max Temperature'] - df['Min Temperature']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(df, x='Date', y=['Max Temperature', 'Min Temperature'],
                            title='Temperature Range Over Time',
                            labels={'value': 'Temperature (°C)', 'variable': 'Type'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig2 = px.bar(df, x='Date', y='Temperature Range',
                             title='Daily Temperature Swing',
                             labels={'Temperature Range': 'Temperature Swing (°C)'})
                st.plotly_chart(fig2, use_container_width=True)
        
        # Statistics
        st.subheader("📊 Extraction Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'Max Temperature' in df.columns:
                st.metric("Avg Max Temp", f"{df['Max Temperature'].mean():.1f}°C")
        with col2:
            if 'Min Temperature' in df.columns:
                st.metric("Avg Min Temp", f"{df['Min Temperature'].mean():.1f}°C")
        with col3:
            if 'Humidity' in df.columns:
                st.metric("Avg Humidity", f"{df['Humidity'].mean():.0f}%")
        with col4:
            if 'Precipitation' in df.columns:
                st.metric("Total Precipitation", f"{df['Precipitation'].sum():.1f}mm")
        
        # Data table
        with st.expander("📋 View Extracted Data"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No extracted data found. Run `python src/task6_extract_weather_data.py` to generate results.")


def main():
    """Main application."""
    st.markdown('<div class="main-header">📊 MLDS Week 1 Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Data Collection and Processing - Results Visualization")
    
    # Sidebar
    st.sidebar.title("🔧 Navigation")
    st.sidebar.markdown("---")
    
    tasks = {
        "Overview": "📊 All Tasks Overview",
        "Task 1": "📰 Web Scraping",
        "Task 2": "🌐 API Data Collection",
        "Task 3": "🌦️ Weather Analysis",
        "Task 4": "📁 CSV Export",
        "Task 5": "📄 XML Parsing",
        "Task 6": "🔍 Regex Extraction"
    }
    
    selected_task = st.sidebar.radio("Select Task", list(tasks.keys()), format_func=lambda x: tasks[x])
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Instructions:**
    1. Run the task scripts to generate data
    2. Select a task from the menu
    3. View visualizations and analysis
    """)
    
    # Display selected task
    if selected_task == "Overview":
        st.info("👈 Select a task from the sidebar to view detailed results")
        
        # Quick status check
        st.subheader("📋 Task Completion Status")
        
        status_data = {
            "Task": ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5", "Task 6"],
            "Description": [
                "Web Scraping",
                "API Data Collection",
                "Weather Analysis",
                "CSV Export",
                "XML Parsing",
                "Regex Extraction"
            ],
            "Status": [
                "✅" if load_json_safe('extracted_wikipedia_data.json') else "⏳",
                "✅" if load_json_safe('tokyo_weather.json') else "⏳",
                "✅" if load_json_safe('src/tokyo_weather_complex.json') else "⏳",
                "✅" if load_csv_safe('tokyo_weather_summary.csv') is not None else "⏳",
                "✅" if load_csv_safe('parsed_weather_data.csv') is not None else "⏳",
                "✅" if load_csv_safe('extracted_weather_data.csv') is not None else "⏳"
            ]
        }
        
        st.table(pd.DataFrame(status_data))
        
    elif selected_task == "Task 1":
        task1_web_scraping()
    elif selected_task == "Task 2":
        task2_api_data()
    elif selected_task == "Task 3":
        task3_weather_analysis()
    elif selected_task == "Task 4":
        task4_csv_export()
    elif selected_task == "Task 5":
        task5_xml_parsing()
    elif selected_task == "Task 6":
        task6_regex_extraction()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**MLDS Week 1** © 2025")


if __name__ == "__main__":
    main()
