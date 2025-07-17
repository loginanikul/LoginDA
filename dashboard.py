import pandas as pd
import streamlit as st
from googletrans import Translator
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
from audio_recorder_streamlit import audio_recorder
import base64
import os
from pathlib import Path
import requests
import urllib.request
import shutil
import time
from streamlit_chat import message
import json
import Third

print(Third.df.head())


# Dictionary of translations for UI elements
translations = {
    'English': {
        'title': 'My Simple Dashboard',
        'upload_text': 'Choose a CSV or Excel file',
        'success_msg': 'File successfully uploaded!',
        'data_table': 'Your Data Table',
        'sort_by': 'Sort by column:',
        'sort_order': 'Sort order:',
        'ascending': 'Ascending',
        'descending': 'Descending',
        'select_rows': 'Select number of rows to display',
        'search': 'Search in table:',
        'showing_rows': 'Showing {} rows out of {} total rows',
        'stats': 'Show Basic Statistics',
        'data_summary': 'Data Summary',
        'upload_prompt': 'Upload a file to view your data in table format!',
        'sample_data': 'Sample Data'
    },
    'हिंदी': {  # Hindi
        'title': 'मेरा सरल डैशबोर्ड',
        'upload_text': 'CSV या Excel फ़ाइल चुनें',
        'success_msg': 'फ़ाइल सफलतापूर्वक अपलोड की गई!',
        'data_table': 'आपका डेटा टेबल',
        'sort_by': 'कॉलम द्वारा क्रमबद्ध करें:',
        'sort_order': 'क्रम:',
        'ascending': 'आरोही',
        'descending': 'अवरोही',
        'select_rows': 'प्रदर्शित करने के लिए पंक्तियों की संख्या चुनें',
        'search': 'टेबल में खोजें:',
        'showing_rows': 'कुल {} पंक्तियों में से {} पंक्तियां दिखाई जा रही हैं',
        'stats': 'बुनियादी आंकड़े दिखाएं',
        'data_summary': 'डेटा सारांश',
        'upload_prompt': 'अपना डेटा देखने के लिए फ़ाइल अपलोड करें!',
        'sample_data': 'नमूना डेटा'
    },
    'मराठी': {  # Marathi
        'title': 'माझा साधा डॅशबोर्ड',
        'upload_text': 'CSV किंवा Excel फाईल निवडा',
        'success_msg': 'फाईल यशस्वीरित्या अपलोड केली!',
        'data_table': 'तुमचा डेटा टेबल',
        'sort_by': 'स्तंभानुसार क्रमवारी लावा:',
        'sort_order': 'क्रम:',
        'ascending': 'चढता',
        'descending': 'उतरता',
        'select_rows': 'प्रदर्शित करण्यासाठी ओळींची संख्या निवडा',
        'search': 'टेबलमध्ये शोधा:',
        'showing_rows': 'एकूण {} पैकी {} ओळी दाखवत आहे',
        'stats': 'मूलभूत आकडेवारी दाखवा',
        'data_summary': 'डेटा सारांश',
        'upload_prompt': 'तुमचा डेटा पाहण्यासाठी फाईल अपलोड करा!',
        'sample_data': 'नमुना डेटा'
    }
    # Add more languages as needed
}

