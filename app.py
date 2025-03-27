import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

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
        </style>
    """, unsafe_allow_html=True)


###################
# Data Loading
###################
# Load data
@st.cache_data
def load_data():

    df= pd.read_csv('finalsocial.csv')
    # Create income groups
    df['Income_Group'] = pd.cut(
        df['Monthly Income (USD)'],
        bins=[ 500, 1500, 2500, 3500, 4500, 5500, 6500, 7500,float('inf')],
        labels=[ '500-1500', '1500-2500', '2500-3500', '3500-4500', 
                '4500-5500', '5500-6500', '6500-7500', '7500+']
    )
    # Create age groups
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 18, 25, 35, 45, 55,65],
        labels=['13-18', '19-25', '26-35', '36-45', '46-55', '56-65']
    )
    return df



###################
# Page Components
###################




###################
# Home Page
###################

def create_welcome_page():
    df = load_data()
    
    # Hero section
    st.markdown("""
        <div class="hero">
            <div class="hero-title">Social Media Usage Patterns</div>
            <div class="hero-subtitle">
                Explore comprehensive insights into social media behavior across platforms, 
                demographics, and user goals.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-value">300,000</div>
                <div class="stat-label">Total Records</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-value">5</div>
                <div class="stat-label">Social Platforms</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        platforms_count = len(df['Primary Platform'].unique())
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{len(df['Country'].unique())}</div>
                <div class="stat-label">Countries</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        goals_count = len(df['Primary Social Media Goal'].unique())
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{goals_count}</div>
                <div class="stat-label">User Goals</div>
            </div>
        """, unsafe_allow_html=True)

    # Description
    st.markdown("### About This Analysis")
    st.write("Welcome to our analysis of social media usage patterns and user goals.")
    
    # Quick start guide
    st.info("""
        📊 *How to use this dashboard:*
        1. Use the navigation menu to explore different analyses
        2. Start with the overview graphs showing general patterns
        3. Filter by platform and goals to dive deeper
        4. Click 'Expand' on any graph for a detailed view
    """)



################
# Navigation
################



def create_navigation():
    with st.sidebar:
        st.title("Navigation")
        return st.radio(
            "Go to",
            ["Overview", "User Goals Analysis", "User Engagement Analysis", "Device Analysis"],
            key="nav"
        )




###############]
# platform icons
##############
def create_platform_bar_chart(platform_percentages, selected_device):
    # Platform icons using emoji/unicode symbols
    platform_colors = {
        'Facebook': '#4267B2',  # Facebook blue
        'Instagram': '#E1306C',  # Instagram pink
        'TikTok': '#69C9D0',    # TikTok teal
        'Twitter': '#1DA1F2',   # Twitter blue
        'YouTube': '#FF0000'    # YouTube red
    }
    
    # Platform names with emoji
    platform_labels = {
        'Facebook': 'Facebook 📱',
        'Instagram': 'Instagram 📸',
        'TikTok': 'TikTok 🎵',
        'Twitter': 'Twitter 🐦',
        'YouTube': 'YouTube ▶️'
    }
    
    fig = go.Figure(data=[go.Bar(
        x=platform_percentages.index,
        y=platform_percentages.values,
        text=platform_percentages.values.round(1).astype(str) + '%',
        textposition='auto',
        marker_color=[platform_colors.get(p, 'rgb(71, 135, 199)') for p in platform_percentages.index],
        hovertemplate='%{x}<br>%{y:.1f}%<extra></extra>',
        customdata=[platform_labels.get(p, p) for p in platform_percentages.index]
    )])
    
    fig.update_layout(
        title=f"{selected_device} Usage Across Platforms",
        xaxis_title="Platform",
        yaxis_title="Percentage of Users",
        yaxis_range=[0, 100],
        height=400,
        margin=dict(t=30, b=20, l=20, r=20)
    )
    
    # Update x-axis labels with emoji
    fig.update_xaxes(
        ticktext=[platform_labels.get(p, p) for p in platform_percentages.index],
        tickvals=list(range(len(platform_percentages.index)))
    )
    
    return fig

# Platform colors dictionary
PLATFORM_COLORS = {
    'Instagram': '#E1306C',
    'Facebook': '#4267B2',
    'Twitter': '#1DA1F2',
    'TikTok': '#FFFFFF',
    'YouTube': '#FF0000'
}

def create_small_multiples_by_goal(data_df, group_col):
    goal_colors = {
        'Education': '#4267B2',
        'Entertainment': '#f39c12',
        'Networking': '#2ecc71',
        'News': '#E1306C',
    }

    goals = sorted(data_df['Primary Social Media Goal'].unique())
    plots = []

    total_by_group = data_df.groupby(group_col).size()

    for goal in goals:
        goal_df = data_df[data_df['Primary Social Media Goal'] == goal]
        counts = goal_df.groupby(group_col).size()
        percentages = (counts / total_by_group * 100).reset_index()
        percentages.columns = [group_col, 'Percentage']

        fig = px.bar(
            percentages,
            x=group_col,
            y='Percentage',
            color_discrete_sequence=[goal_colors.get(goal, '#888')],
            title=goal
        )

        fig.update_layout(
            height=300,
            margin=dict(t=40, b=40, l=40, r=20),
            title=dict(font=dict(size=20), x=0.5),
            xaxis_title=None,
            yaxis_title="%",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        plots.append(fig)

    return plots

def user_goals_analysis():
    st.title("User Goals Analysis")
    df = load_data()

    with st.expander("📊 Analysis Guide and Insights", expanded=True):
        st.markdown("""
            [This section will contain guidance on how to interpret the visualizations 
            and key insights from the data analysis.]
        """)

    col1, col2 = st.columns([1, 2])

    with col1:
        platform = st.selectbox(
            "Select Platform",
            options=["All Platforms"] + sorted(list(PLATFORM_COLORS.keys())),
            help="Choose a platform to analyze or view all platforms"
        )

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
            help="Select one category to view the goal distribution by"
        )

    with col2:
        if platform != "All Platforms":
            goals = st.multiselect(
                "Select Goals",
                options=sorted(df['Primary Social Media Goal'].unique()),
                default=[df['Primary Social Media Goal'].iloc[0]],
                help="Select one or more goals to analyze"
            )

    st.markdown("---")

    def create_distribution_plot(data_df, group_col, title, show_legend=True, platform=None, selected_goals=None):
        goals_to_plot = selected_goals if selected_goals is not None else sorted(data_df['Primary Social Media Goal'].unique())

        goal_colors = {
            'Education': '#4267B2',
            'Entertainment': '#f39c12',
            'Networking': '#2ecc71',
            'News': '#E1306C',
        }
        goals_to_plot = sorted(goals_to_plot)

        if group_col == 'Occupation':
            selected_occupations = ['Professional', 'Student', 'Self-Employed', 'Retired', 'Unemployed', 'Other']
            data_df = data_df[data_df[group_col].isin(selected_occupations)]

        total_by_group = data_df.groupby(group_col).size()
        plot_data = []

        for goal in goals_to_plot:
            goal_df = data_df[data_df['Primary Social Media Goal'] == goal]
            counts = goal_df.groupby(group_col).size()
            percentages = (counts / total_by_group * 100).reset_index()
            percentages['Goal'] = goal
            plot_data.append(percentages)

        if not plot_data:
            return None

        plot_df = pd.concat(plot_data)

        title_emojis = {
            'Age_Group': '👥',
            'Country': '🌎',
            'Income_Group': '💰',
            'Occupation': '💼'
        }

        title_with_emoji = f"{title} {title_emojis.get(group_col, '')}"

        fig = px.bar(
            plot_df,
            x=group_col,
            y=0,
            color='Goal',
            barmode='group',
            color_discrete_map=goal_colors,
            labels={'0': 'Percentage of Users', group_col: group_col.replace('_', ' ')}
        )

        fig.update_layout(
            title=dict(
                text=title_with_emoji if title else "",
                font=dict(size=24, color="white"),
                y=0.97
            ),
            height=500,
            margin=dict(l=60, r=40, t=80, b=40),
            showlegend=show_legend,
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
                yanchor="top",
                y=0.88,
                xanchor="center",
                x=0.5,
                font=dict(size=20),
                bgcolor="rgba(0,0,0,0.5)",
                itemwidth=50
            ) if show_legend else {},
        )
        return fig

    if platform == "All Platforms":
        goals = sorted(df['Primary Social Media Goal'].unique())

        title_dict = {
            'Age_Group': "Goals Distribution by Age Group",
            'Country': "Goals Distribution by Country",
            'Income_Group': "Goals Distribution by Income Level",
            'Occupation': "Goals Distribution by Occupation"
        }

        fig = create_distribution_plot(
            df,
            selected_group,
            title_dict[selected_group],
            show_legend=True,
            platform="All Platforms"
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Small Multiples by Goal 🎯")
        small_figs = create_small_multiples_by_goal(df, selected_group)
        for f in small_figs:
            st.plotly_chart(f, use_container_width=True)

    else:
        if not goals:
            st.warning("Please select at least one goal to analyze.")
            return

        st.markdown(f"""
            <h2 style='text-align: center;'>
                <span style='color: white;'>Goal Distribution Analysis for </span>
                <span style='color: {PLATFORM_COLORS[platform]};'>{platform}</span>
            </h2>
        """, unsafe_allow_html=True)

        platform_df = df[df['Primary Platform'] == platform]

        title_dict = {
            'Age_Group': "Age Distribution",
            'Country': "Country Distribution",
            'Income_Group': "Income Distribution",
            'Occupation': "Occupation Distribution"
        }

        emojis = {
            'Age_Group': '👥',
            'Country': '🌎',
            'Income_Group': '💰',
            'Occupation': '💼'
        }

        fig = create_distribution_plot(
            platform_df,
            selected_group,
            "",
            show_legend=True,
            platform=platform,
            selected_goals=goals
        )

        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                f"<h3 style='text-align: center;'>{title_dict[selected_group]} {emojis[selected_group]}</h3>",
                unsafe_allow_html=True
            )

                    

#################
# QUESTION 2
##################

##############################
def engagement_metrics_analysis():
    st.title("User Engagement Analysis")
    st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
    
    df = load_data()
    
    # Initialize session states
    if 'selected_platforms' not in st.session_state:
        st.session_state.selected_platforms = ["All Platforms"]
    if 'platform_states' not in st.session_state:
        st.session_state.platform_states = {}
    
    platform_colors = {
        'All Platforms': '#000000',
        'Facebook': '#4267B2',
        'Instagram': '#E1306C',
        'Twitter': '#1DA1F2',
        'TikTok': '#69C9D0',
        'YouTube': '#FF0000'
    }

    col1, col2 = st.columns([4, 1])

    with col2:
        st.markdown("<div style='height: 100px'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='font-size: 22px;'>Select Metric</h2>", unsafe_allow_html=True)
        metric_choice = st.radio(" ", ["Notifications", "Ad Interactions"], key="metric_choice")

        st.markdown("<h2 style='font-size: 22px; margin-top: 10px;'>Select Platforms</h2>", unsafe_allow_html=True)
        
        platform_options = sorted(df['Primary Platform'].unique().tolist())
        platforms_to_show = ['All Platforms'] + platform_options

        for platform in platforms_to_show:
            cols = st.columns([4, 1])
            with cols[0]:
                # Use a unique key for each checkbox
                checkbox_state = st.checkbox(
                    platform,
                    value=platform in st.session_state.selected_platforms,
                    key=f"platform_select_{platform}"
                )
                
                # Handle checkbox state change
                if checkbox_state and platform not in st.session_state.selected_platforms:
                    if len(st.session_state.selected_platforms) >= 2:
                        # Remove first platform
                        first_platform = st.session_state.selected_platforms[0]
                        st.session_state.selected_platforms.remove(first_platform)
                    st.session_state.selected_platforms.append(platform)
                elif not checkbox_state and platform in st.session_state.selected_platforms:
                    st.session_state.selected_platforms.remove(platform)
                
            with cols[1]:
                st.markdown(
                    f'<div style="width: 12px; height: 12px; background-color: {platform_colors[platform]}; border-radius: 50%; margin-top: 5px;"></div>',
                    unsafe_allow_html=True
                )

    with col1:
        max_range = 200 if metric_choice == "Notifications" else 50
        range_values = st.slider(
            "Choose specific range",
            min_value=0,
            max_value=max_range,
            value=(0, max_range),
            step=5,
            key="range_slider"
        )

        def prepare_correlation_data(platform_df, metric_type, range_values):
            if metric_type == "Notifications":
                filtered_df = platform_df[
                    (platform_df['Notifications Received Daily'] >= range_values[0]) & 
                    (platform_df['Notifications Received Daily'] <= range_values[1])
                ]
                correlation = filtered_df.groupby('Notifications Received Daily')['Daily Social Media Time (hrs)'].mean().reset_index()
                x_column = 'Notifications Received Daily'
            else:
                filtered_df = platform_df[
                    (platform_df['Ad Interaction Count'] >= range_values[0]) & 
                    (platform_df['Ad Interaction Count'] <= range_values[1])
                ]
                correlation = filtered_df.groupby('Ad Interaction Count')['Daily Social Media Time (hrs)'].mean().reset_index()
                x_column = 'Ad Interaction Count'
            return correlation, x_column

        fig = go.Figure()
        
        platforms_to_plot = st.session_state.selected_platforms if st.session_state.selected_platforms else ["All Platforms"]
        
        for platform in platforms_to_plot:
            platform_df = df if platform == "All Platforms" else df[df['Primary Platform'] == platform]
            correlation_data, x_column = prepare_correlation_data(
                platform_df, 
                metric_choice,
                range_values
            )
            
            fig.add_trace(go.Scatter(
                x=correlation_data[x_column],
                y=correlation_data['Daily Social Media Time (hrs)'],
                mode='lines',
                name=platform,
                line=dict(
                    shape='spline',
                    width=3,
                    color=platform_colors[platform]
                ),
            ))

        st.markdown(
            f"<h1 style='text-align: center; font-size: 28px; margin-bottom: 20px;'>Impact of {metric_choice} on Usage Time</h1>",
            unsafe_allow_html=True
        )

        fig.update_layout(
            xaxis_title=dict(
                text=f"Number of Daily {metric_choice}",
                font=dict(size=16)
            ),
            yaxis_title=dict(
                text="Hours Spent Daily",
                font=dict(size=16)
            ),
            height=500,
            plot_bgcolor='white',
            showlegend=False,
            margin=dict(t=20, l=60, r=20, b=20),
            xaxis=dict(
                tickfont=dict(size=14),
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray',
                range=range_values
            ),
            yaxis=dict(
                tickfont=dict(size=14),
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

##############
# QUESSTION 3
##############




def device_analysis():
    st.title("Device Usage Analysis")
    df = load_data()

    # Common styling dictionaries
    device_colors = {
        'Smartphone': '#FF6B6B',  # Coral Red
        'PC': '#4ECDC4',         # Turquoise
        'Tablet': '#FFD93D'      # Golden Yellow
    }
    
    platform_colors = {
        'Instagram': '#E1306C',
        'Facebook': '#4267B2',
        'Twitter': '#1DA1F2',
        'TikTok': '#69C9D0',
        'YouTube': '#FF0000'
    }
    
    platform_emojis = {
        'Facebook': '📱',
        'Instagram': '📸',
        'TikTok': '🎵',
        'Twitter': '🐦',
        'YouTube': '▶️'
    }

    # Overall Device Distribution Section
    st.header("Overall Device Distribution")
    
    col1, col2 = st.columns([3, 2])
    
    device_distribution = df['Device Type'].value_counts()
    device_percentages = (device_distribution / len(df) * 100).round(1)
    
    with col1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=device_percentages.index,
            values=device_percentages.values,
            textinfo='label+percent',
            textfont=dict(size=16),
            hovertemplate="Device: %{label}<br>Percentage: %{value:.1f}%<extra></extra>",
            marker=dict(colors=[device_colors[device] for device in device_percentages.index])
        )])
        
        fig_pie.update_layout(
            height=400,
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; height: 400px;">
            <h3>📊 Visualization Guide</h3>
            [Your guidance text will go here]
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Analysis Options Selection
    st.markdown("### 📱 Choose Analysis View")
    
    # Centered, shorter selection menu
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analysis_options = st.selectbox(
            "",
            ["Platform Usage Analysis", "Device Distribution by Platform", "Show Both"],
            key="analysis_view"
        )

    if analysis_options in ["Platform Usage Analysis", "Show Both"]:
        # Device selection for platform analysis
        st.markdown("### Select Device Type for Analysis")
        selected_device = st.radio(
            "",
            options=device_percentages.index,
            format_func=lambda x: f"{x} ({device_percentages[x]}%)",
            horizontal=True
        )

        # Platform Usage Analysis Section
        platform_device_counts = df[df['Device Type'] == selected_device]['Primary Platform'].value_counts()
        total_platform_users = df['Primary Platform'].value_counts()
        platform_percentages = (platform_device_counts / total_platform_users * 100).round(1)

        st.markdown(f"#### {selected_device} Usage Across Platforms")
        
        fig_platforms = go.Figure(data=[go.Bar(
            x=platform_percentages.index,
            y=platform_percentages.values,
            text=platform_percentages.values.round(1).astype(str) + '%',
            textposition='auto',
            textfont=dict(size=14),
            marker_color=[platform_colors.get(p, '#000000') for p in platform_percentages.index]
        )])

        fig_platforms.update_layout(
            yaxis_title="Percentage of Users",
            yaxis_range=[0, 100],
            height=500,
            margin=dict(t=20, b=20, l=20, r=20)
        )

        st.plotly_chart(fig_platforms, use_container_width=True)

    if analysis_options in ["Device Distribution by Platform", "Show Both"]:
        st.markdown("---")
        # Platform Device Distribution Section
        # Centered, shorter platform selection
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.markdown("### Select Platform")
            selected_platform = st.selectbox(
                "",
                options=df['Primary Platform'].unique(),
                format_func=lambda x: f"{x} {platform_emojis.get(x, '')}",
                key="platform_select"
            )

        platform_df = df[df['Primary Platform'] == selected_platform]
        platform_device_dist = platform_df['Device Type'].value_counts()
        platform_device_pct = (platform_device_dist / len(platform_df) * 100).round(1)

        st.markdown(f"#### Device Distribution for {selected_platform} {platform_emojis.get(selected_platform, '')} ")
        st.markdown(f"<p style='color: {platform_colors.get(selected_platform, '#FFFFFF')};'>Platform-specific device usage analysis</p>", unsafe_allow_html=True)

        fig_platform = go.Figure()
        
        for device in platform_device_pct.index:
            fig_platform.add_trace(go.Bar(
                x=[selected_platform],
                y=[platform_device_pct[device]],
                name=device,
                text=f"{platform_device_pct[device]:.1f}%",
                textposition='inside',
                textfont=dict(size=14),
                marker_color=device_colors[device]
            ))

        fig_platform.update_layout(
            barmode='stack',
            height=400,
            showlegend=True,
            legend_title="Device Types",
            legend=dict(font=dict(size=14)),
            margin=dict(t=30, b=20, l=20, r=20)
        )

        st.plotly_chart(fig_platform, use_container_width=True)

        # Platform insights
        total_users = len(platform_df)
        primary_device = platform_device_dist.index[0]

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Primary Device",
                primary_device,
                f"{platform_device_pct[primary_device]:.1f}% of users"
            )
        with col2:
            st.metric(
                "Total Users",
                f"{total_users:,}",
                "on this platform"
            )





    ###################
# Main App Logic
###################
def main():
    # Load CSS
    load_css()
    
    # Get current page from navigation
    current_page = create_navigation()
    
    # Route to appropriate page
    if current_page == "Overview":
        create_welcome_page()
    elif current_page == "User Goals Analysis":
        user_goals_analysis()
    elif current_page == "User Engagement Analysis":
        engagement_metrics_analysis()
    elif current_page == "Device Analysis":
        device_analysis()

if __name__ == "__main__":
    main()
