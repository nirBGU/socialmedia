import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Social Media Usage Analysis",
    page_icon="📱",
    layout="wide"
)

###################
# Custom Styling
###################
def load_css():
    st.markdown("""
        <style>
        .hero {
            padding: 2rem;
            background: linear-gradient(to right, #1f2937, #374151);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .hero-title {
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            color: #e5e7eb;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #1f2937;
        }
        .stat-label {
            font-size: 1rem;
            color: #6b7280;
        }

        /* 🔽 הוספה שמצמצמת רווח בין עמודות */
        .block-container {
            padding: 0 1rem;
        }
        .element-container:has(.stColumn) {
            gap: 0.5rem !important;  /* אפשר להקטין ל-0.3rem אם עדיין רחב מדי */
        }
        </style>
    """, unsafe_allow_html=True)

def add_custom_css():
    st.markdown("""
        <style>
        /* Make the Filter by Category dropdown more compact */
        div[data-testid="stSelectbox"] > div > div > div {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            min-height: 0px !important;
        }
        
        /* Reduce padding around the selectbox label */
        div[data-testid="stSelectbox"] label {
            padding-bottom: 0px !important;
            margin-bottom: 0px !important;
            font-size: 0.9rem !important;
        }
        </style>
    """, unsafe_allow_html=True)


def add_title_with_spacing(title_text):
    """
    Creates a title with proper spacing to prevent cutoff issues
    """
    # Add space above title to prevent cutoff
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    # Add the title
    st.title(title_text)
    # Add a small space below the title
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)


# Define regular and colorblind color palettes
def get_color_palette(colorblind_mode=False):
    if colorblind_mode:
        # Colorblind-friendly palettes
        platform_colors = {
            'Facebook': '#0072B2',  # Blue
            'Instagram': '#CC79A7',  # Pink
            'Twitter': '#56B4E9',    # Light blue
            'TikTok': '#000000',     # Black
            'YouTube': '#D55E00'     # Orange-red
        }
        
        device_colors = {
            'Smartphone': '#D55E00',  # Orange-red
            'PC': '#009E73',          # Green
            'Tablet': '#F0E442'       # Yellow
        }
        
        goal_colors = {
            'Education': '#0072B2',   # Blue
            'Entertainment': '#E69F00', # Orange
            'Networking': '#009E73',    # Green
            'News': '#CC79A7'           # Pink
        }
    else:
        # Original color palettes
        platform_colors = {
            'Facebook': '#4267B2',
            'Instagram': '#bc2a8d',
            'Twitter': '#1DA1F2',
            'TikTok': '#000000',
            'YouTube': '#FF0000'
        }
        
        device_colors = {
            'Smartphone': '#FF6B6B',
            'PC': '#4ECDC4',
            'Tablet': '#FFD93D'
        }
        
        goal_colors = {
            'Education': '#4267B2',
            'Entertainment': '#f39c12',
            'Networking': '#2ecc71',
            'News': '#E1306C'
        }
    
    return platform_colors, device_colors, goal_colors



###################################

def add_question_help_icon(question_number, title_text, explanation_text):
    """
    Adds a title with a help icon for each question section.
    
    Parameters:
    - question_number: The number of the question (1, 2, or 3)
    - title_text: The title of the section
    - explanation_text: The text to display in the explanation popup
    """
    # Create a container for the title section
    title_container = st.container()
    
    # Create columns for the title and help icon
    col1, col2 = title_container.columns([0.98, 0.02])
    
    with col1:
        st.title(title_text)
        
    with col2:
        # Add some spacing to align with the title
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        help_expander = st.expander("?")
        with help_expander:
            st.markdown(explanation_text)
    
    # Add a small space after the title section
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

###################
# Data Loading
###################
@st.cache_data
def load_data():
    df = pd.read_csv('finalsocial.csv')
    # Create income groups
    df['Income_Group'] = pd.cut(
        df['Monthly Income (USD)'],
        bins=[500, 1500, 2500, 3500, 4500, 5500, 6500, 7500, float('inf')],
        labels=['500-1500', '1500-2500', '2500-3500', '3500-4500', 
                '4500-5500', '5500-6500', '6500-7500', '7500+']
    )
    # Create age groups
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 18, 25, 35, 45, 55, 65],
        labels=['13-18', '19-25', '26-35', '36-45', '46-55', '56-65']
    )
    return df