# Set page config first
st.set_page_config(
    page_title="Interactive CSV/Excel Editor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for themes
st.markdown("""
<style>
    /* Light theme */
    .light-theme {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Dark theme */
    .dark-theme {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Custom theme */
    .custom-theme {
        background-color: var(--custom-bg);
        color: var(--custom-text);
    }
    
    /* Animated sidebar */
    .sidebar .sidebar-content {
        transition: all 0.3s ease-in-out;
    }
    
    /* Custom metric cards */
    .metric-card {
        transition: transform 0.3s ease-in-out;
    }
    .metric-card:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.title("⚙️ App Settings")
    
    # Theme selection
    st.subheader("Theme Settings")
    theme = st.selectbox(
        "Choose Theme",
        ["Light", "Dark", "Custom"],
        key="theme_select"
    )
    
    if theme == "Custom":
        custom_bg = st.color_picker("Background Color", "#ffffff")
        custom_text = st.color_picker("Text Color", "#000000")
        st.markdown(
            f"""
            <style>
            :root {{
                --custom-bg: {custom_bg};
                --custom-text: {custom_text};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    # Audio settings
    st.subheader("Audio Settings")
    enable_music = st.checkbox("Enable Background Music", value=True)
    volume = st.slider("Volume", 0.0, 1.0, 0.5)
    
    if enable_music:
        music_option = st.selectbox(
            "Select Background Music",
            ["Calm", "Upbeat", "Focus"],
            key="music_select"
        )
        
        # Add play/pause button
        if 'is_playing' not in st.session_state:
            st.session_state.is_playing = True
            
        if st.button("Play/Pause Music"):
            st.session_state.is_playing = not st.session_state.is_playing
    
    # Animation settings
    st.subheader("Animation Settings")
    enable_animations = st.checkbox("Enable Animations", value=True)
    
    # Accessibility settings
    st.subheader("Accessibility")
    font_size = st.select_slider(
        "Font Size",
        options=["Small", "Medium", "Large"],
        value="Medium"
    )
    
    high_contrast = st.checkbox("High Contrast Mode")

# Apply selected theme
if theme == "Dark":
    st.markdown("""
        <style>
        .main {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)
elif theme == "Light":
    st.markdown("""
        <style>
        .main {
            background-color: #ffffff;
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply font size
font_sizes = {
    "Small": "14px",
    "Medium": "16px",
    "Large": "18px"
}
st.markdown(f"""
    <style>
    .main {{
        font-size: {font_sizes[font_size]};
    }}
    </style>
""", unsafe_allow_html=True)

# Apply high contrast if enabled
if high_contrast:
    st.markdown("""
        <style>
        .main {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        a {
            color: #00ff00 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Main app title with animation
if enable_animations:
    st.markdown("""
        <style>
        .title-animation {
            animation: fadeIn 1.5s ease-in;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        </style>
        <h1 class='title-animation'>📊 Interactive Data Editor & Analyzer</h1>
    """, unsafe_allow_html=True)
else:
    st.title("📊 Interactive Data Editor & Analyzer")

# Add this function after imports, before the main code
def get_audio_base64(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode()
    except Exception as e:
        return None

# Add this before the setup_audio_files function
# Dictionary of audio files and their URLs
audio_files = {
    'calm.mp3': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
    'upbeat.mp3': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
    'focus.mp3': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'
}

# Audio samples information
AUDIO_SAMPLES = {
    "Calm": {
        'path': 'audio/calm.mp3',
        'description': 'Peaceful background music for relaxation'
    },
    "Upbeat": {
        'path': 'audio/upbeat.mp3',
        'description': 'Energetic music for productivity'
    },
    "Focus": {
        'path': 'audio/focus.mp3',
        'description': 'Concentration-enhancing background music'
    }
}

def download_with_retry(url, file_path, max_retries=3):
    """Download file with retry mechanism"""
    for attempt in range(max_retries):
        try:
            urllib.request.urlretrieve(url, file_path)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)
    return False

def setup_audio_files():
    """Download and setup sample audio files if they don't exist"""
    audio_dir = Path('audio')
    audio_dir.mkdir(exist_ok=True)
    
    with st.sidebar:
        with st.expander("📥 Audio System Status", expanded=False):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, (filename, url) in enumerate(audio_files.items()):
                file_path = audio_dir / filename
                if not file_path.exists():
                    try:
                        status_text.text(f"Downloading {filename}...")
                        download_with_retry(url, file_path)
                        status_text.success(f"✅ {filename}")
                    except Exception as e:
                        status_text.error(f"❌ {filename}: {str(e)}")
                else:
                    status_text.info(f"✅ {filename}")
                progress_bar.progress((i + 1) / len(audio_files))
            
            status_text.success("🎵 System Ready")
    return True

# Initialize audio setup in session state
if 'audio_setup_complete' not in st.session_state:
    st.session_state.audio_setup_complete = setup_audio_files()

# Update the AUDIO_SAMPLES dictionary with file info
AUDIO_SAMPLES = {
    "Calm": {
        'path': 'audio/calm.mp3',
        'description': 'Peaceful background music for relaxation'
    },
    "Upbeat": {
        'path': 'audio/upbeat.mp3',
        'description': 'Energetic music for productivity'
    },
    "Focus": {
        'path': 'audio/focus.mp3',
        'description': 'Concentration-enhancing background music'
    }
}

# Update the audio player section
if enable_music and st.session_state.is_playing:
    audio_placeholder = st.empty()
    
    # Get the selected audio file
    selected_audio = AUDIO_SAMPLES.get(music_option)
    
    if selected_audio and os.path.exists(selected_audio['path']):
        audio_base64 = get_audio_base64(selected_audio['path'])
        if audio_base64:
            st.write(f"🎵 Now playing: {music_option}")
            st.write(f"ℹ️ {selected_audio['description']}")
            audio_placeholder.markdown(f"""
                <audio autoplay loop>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
            
            # Add audio controls
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🔄 Change Track"):
                    st.session_state.is_playing = False
                   # st.experimental_rerun()
            with col2:
                st.slider("Volume", 0.0, 1.0, 0.5, key="volume_slider")
        else:
            st.warning("Unable to load audio file.")
    else:
        st.error("Audio file not found. Please wait for download to complete.")
        setup_audio_files()  # Try to download again

# Add a function to clean up downloaded files (optional)
def cleanup_audio():
    """Remove downloaded audio files"""
    try:
        shutil.rmtree('audio')
        st.success("Audio files cleaned up successfully!")
    except Exception as e:
        st.error(f"Error cleaning up audio files: {str(e)}")

# Add cleanup option in sidebar
with st.sidebar:
    if st.button("🗑️ Clean Up Audio Files"):
        cleanup_audio()

# Language selector
selected_language = st.sidebar.selectbox(
    "Select Language / भाषा चुनें / भाषा निवडा",
    options=list(translations.keys())
)

# Get translations for selected language
t = translations[selected_language]

# Add a title
st.title(t['title'])

# Add file uploader
st.subheader(t['upload_text'])
uploaded_file = st.file_uploader(t['upload_text'], type=['csv', 'xlsx', 'xls'])

# Initialize DataFrame
df = None

if uploaded_file is not None:
    try:
        # Check file type and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Display success message
        st.success(t['success_msg'])
        
        # Display the data in an editable format
        st.subheader(t['data_table'])
        
        # Add column management
        col1, col2 = st.columns([2, 1])
        with col1:
            # Add new column
            new_col_name = st.text_input("Add new column:", "")
            if st.button("Add Column") and new_col_name:
                if new_col_name not in df.columns:
                    df[new_col_name] = ""
                    st.success(f"Added column: {new_col_name}")
                else:
                    st.warning("Column already exists!")
        
        with col2:
            # Delete column
            col_to_delete = st.selectbox("Select column to delete:", [""] + list(df.columns))
            if st.button("Delete Column") and col_to_delete:
                df = df.drop(columns=[col_to_delete])
                st.success(f"Deleted column: {col_to_delete}")

        # Convert DataFrame to a format that can be edited
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
        )

        # Add download buttons
        st.subheader("Download Edited Data")
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as CSV
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="edited_data.csv",
                mime="text/csv",
                key='download-csv'
            )
        
        with col2:
            # Download as Excel - Fixed version
            # buffer = io.BytesIO()
            # with pd.ExcelWriter(buffer, engine='xlsxwriter', mode='w') as writer:
            #     edited_df.to_excel(writer, sheet_name='Sheet1', index=False)
            #     writer.close()  # Close the writer
            
            # excel_data = buffer.getvalue()
            # st.download_button(
            #     label="📥 Download as Excel",
            #     data=excel_data,
            #     file_name="edited_data.xlsx",
            #     mime="application/vnd.ms-excel",
            #     key='download-excel'
            # )

        # Show table info
        #st.info(f"Total rows: {len(edited_df)}, Total columns: {len(edited_df.columns)}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    # Show sample data if no file is uploaded
    st.info(t['upload_prompt'])
    
    # Show sample data
    sample_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Sales': [1200, 1500, 1300, 1800, 2100],
        'Expenses': [1000, 1300, 1100, 1400, 1800]
    }
    df = pd.DataFrame(sample_data)
    st.subheader(t['sample_data'])
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
    )

# Add visualization section after the data editor
if df is not None:
    st.header("Data Analysis & Visualizations")
    
    # Get numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Basic Stats", "Charts", "Correlation", "Distribution"])
    
    with tab1:
        st.subheader("Basic Statistics")
        if len(numeric_cols) > 0:
            # Create three columns for key metrics with custom CSS
            st.markdown("""
                <style>
                .metric-card {
                    background-color: #f0f2f6;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                }
                .metric-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0066cc;
                }
                .metric-label {
                    font-size: 16px;
                    color: #666;
                }
                </style>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df)}</div>
                        <div class="metric-label">Total Rows</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df.columns)}</div>
                        <div class="metric-label">Total Columns</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                missing = df.isna().sum().sum()
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{missing}</div>
                        <div class="metric-label">Missing Values</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                duplicates = df.duplicated().sum()
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{duplicates}</div>
                        <div class="metric-label">Duplicate Rows</div>
                    </div>
                """, unsafe_allow_html=True)

            # Add spacing
            st.markdown("<br>", unsafe_allow_html=True)

            # Numeric columns summary with better formatting
            st.subheader("Numeric Columns Summary")
            summary_stats = df[numeric_cols].describe()
            
            # Format the summary statistics
            formatted_stats = summary_stats.round(2)
            
            # Add custom styling to the dataframe
            st.markdown("""
                <style>
                .stats-table {
                    font-family: Arial, sans-serif;
                }
                .stats-table th {
                    background-color: #0066cc;
                    color: white;
                    font-weight: bold;
                    padding: 10px;
                }
                .stats-table td {
                    padding: 8px;
                }
                .stats-table tr:nth-child(even) {
                    background-color: #f5f5f5;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Display styled dataframe
            st.dataframe(
                formatted_stats,
                use_container_width=True,
                height=300
            )

            # Column-wise missing values
            st.subheader("Missing Values by Column")
            missing_values = df.isnull().sum().reset_index()
            missing_values.columns = ['Column', 'Missing Count']
            missing_values['Missing Percentage'] = (missing_values['Missing Count'] / len(df) * 100).round(2)
            
            # Only show columns with missing values
            missing_values = missing_values[missing_values['Missing Count'] > 0]
            
            if not missing_values.empty:
                fig = px.bar(
                    missing_values,
                    x='Column',
                    y='Missing Percentage',
                    title='Missing Values Distribution',
                    labels={'Missing Percentage': 'Missing Values (%)'},
                    color='Missing Percentage',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    xaxis_tickangle=-45,
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No missing values found in the dataset! 🎉")

            # Data Types Summary
            st.subheader("Column Data Types")
            dtypes = df.dtypes.reset_index()
            dtypes.columns = ['Column', 'Data Type']
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(dtypes, use_container_width=True)
            
            with col2:
                dtype_counts = df.dtypes.value_counts()
                fig = px.pie(
                    values=dtype_counts.values,
                    names=dtype_counts.index.astype(str),
                    title='Distribution of Data Types'
                )
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found in the dataset. Basic statistics are only available for numeric data.")
    
    with tab2:
        st.subheader("Data Visualization")
        
        # Add filtering options
        st.write("Filter Data")
        filter_col, filter_value = st.columns([1, 1])
        
        with filter_col:
            filter_column = st.selectbox(
                "Select column to filter",
                options=["None"] + list(df.columns)
            )
        
        # Create filtered dataframe
        filtered_df = df.copy()
        
        if filter_column != "None":
            with filter_value:
                if df[filter_column].dtype in ['int64', 'float64']:
                    # Numeric filter
                    min_val = float(df[filter_column].min())
                    max_val = float(df[filter_column].max())
                    filter_range = st.slider(
                        "Select range",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val)
                    )
                    filtered_df = filtered_df[
                        (filtered_df[filter_column] >= filter_range[0]) & 
                        (filtered_df[filter_column] <= filter_range[1])
                    ]
                else:
                    # Categorical filter
                    unique_values = ["All"] + list(df[filter_column].unique())
                    selected_value = st.selectbox(
                        "Select value",
                        options=unique_values
                    )
                    if selected_value != "All":
                        filtered_df = filtered_df[filtered_df[filter_column] == selected_value]
        
        # Show number of filtered rows
        st.write(f"Showing {len(filtered_df)} rows")
        
        # Chart type selector
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"]
        )
        
        if len(numeric_cols) > 0:
            if chart_type in ["Line Chart", "Bar Chart"]:
                selected_cols = st.multiselect(
                    "Select columns to visualize",
                    options=numeric_cols,
                    default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols[:1]
                )
                
                if selected_cols:
                    if chart_type == "Line Chart":
                        fig = px.line(filtered_df, y=selected_cols)
                    else:  # Bar Chart
                        fig = px.bar(filtered_df, y=selected_cols)
                    
                    # Update layout for better visibility
                    fig.update_layout(
                        height=500,
                        title=f"{chart_type} for {', '.join(selected_cols)}",
                        xaxis_title="Index",
                        yaxis_title="Value",
                        legend_title="Columns"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Scatter Plot" and len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    x_axis = st.selectbox("Select X-axis", numeric_cols)
                with col2:
                    y_axis = st.selectbox("Select Y-axis", numeric_cols)
                
                color_col = st.selectbox("Select color column (optional)", ["None"] + categorical_cols)
                
                if color_col == "None":
                    fig = px.scatter(filtered_df, x=x_axis, y=y_axis)
                else:
                    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color_col)
                
                # Update layout
                fig.update_layout(
                    height=500,
                    title=f"Scatter Plot: {x_axis} vs {y_axis}",
                    legend_title="Legend"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Pie Chart":
                if categorical_cols:
                    value_col = st.selectbox("Select value column", numeric_cols)
                    category_col = st.selectbox("Select category column", categorical_cols)
                    
                    # Aggregate data for pie chart
                    pie_data = filtered_df.groupby(category_col)[value_col].sum().reset_index()
                    fig = px.pie(
                        pie_data, 
                        values=value_col, 
                        names=category_col,
                        title=f"Pie Chart: {value_col} by {category_col}"
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Pie chart requires at least one categorical column")
    
    # with tab3:
    #     st.subheader("Correlation Analysis")
    #     # if len(numeric_cols) > 1:
    #     #     #correlation = df[numeric_cols].corr()
    #     #     fig = px.imshow(correlation,
    #     #                   labels=dict(color="Correlation"),
    #     #                   color_continuous_scale='RdBu_r')
    #     #     st.plotly_chart(fig, use_container_width=True)
            
    #         # Display correlation table
    #         st.dataframe(correlation.style.background_gradient(cmap='RdBu_r'))
    #     else:
    #         st.warning("Correlation analysis requires at least 2 numeric columns")
    
    with tab4:
        st.subheader("Distribution Analysis")
        if numeric_cols:
            selected_col = st.selectbox("Select column for distribution", numeric_cols)
            
            col1, col2 = st.columns(2)
            with col1:
                # Histogram
                fig_hist = px.histogram(df, x=selected_col, nbins=30)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Box plot
                fig_box = px.box(df, y=selected_col)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Basic statistics
            st.write("Basic Statistics:")
            stats = df[selected_col].describe()
            st.dataframe(stats)
        else:
            st.warning("Distribution analysis requires numeric columns")

# Add some fun interactive elements
if st.checkbox("Show Fun Controls"):
    st.write("Fun Controls")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎨 Random Color Theme"):
            import random
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            st.markdown(f"""
                <style>
                .main {{
                    background-color: rgb({r},{g},{b});
                    color: {'#ffffff' if (r+g+b)/3 < 128 else '#000000'};
                }}
                </style>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🎲 Surprise Me"):
            import random
            effects = ["bounce", "shake", "spin", "flip"]
            effect = random.choice(effects)
            st.markdown(f"""
                <style>
                .element {{
                    animation: {effect} 1s ease-in-out;
                }}
                </style>
            """, unsafe_allow_html=True)

def create_chat_interface():
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'df_info' not in st.session_state:
        st.session_state.df_info = None

    # Initialize user input if not in session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    st.markdown("""
        <style>
        .chat-container {
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid var(--primary-color);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }
        .user-message {
            background: rgba(0, 255, 136, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .bot-message {
            background: rgba(0, 102, 255, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .stTextInput input {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--primary-color);
            color: white;
            border-radius: 25px;
        }
        .stTextInput input:focus {
            box-shadow: 0 0 10px var(--primary-color);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 💬 Data Assistant")
    
    # Create chat container
    chat_container = st.container()
    
    # Create input container
    input_container = st.container()

    def clear_input():
        st.session_state.user_input = ""
    
    with input_container:
        # Create two columns for input and button
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me about your data:", 
                key="user_input",
                placeholder="e.g., Show me basic statistics",
                on_change=clear_input if st.session_state.user_input else None
            )
        
        with col2:
            send_button = st.button("Send 📤")
    
    if send_button and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(("user", user_input))
        
        # Generate response based on the data and user input
        response = generate_data_response(user_input)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append(("assistant", response))
    
    # Display chat history
    with chat_container:
        for i, (role, content) in enumerate(reversed(st.session_state.chat_history)):
            if role == "user":
                message(content, is_user=True, key=f"user_{i}")
            else:
                message(content, is_user=False, key=f"assistant_{i}")

    # Show initial help message if chat is empty
    if not st.session_state.chat_history:
        st.info("👋 Hi! I'm your data assistant. Type 'help' to see what I can do!")

def generate_data_response(user_input):
    """Generate response based on user input and current dataframe"""
    try:
        if 'df' not in locals() and 'df' not in globals():
            return "Please upload a file first to analyze it."
        
        # Convert user input to lowercase for easier matching
        query = user_input.lower()
        
        # Basic statistics request
        if any(word in query for word in ['statistics', 'stats', 'summary']):
            numeric_df = df.select_dtypes(include=['float64', 'int64'])
            if numeric_df.empty:
                return "No numeric columns found in the dataset."
            stats = numeric_df.describe().round(2).to_string()
            return f"📊 Here are the basic statistics:\n{stats}"
        
        # Column information request
        elif any(word in query for word in ['columns', 'fields']):
            cols = "\n".join([f"- {col}" for col in df.columns])
            return f"📋 The dataset contains these columns:\n{cols}"
        
        # Missing values information
        elif 'missing' in query:
            missing = df.isnull().sum()
            missing = missing[missing > 0].to_string()
            if not missing:
                return "✨ Great news! No missing values found in the dataset."
            return f"🔍 Here's the missing values count per column:\n{missing}"
        
        # Shape of the dataset
        elif any(word in query for word in ['shape', 'size', 'dimensions']):
            rows, cols = df.shape
            return f"📏 The dataset has {rows:,} rows and {cols} columns."
        
        # Data types information
        elif 'types' in query:
            dtypes = "\n".join([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()])
            return f"🏷️ Here are the data types of each column:\n{dtypes}"
        
        # Sample data request
        elif 'sample' in query:
            sample = df.head().to_string()
            return f"📎 Here's a sample of the first 5 rows:\n{sample}"
        
        # Unique values count
        elif 'unique' in query:
            unique_counts = {col: df[col].nunique() for col in df.columns}
            unique_info = "\n".join([f"- {col}: {count:,} unique values" for col, count in unique_counts.items()])
            return f"🔄 Unique values per column:\n{unique_info}"
        
        # Help message
        elif 'help' in query:
            return """🤖 I can help you analyze your data! Try asking me about:
            
            📊 Basic statistics
            📋 Column information
            🔍 Missing values
            📏 Dataset shape
            🏷️ Data types
            📎 Sample data
            🔄 Unique values
            
            Just ask in natural language!"""
        
        # Default response
        else:
            return "❓ I'm not sure how to help with that. Type 'help' to see what I can do!"
    
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# Add this to your main interface where you want the chat to appear
st.markdown("---")
create_chat_interface() 