###################
# Global Navigation
###################
def create_navigation():
    with st.sidebar:
        st.title("Navigation")

        # Page selection (appears first)
        page = st.radio(
            "Go to page",
            ["Overview", "User Goals Analysis", "User Engagement Analysis", "Device Analysis"],
            key="nav"
        )

        st.markdown("---")

        # Platform selection (appears below the page radio buttons)
        st.subheader("Choose a Platform")
        global_platform = st.selectbox(
            label="",
            options=["All Platforms"] + sorted(["Facebook", "Instagram", "TikTok", "Twitter", "YouTube"]),
            key="global_platform",
            help="Select the social platform to analyze"
        )

        # st.markdown(
        #     "<h3 style='margin-bottom: 0rem;'>Choose a Platform</h3>", 
        #     unsafe_allow_html=True
        # )
        # global_platform = st.selectbox(
        #     label="", 
        #     options=["All Platforms", "Facebook", "Instagram", "TikTok", "Twitter", "YouTube"]
        # )


        # Add colorblind mode option
        st.markdown("---")
        st.subheader("Accessibility")
        colorblind_mode = st.checkbox("Colorblind-friendly mode", value=False, key="colorblind_mode",
                          help="Enable colorblind-friendly color palette")

    # Return page, platform, and colorblind mode setting
    return page, global_platform, colorblind_mode

###################
# Home Page
###################
def create_welcome_page():
    df = load_data()

    col1, col2 = st.columns([2.5, 1.5])

    with col1:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True) 
        st.markdown("""
            
            <h2 style="font-size: 24px; margin-bottom: 8px;">Welcome to the Social Media Analytics Dashboard!</h2>
            <hr style="margin-top:4px; margin-bottom:16px;">

            <p style="font-size: 14px;">
            This dashboard is part of the final project for the Information Visualization course.  
            It provides visualizations aimed at helping social media platform developers gain deeper insights into user behavior, enhance user experiences, and optimize platform designs to increase engagement and traffic.
            </p>

            <p style="font-size: 14px;">
            <strong>Dataset Source:</strong> 
            <a href="https://www.kaggle.com/datasets/vardhansiramdas/social-media-and-entertainment-dataset" target="_blank">
                Kaggle - Social Media and Entertainment Dataset
            </a>
            </p>

            <p style="font-size: 14px;">
            The dataset contains information on <strong>300,000 users</strong> from diverse backgrounds, collected from various social media platforms.  
            It includes features such as demographics, daily activity, digital behavior, lifestyle metrics and technical details.
            </p>

            <hr style="margin-top:25px; margin-bottom:15px;">
            <h4 style="font-size: 16px;">How to Navigate the Dashboard?</h4>
            <p style="font-size: 13px;">
            
            On the left, you will find three tabs, each dedicated to a specific question.  
            Each page includes a short explanation of the question it addresses, along with guidance on how to interact with the visualizations.  
            In addition, you can filter the data by your platform of interest and view the relevant visualizations accordingly.  
            A colorblind-friendly mode is also available and applies across the entire dashboard.  
            Each tab operates independently – filters in one tab won't affect the others.

            </p>
        """, unsafe_allow_html=True)

    with col2:
        st.image("image homepage.png", use_container_width=True)

        st.markdown("""
            <div style="background-color: rgba(240, 240, 240, 0.7); padding: 15px; border-radius: 10px; margin-top: 20px;">
                <h4 style="font-size: 16px;">📊 Graphs on the Dashboard</h4>
                <p style="font-size: 13px;">
                    All graphs on this site support zooming in for closer analysis.  
                    To zoom in, click and drag over the desired area on the graph.  
                    To reset the view and zoom back out, simply double-click anywhere on the graph.
                </p>
            </div>
        """, unsafe_allow_html=True)



###################
# Helper Functions FOR Q1
###################

PLATFORM_COLORS = {
    'Facebook': '#4267B2',
    'Instagram': '#bc2a8d',
    'Twitter': '#1DA1F2',
    'TikTok': '#000000',
    'YouTube': '#FF0000'
}

def create_small_multiples_by_goal(data_df, group_col):
   

    goal_colors = st.session_state.goal_colors
    goals = sorted(data_df['Primary Social Media Goal'].unique())
    plots = []
    total_by_group = data_df.groupby(group_col).size()

    for goal in goals:
        goal_df = data_df[data_df['Primary Social Media Goal'] == goal]
        counts = goal_df.groupby(group_col).size()
        percentages = (counts / total_by_group * 100).reset_index()
        percentages.columns = [group_col, 'Percentage']
        percentages['Goal'] = goal

        fig = px.bar(
            percentages,
            x=group_col,
            y='Percentage',
            color_discrete_sequence=[goal_colors.get(goal, '#888')],
            title=goal
        )

        fig.update_layout(
            height=180,
            margin=dict(t=20, b=10, l=10, r=10),  
            title=dict(font=dict(size=16), x=0.5),
            xaxis_title=None,
            yaxis_title="%",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

        plots.append(fig)

    return plots

def create_distribution_plot(data_df, group_col, title, show_legend=True, selected_goals=None):
 

    goal_colors = st.session_state.goal_colors
    if selected_goals is None:
        selected_goals = sorted(data_df['Primary Social Media Goal'].unique())

    # Filter out occupations if needed
    if group_col == 'Occupation':
        selected_occupations = ['Professional', 'Student', 'Self-Employed', 'Retired', 'Unemployed', 'Other']
        data_df = data_df[data_df[group_col].isin(selected_occupations)]

    data_df = data_df.dropna(subset=[group_col])

    data_df[group_col] = data_df[group_col].replace(["", "undefined", None], "Other")

    total_by_group = data_df.groupby(group_col).size()
    plot_data = []

    for goal in sorted(selected_goals):
        goal_df = data_df[data_df['Primary Social Media Goal'] == goal]
        counts = goal_df.groupby(group_col).size()
        percentages = (counts / total_by_group * 100).reset_index()
        percentages.columns = [group_col, 'Percentage']
        percentages['Goal'] = goal
        plot_data.append(percentages)

    if not plot_data:
        return None

    plot_df = pd.concat(plot_data)

    fig = px.bar(
        plot_df,
        x=group_col,
        y='Percentage',
        color='Goal',
        barmode='group',
        color_discrete_map=goal_colors,
        labels={'Percentage': 'Percentage of Users', group_col: group_col.replace('_', ' '), 'Goal': 'Goal'}
    )

    fig.for_each_annotation(lambda a: a.update(text=''))

    # Remove the title from the plot - we'll use a Streamlit markdown header instead
    fig.update_layout(
        title=None,  
        legend_title=None,
        height=500,
        margin=dict(l=60, r=40, t=40, b=40),  # Reduced top margin since we removed the title
        showlegend=show_legend,
        legend_title_text='',
        xaxis_title=None,
        yaxis=dict(
            title=dict(
                text="Percentage (%)",
                font=dict(size=16),
                standoff=30
            ),
            tickfont=dict(size=14)
        ),
        xaxis=dict(
            title=dict(
                text=group_col.replace('_', ' '),
                font=dict(size=16)
            ),
            tickfont=dict(size=14)
        ),
        hoverlabel=dict(
            font_size=16,
            font_color="white",
            bgcolor="rgba(0,0,0,0.8)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title_text='',
            font=dict(size=16),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            borderwidth=0,
            itemwidth=50
        )
        if show_legend else {},
    )
    return fig

###################
# Q1- User Goals Analysis
###################


def user_goals_analysis(global_platform):


    
    add_title_with_spacing("User Goals Analysis")
    df = load_data()

    if st.session_state.get('colorblind_mode', False):
        col1, col2 = st.columns([3, 1])
        with col2:
            st.markdown("""
                <div style="background-color: #1E3A8A; color: white; padding: 10px; 
                border-radius: 5px; text-align: center; margin-bottom: 20px;">
                    🌈 <b>Colorblind-friendly mode active</b>
                </div>
            """, unsafe_allow_html=True)


    title_col, help_col = st.columns([0.7, 0.3])
    with title_col:
        if global_platform != "All Platforms":
            st.markdown(f"### Analysis for {global_platform}")
        else:
            st.markdown("### Analysis for All Platforms")
    with help_col:
        with st.expander("ℹ️ Page Guide"):
            st.markdown("""
                This section explores user goals across different personal characteristics.

You can select the personal attribute that interests you and view the distribution of user goals within that attribute.

In addition, you can see the distribution for each goal separately to focus the analysis on a specific goal or compare across groups within that goal
            """)


    st.markdown("""
        <style>
        div[data-testid="stSelectbox"] {
            max-height: 40px;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    
    group_options = {
        'Age_Group': 'Age Group',
        'Country': 'Country',
        'Income_Group': 'Income Level',
        'Occupation': 'Occupation'
    }

    selected_group = st.selectbox(
        "Filter by Category",
        options=list(group_options.keys()),
        format_func=lambda x: group_options[x],
        help="Select a category to view the goal distribution"
    )

    st.markdown("---")

    col1, col2 = st.columns([2.5, 2.7])
 
    with col1:
        # Add a header with the same styling as the "Small Multiples by Goal"
        st.markdown(f"#### Goals Distribution by {group_options[selected_group]}")
        
        all_goals = ['Education', 'Entertainment', 'Networking', 'News']
        fig = create_distribution_plot(
            df,
            selected_group,
            title="", 
            show_legend=True,
            selected_goals=all_goals
        )
        if fig:
            
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Add title at the same level as the left column
        st.markdown("#### Small Multiples by Goal")
        
        # Add spacing to push the small multiples down to align with the main chart
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        
        small_figs = create_small_multiples_by_goal(df, selected_group)

        # Adjust the layout of the small multiples for better alignment
        # First row - Education and Entertainment
        row1_cols = st.columns(2)
        with row1_cols[0]:
            st.plotly_chart(small_figs[0], use_container_width=True)
        with row1_cols[1]:
            st.plotly_chart(small_figs[1], use_container_width=True)
            
        # Add spacing between rows
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
        # Second row - Networking and News
        row2_cols = st.columns(2)
        with row2_cols[0]:
            st.plotly_chart(small_figs[2], use_container_width=True)
        with row2_cols[1]:
            st.plotly_chart(small_figs[3], use_container_width=True)










def engagement_metrics_analysis(global_platform):
    add_title_with_spacing("User Engagement Analysis")
    
    if st.session_state.get('colorblind_mode', False):
        col1, col2 = st.columns([3, 1])
        with col2:
            st.markdown("""
                <div style="background-color: #1E3A8A; color: white; padding: 10px; 
                border-radius: 5px; text-align: center; margin-bottom: 20px;">
                    🌈 <b>Colorblind-friendly mode active</b>
                </div>
            """, unsafe_allow_html=True)


    st.markdown("", unsafe_allow_html=True)
    
    df = load_data()

    # Filter for the main (sidebar-selected) platform if not "All Platforms"
    # if global_platform != "All Platforms":
    #     df_main = df[df['Primary Platform'] == global_platform]
    #     st.markdown(f"### Analysis for {global_platform}")
    # else:
    #     df_main = df.copy()
    #     st.markdown("### Analysis for All Platforms")

    if global_platform != "All Platforms":
        df_main = df[df['Primary Platform'] == global_platform]
        title_col, help_col = st.columns([0.7, 0.3])
        with title_col:
            st.markdown(f"### Analysis for {global_platform}")
        with help_col:
            with st.expander("ℹ️ Page Guide"):
                st.markdown("""
                    This section explores how user-initiated interactions- notifications or ad clicks- affect time spent on social media.
You can select a metric- notifications or ad interactions and adjust the interaction range using the scroller. You can also compare with additional platforms to identify trends.
                """)
    else:
        title_col, help_col = st.columns([0.7, 0.3])
        df_main = df.copy()
        with title_col:
            st.markdown("### Analysis for All Platforms")
        with help_col:
            with st.expander("ℹ️ Page Guide"):
                st.markdown("""
                    This section explores how user-initiated interactions- notifications or ad clicks- affect time spent on social media.

You can select a metric- notifications or ad interactions and adjust the interaction range using the scroller.
 You can also compare with additional platforms to identify trends.
                """)


    # with st.expander("Analysis Guide and Insights", expanded=False):
    #     st.markdown("""
    #         This section explores how user-initiated interactions- notifications or ad clicks-
    #         affect time spent on social media.
            
    #         You can select a metric- notifications or ad interactions and adjust the interaction range
    #         using the scroller. You can also compare with additional platforms to identify trends.
    #     """)    

    # Create two columns: left for the chart, right for metric & controls
    # Changing ratio to [7, 3] => ~70% for the chart, ~30% for the controls
    col1, col2 = st.columns([7, 3])

    with col2:
        # 1) Metric choice
        st.markdown("<h4>Select Metric</h4>", unsafe_allow_html=True)
        metric_choice = st.radio(
            "",
            ["Notifications", "Ad Interactions"],
            key="metric_choice"
        )

        
        if metric_choice == "Notifications":
            max_range = 200
        else:
            max_range = 50

        range_values = st.slider(
            "Choose a range",
            min_value=0,
            max_value=max_range,
            value=(0, max_range),
            step=5,
            key="range_slider"
        )

        # 2) Multiple platforms comparison
        
        st.markdown("<h4 style='white-space: nowrap;'>Compare with additional platforms</h4>", 
                    unsafe_allow_html=True)

        all_platforms = ["Facebook", "Instagram", "TikTok", "Twitter", "YouTube"]
        if global_platform != "All Platforms":
            possible_comparison_platforms = [p for p in all_platforms if p != global_platform]
        else:
            possible_comparison_platforms = all_platforms

        selected_comparison_platforms = st.multiselect(
            "Select one or more platforms to compare",
            options=possible_comparison_platforms,
            default=[]
        )

    with col1:
        # Helper function for correlation data
        def prepare_correlation_data(df_subset, metric_type, r_values):
            if metric_type == "Notifications":
                filtered_df = df_subset[
                    (df_subset['Notifications Received Daily'] >= r_values[0]) & 
                    (df_subset['Notifications Received Daily'] <= r_values[1])
                ]
                correlation = filtered_df.groupby('Notifications Received Daily')['Daily Social Media Time (hrs)'].mean().reset_index()
                x_column = 'Notifications Received Daily'
            else:
                filtered_df = df_subset[
                    (df_subset['Ad Interaction Count'] >= r_values[0]) & 
                    (df_subset['Ad Interaction Count'] <= r_values[1])
                ]
                correlation = filtered_df.groupby('Ad Interaction Count')['Daily Social Media Time (hrs)'].mean().reset_index()
                x_column = 'Ad Interaction Count'
            return correlation, x_column

    
        platform_colors = st.session_state.platform_colors
        

        fig = go.Figure()

        # Main platform trace
        correlation_data_main, x_column_main = prepare_correlation_data(df_main, metric_choice, range_values)
        if global_platform != "All Platforms":
            line_color_main = PLATFORM_COLORS.get(global_platform, '#000000')
            main_name = global_platform
        else:
            line_color_main = '#808080'
            main_name = "All Platforms"

        fig.add_trace(go.Scatter(
            x=correlation_data_main[x_column_main],
            y=correlation_data_main['Daily Social Media Time (hrs)'],
            mode='lines',
            name=main_name,
            line=dict(shape='spline', width=3, color=line_color_main),
        ))

        # Comparison traces
        for compare_plat in selected_comparison_platforms:
            df_compare = df[df['Primary Platform'] == compare_plat]
            correlation_data_compare, x_column_compare = prepare_correlation_data(df_compare, metric_choice, range_values)
            line_color_compare = PLATFORM_COLORS.get(compare_plat, '#666666')
            fig.add_trace(go.Scatter(
                x=correlation_data_compare[x_column_compare],
                y=correlation_data_compare['Daily Social Media Time (hrs)'],
                mode='lines',
                name=compare_plat,
                line=dict(shape='spline', width=3, color=line_color_compare),
            ))

        # Chart title
        title_text = f"Impact of {metric_choice} on Daily Usage"

        # Update layout
        fig.update_layout(
            title=dict(
                text=title_text,
                font=dict(size=20),
                x=0.5
            ),
            xaxis_title=dict(
                text=f"Number of Daily {metric_choice}",
                font=dict(size=14)
            ),
            yaxis_title=dict(
                text="Hours Spent Daily",
                font=dict(size=14)
            ),
            height=450,  # slightly smaller
            plot_bgcolor='white',
            showlegend=True,
            margin=dict(t=40, l=60, r=20, b=50),
            xaxis=dict(
                tickfont=dict(size=12),
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray',
                range=range_values
            ),
            yaxis=dict(
                tickfont=dict(size=12),
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            )
        )

        # Fill the entire width of the left column
        st.plotly_chart(fig, use_container_width=True)











########################
# QUESTION 3 ###########
########################


def device_analysis(global_platform):
    add_title_with_spacing("Device Usage Analysis")

    if st.session_state.get('colorblind_mode', False):
        col1, col2 = st.columns([3, 1])
        with col2:
            st.markdown("""
                <div style="background-color: #1E3A8A; color: white; padding: 10px; 
                border-radius: 5px; text-align: center; margin-bottom: 20px;">
                    🌈 <b>Colorblind-friendly mode active</b>
                </div>
            """, unsafe_allow_html=True)

    # Enhanced title for selected platform
    if global_platform != "All Platforms":
        title_col, help_col = st.columns([0.7, 0.3])
        with title_col:
            st.markdown(f"## Analysis for {global_platform}")
        with help_col:
            with st.expander("ℹ️ Page Guide"):
                st.markdown("""
                    This section presents the distribution of device types across the selected social media platform.
You can filter the results by a demographic variable such as country or gender, to explore patterns within specific populations.
Clicking on any device segment of the pie chart displays a trend line showing its usage distribution- you can choose whether to view the distribution by age group or income level, depending on your focus of interest.
                """)
    else:
        title_col, help_col = st.columns([0.7, 0.3])
        with title_col:
            st.markdown("## Analysis for All Platforms")
        with help_col:
            with st.expander("ℹ️ Page Guide"):
                st.markdown("""
                    This section presents the distribution of device types across the selected social media platform.

You can filter the results by a demographic variable such as country or gender, to explore patterns within specific populations.

Clicking on any device segment of the pie chart displays a trend line showing its usage distribution- you can choose whether to view the distribution by age group or income level, depending on your focus of interest.
                """)

    df = load_data()
    
    # Modified demographic filters with multi-select options
    with st.expander("Filter by Demographics", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            # Gender filter - multi-select
            genders = ["Male", "Female", "Other"]
            selected_genders = st.multiselect(
                "Gender",
                genders,
                default=[]
            )
        
        with col2:
            # Country filter - multi-select
            countries = df['Country'].unique().tolist()
            selected_countries = st.multiselect(
                "Country",
                countries,
                default=[]
            )
    
    # Apply filters
    df_filtered = df.copy()
    if global_platform != "All Platforms":
        df_filtered = df_filtered[df_filtered['Primary Platform'] == global_platform]
    
    # Apply demographic filters (with multi-select support)
    if selected_genders:
        df_filtered = df_filtered[df_filtered['Gender'].isin(selected_genders)]
    
    # Removed occupation filter
    
    if selected_countries:
        df_filtered = df_filtered[df_filtered['Country'].isin(selected_countries)]
    
    # Store the filtered dataframe in session state for use with the bar chart
    st.session_state.df_filtered = df_filtered
    
    # Overall Device Distribution
    st.markdown("### Overall Device Distribution")
    
    # Initialize session state for counter if it doesn't exist
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    # Setup layout
    col1, col2 = st.columns([3, 2])
    
    # Define device colors 
    device_colors = st.session_state.device_colors
    
    # Calculate actual device distribution
    device_distribution = df_filtered['Device Type'].value_counts()
    device_percentages = (device_distribution / device_distribution.sum() * 100).round(1)
    
    # Get the list of devices in the correct order
    device_list = device_distribution.index.tolist()
    
    # Create the pie chart
    with col1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=device_list,
            values=device_distribution.values.tolist(),
            textinfo='label+percent',
            textfont=dict(size=16),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>",
            marker=dict(
                colors=[device_colors.get(d, '#888888') for d in device_list],
                line=dict(color='white', width=2)
            )
        )])
        
        # Update pie chart prompt based on platform selection
        pie_prompt = "Click on a segment to see demographic trends"  # Changed for both cases
        
        fig_pie.update_layout(
            height=350,
            showlegend=False,
            margin=dict(t=20, b=40, l=20, r=20),
            annotations=[
                dict(
                    text=pie_prompt,
                    x=0.5, y=-0.15,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=16, color="white")
                )
            ],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial",
                bordercolor="darkgray",
                font_color="black"
            ),
        )
        
        unique_key = f"pie_chart_events_{global_platform}_{st.session_state.counter}"
        selected_points = plotly_events(fig_pie, click_event=True, key=unique_key)
    
    # Display different visualizations based on platform selection
    with col2:
        # Check if a segment was clicked
        if selected_points and len(selected_points) > 0:
            clicked_point = selected_points[0]
            
            # Try to get the label directly if available
            if 'label' in clicked_point:
                selected_device = clicked_point['label']
            # Fall back to point/curve number if label is not available
            elif 'pointNumber' in clicked_point:
                point_number = clicked_point['pointNumber']
                if point_number < len(device_list):
                    selected_device = device_list[point_number]
                else:
                    st.warning("Invalid selection. Please try again.")
                    selected_device = None
            # Another fallback for different plotly_events versions
            elif 'pointIndex' in clicked_point:
                point_index = clicked_point['pointIndex']
                if point_index < len(device_list):
                    selected_device = device_list[point_index]
                else:
                    st.warning("Invalid selection. Please try again.")
                    selected_device = None
            else:
                # Last resort - try with the first key we can find that might be an index
                for key in ['curveNumber', 'x', 'y']:
                    if key in clicked_point and isinstance(clicked_point[key], int):
                        index = clicked_point[key]
                        if index < len(device_list):
                            selected_device = device_list[index]
                            break
                else:
                    st.warning("Could not determine which device was selected. Please try again.")
                    selected_device = None
            
            if selected_device:
                # Get the color for the selected device
                device_color = device_colors.get(selected_device, '#888888')
                
                # Create colored text for the selected device
                st.markdown(
                    f"Selected device: <span style='color:{device_color}; font-weight:bold;'>{selected_device}</span>",
                    unsafe_allow_html=True
                )
                
                # Filter data for the selected device FROM THE FILTERED DATAFRAME
                device_data = st.session_state.df_filtered[st.session_state.df_filtered['Device Type'] == selected_device]
                
                # SIMPLIFIED: Show demographic trends directly for both 'All Platforms' and specific platform
                
                # --> [שינוי כאן]: עדכון כותרת המדרוג כאשר global_platform == "All Platforms"
                if global_platform == "All Platforms":
                    st.markdown(
                        f"### Demographics for <span style='color:{device_color}; font-weight:bold;'>{selected_device}</span> across All Platforms",
                        unsafe_allow_html=True
                    )
                else:
                    # Get platform color
                    platform_colors = st.session_state.platform_colors
                    platform_color = platform_colors.get(global_platform, '#FFFFFF')
                    
                    # For dark colored platforms like TikTok, add a light border or background
                    if platform_color == "#000000" or platform_color.lower() in ["#000", "black"]:
                        st.markdown(
                            f"""### Demographics for <span style='color:#FFFFFF; background-color:#444444; padding:2px 8px; border-radius:4px;'>{global_platform}</span> on <span style='color:{device_color}; font-weight:bold;'>{selected_device}</span>""",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"### Demographics for <span style='color:{platform_color}; font-weight:bold;'>{global_platform}</span> on <span style='color:{device_color}; font-weight:bold;'>{selected_device}</span>",
                            unsafe_allow_html=True
                        )
                
                # Option to toggle between Age and Income visualizations
                trend_type = st.radio(
                    "Select demographic to visualize:",
                    ["Age Group", "Income Level"],
                    horizontal=True,
                    key=f"trend_radio_{selected_device}"
                )
                
                if trend_type == "Age Group":
                    # Prepare age group data
                    age_bins = [13, 18, 25, 35, 45, 55, 65, 100]
                    age_labels = ["13-18", "19-25", "26-35", "36-45", "46-55", "56-65", "65+"]
                    
                    # Add age group column to device data
                    device_data['Age Group'] = pd.cut(
                        device_data['Age'], 
                        bins=age_bins, 
                        labels=age_labels, 
                        right=True
                    )
                    
                    # Get counts by age group
                    age_counts = device_data['Age Group'].value_counts().sort_index()
                    age_percentages = (age_counts / len(device_data) * 100).round(1)
                    
                    # Create scatter with trend line
                    fig_trend = go.Figure()
                    
                    # Add scatter plot
                    fig_trend.add_trace(go.Scatter(
                        x=age_percentages.index,
                        y=age_percentages.values,
                        mode='markers+lines',
                        marker=dict(
                            size=12,
                            color=device_color,
                            line=dict(width=2, color='DarkSlateGrey')
                        ),
                        line=dict(color=device_color, width=3),
                        name=f"{selected_device} by Age Group",
                        hovertemplate="Age Group: %{x}<br>Percentage: %{y:.1f}%<extra></extra>"
                    ))
                    
                    # Customize title based on global platform
                    title_text = f"Age Distribution for {selected_device}" if global_platform == "All Platforms" else f"Age Distribution for {selected_device} on {global_platform}"
                    
                    # Update layout
                    fig_trend.update_layout(
                        title=title_text,
                        xaxis_title="Age Group",
                        yaxis_title="Percentage (%)",
                        height=350,
                        margin=dict(t=50, b=20, l=20, r=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        hoverlabel=dict(
                            bgcolor="white",
                            font_size=14,
                            font_family="Arial",
                            bordercolor="darkgray",
                            font_color="black"
                        ),
                    )
                    
                    st.plotly_chart(fig_trend, use_container_width=True)
                    
                else:  # Income Level
                    # Add income group column with more detailed ranges
                    income_bins = [0, 1000, 2000, 3000, 4000, 5000, 7500, 10000, 100000]
                    income_labels = [
                        "<$1000", 
                        "$1000-$2000", 
                        "$2000-$3000", 
                        "$3000-$4000", 
                        "$4000-$5000", 
                        "$5000-$7500", 
                        "$7500-$10000", 
                        ">$10000"
                    ]
                    
                    device_data['Income Group'] = pd.cut(
                        device_data['Monthly Income (USD)'], 
                        bins=income_bins, 
                        labels=income_labels, 
                        right=True
                    )
                    
                    # Get counts by income group
                    income_counts = device_data['Income Group'].value_counts().sort_index()
                    income_percentages = (income_counts / len(device_data) * 100).round(1)
                    
                    # Create scatter with trend line
                    fig_trend = go.Figure()
                    
                    # Add scatter plot
                    fig_trend.add_trace(go.Scatter(
                        x=income_percentages.index,
                        y=income_percentages.values,
                        mode='markers+lines',
                        marker=dict(
                            size=12,
                            color=device_color,
                            line=dict(width=2, color='DarkSlateGrey')
                        ),
                        line=dict(color=device_color, width=3),
                        name=f"{selected_device} by Income Group",
                        hovertemplate="Income Group: %{x}<br>Percentage: %{y:.1f}%<extra></extra>"
                    ))
                    
                    # Customize title based on global platform
                    title_text = f"Income Distribution for {selected_device}" if global_platform == "All Platforms" else f"Income Distribution for {selected_device} on {global_platform}"
                    
                    # Update layout
                    fig_trend.update_layout(
                        title=title_text,
                        xaxis_title="Income Group",
                        yaxis_title="Percentage (%)",
                        height=350,
                        margin=dict(t=50, b=20, l=20, r=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        hoverlabel=dict(
                            bgcolor="white",
                            font_size=14,
                            font_family="Arial",
                            bordercolor="darkgray",
                            font_color="black"
                        ),
                    )
                    
                    st.plotly_chart(fig_trend, use_container_width=True)
        else:
            # Prompt to click on the pie chart
            st.info("👈 Click on a device in the pie chart to see demographic trends")



###################
# Main App Logic
###################
def main():
    load_css()
    
    page, global_platform, colorblind_mode = create_navigation()

    # Get appropriate color palette based on colorblind setting
    platform_colors, device_colors, goal_colors = get_color_palette(colorblind_mode)

    # Store in session state for access by all functions
    st.session_state.platform_colors = platform_colors
    st.session_state.device_colors = device_colors
    st.session_state.goal_colors = goal_colors

    if page == "Overview":
        create_welcome_page()
    elif page == "User Goals Analysis":
        user_goals_analysis(global_platform)
    elif page == "User Engagement Analysis":
        engagement_metrics_analysis(global_platform)
    elif page == "Device Analysis":
        device_analysis(global_platform)

if __name__ == "__main__":
    main()