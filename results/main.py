import pandas as pd                         # Data manipulation and analysis
import json                                 # For handling JSON data
import plotly.express as px                 # High-level interface for Plotly visualization
import numpy as np                          # Numerical operations and array handling
from scipy.stats import norm                # Statistical functions, including the normal distribution
import plotly.io as pio                     # Input/Output utilities for Plotly (e.g., saving figures)

# Configure Kaleido for exporting Plotly figures with enhanced resolution
pio.kaleido.scope.default_format = "pdf"    # Set the default export format to PDF
pio.kaleido.scope.default_width = 1200      # Set the default image width
pio.kaleido.scope.default_height = 800      # Set the default image height
pio.kaleido.scope.default_scale = 1.5       # Increase the resolution (scaling factor)

def build_comparison_wins(prefix, row):
    """
    Constructs a dictionary mapping the 6 dimensions (using the same labels as in 'ratings')
    to the number of wins achieved based on the 15 comparison items.
    The prefix represents the common part of the header in the comparison questions,
    for example "Task 1: Introduction & Initial Interaction".
    """
    # Mapping responses (e.g., "Mental Demand") to the keys used in "ratings"
    key_mapping = {
        "Mental Demand": "mental_demand",
        "Physical Demand": "physical_demand",
        "Temporal Demand": "temporal_demand",
        "Performance": "performance",
        "Effort": "effort",
        "Frustration": "frustration"
    }
    
    wins = {
        "mental_demand": 0,
        "physical_demand": 0,
        "temporal_demand": 0,
        "performance": 0,
        "effort": 0,
        "frustration": 0
    }
    for i in range(1, 16):
        col_name = f"{prefix}\n\n{i})"
        if col_name in row and pd.notna(row[col_name]):
            winner_raw = str(row[col_name]).strip()
            if winner_raw in key_mapping:
                key = key_mapping[winner_raw]
                wins[key] += 1
    return wins

def plot_statistics(users, show_plot=False, save_image=True):
    """
    Creates and saves statistical charts based on user data:
        - A pie chart for gender distribution.
        - A pie chart for qualification/profession distribution.
        - A bar chart for XR experience level, categorized as:
            "Inexperienced" (levels 1-2),
            "Average" (levels 3-4),
            "Experienced" (levels 5-6).
    
    Each chart is saved as an SVG file.
    """
    # Build a DataFrame with relevant user data
    data = {
        'gender': [user.gender for user in users],
        'qualification': [user.qualification for user in users],
        'xr_experience': [user.vr_experience for user in users]
    }
    df = pd.DataFrame(data)
    
    # ---------------------------------
    # Pie chart: Gender Distribution
    # ---------------------------------
    fig_gender = px.pie(df, names='gender')
    fig_gender.update_traces(
        textinfo='value+percent',
        textfont=dict(size=30)
    )
    fig_gender.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="center",
            x=0.5,
            font=dict(size=40, color='#333333'),
            itemwidth=40,
            itemsizing='constant',
            bordercolor='gray',
            borderwidth=1
        ),
        margin=dict(t=150, b=80),
        width=1000,
        height=700
    )
    
    # -----------------------------------------
    # Pie chart: Qualification/Profession Distribution
    # -----------------------------------------
    fig_qual = px.pie(df, names='qualification')
    fig_qual.update_traces(
        textinfo='value+percent',
        textfont=dict(size=28)
    )
    fig_qual.update_layout(
        legend=dict(
            font=dict(size=40, color='#333333'),
            itemwidth=40,
            bordercolor='gray',
            borderwidth=1
        )
    )
    
    # ---------------------------------
    # Bar chart: XR Experience Level
    # ---------------------------------
    # Count the number of users for each XR experience level
    vr_counts = df['xr_experience'].value_counts().reset_index()
    vr_counts.columns = ['xr_experience', 'count']
    
    # Convert experience levels to numeric and sort them in ascending order
    vr_counts['xr_experience'] = pd.to_numeric(vr_counts['xr_experience'], errors='coerce')
    vr_counts = vr_counts.sort_values('xr_experience')
    
    # Categorize users based on XR experience level
    def get_group(x):
        if x in [1, 2]:
            return 'Inexperienced'
        elif x in [3, 4]:
            return 'Average'
        elif x in [5, 6]:
            return 'Experienced'
        else:
            return 'Other'
    
    vr_counts['group'] = vr_counts['xr_experience'].apply(get_group)
    
    # Calculate the percentage of users per experience level
    total_users = df.shape[0]
    vr_counts['percentage'] = (vr_counts['count'] / total_users * 100).round(2)
    
    # Create labels displaying the percentage for the bar chart
    vr_counts['text'] = (
        vr_counts['percentage'].astype(str) + "%"
    )
    
    # Custom color mapping for each user category
    color_map = {
        'Inexperienced': '#1f77b4',
        'Average': '#ff7f0e',
        'Experienced': '#2ca02c',
        'Other': '#7f7f7f'
    }
    
    fig_xr = px.bar(
        vr_counts,
        x='xr_experience',
        y='count',
        color='group',
        color_discrete_map=color_map,
        labels={'xr_experience': 'XR Experience', 'count': 'Number of Users', 'group': 'User Category'},
        text=vr_counts['text']
    )
    fig_xr.update_traces(
        textposition='inside',
        textfont=dict(size=22)
    )
    fig_xr.update_layout(
        xaxis=dict(
            title_font=dict(size=30),
            tickfont=dict(size=28)
        ),
        yaxis=dict(
            title_font=dict(size=30),
            tickfont=dict(size=28)
        ),
        legend=dict(
            font=dict(size=40, color='#333333'),
            itemwidth=40,
            bordercolor='gray',
            borderwidth=1
        )
    )
    if show_plot:
        fig_gender.show()
        fig_qual.show()
        fig_xr.show()
    if save_image:
        fig_gender.write_image("gender_distribution.svg")
        fig_qual.write_image("profession_distribution.svg")
        fig_xr.write_image("xr_experience.svg")


def plot_nasa_tlx_spider(dimension_scores_mean_task, user_name, show_plot=False, save_image=True):
    """
    Creates an advanced radar chart with:
        - A custom logarithmic scale (range 4-100)
        - 10 concentric circles with meaningful labels
        - A horizontal legend above the chart
        - Large markers with contrasting borders
        - High-contrast colors
        - Anti-overlap adjustments for identical values
    """
    
    import math
    import plotly.graph_objects as go
    
    # -------------------------------------------------------------------
    # Initial configuration and data mapping
    # -------------------------------------------------------------------    
    # Mapping of full dimension names to short labels for the radar chart
    KEY_MAPPING = {
        "mental_demand": "MD",
        "physical_demand": "PD",
        "temporal_demand": "TD",
        "performance": "P",
        "effort": "E",
        "frustration": "F",
    }
    
    # Task names (formatted for display)
    TASK_NAMES = [
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4"
    ]
    
    # Colors and marker types for each task trace
    COLORS = [
        'rgba(0, 92, 230, 0.9)',    # Electric blue
        'rgba(255, 0, 0, 0.9)',      # Bright red
        'rgba(0, 163, 0, 0.9)',      # Neon green
        'rgba(163, 0, 163, 0.9)'     # Intense purple
    ]
    MARKERS = ['circle', 'square', 'diamond', 'x']
    
    # -------------------------------------------------------------------
    # Support function: adjust_overlaps
    # -------------------------------------------------------------------
    def adjust_overlaps(values):
        """
        Adds small offsets to identical values to prevent marker overlap.
        """
        seen = {}
        adjusted = []
        for idx, val in enumerate(values):
            if val in seen:
                # Calcola offset progressivo basato sulla posizione
                delta = 0.5 * (idx - seen[val])
                adjusted_val = val + delta
                adjusted.append(min(adjusted_val, 100))  # Limite superiore
            else:
                adjusted.append(val)
                seen[val] = idx
        return adjusted
    
    # -------------------------------------------------------------------
    # Data preparation: apply transformation and anti-overlap adjustment
    # -------------------------------------------------------------------    
    # List of dimensions to display on the radar chart
    dimensions = list(KEY_MAPPING.keys())
    
    # Apply a logarithmic transformation to the scores for each dimension
    log_normalized = {
        dim: [x for x in dimension_scores_mean_task[dim]] 
        for dim in dimensions
    }
    
    # Adjust overlapping values to avoid collision of markers
    adjusted_values = {dim: adjust_overlaps(log_normalized[dim]) for dim in dimensions}
    
    
    # -------------------------------------------------------------------
    # Build the radar chart by adding one trace per task
    # -------------------------------------------------------------------
    fig = go.Figure()
    for i in range(4):
        # Extract and format values for the current task
        values = [adjusted_values[dim][i] for dim in dimensions]
        values += [values[0]]
        
        # Crea la traccia
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=[KEY_MAPPING[dim] for dim in dimensions] + [KEY_MAPPING[dimensions[0]]],
            line=dict(color=COLORS[i], width=3.5),
            marker=dict(
                symbol=MARKERS[i],
                size=16,
                color=COLORS[i],
                line=dict(width=2, color='black')
            ),
            name=TASK_NAMES[i],
            fill='toself',
            fillcolor=COLORS[i].replace('0.9)', '0.2)'),
            mode='lines+markers'
        ))
    
    # -------------------------------------------------------------------
    # Final formatting of the radar chart
    # -------------------------------------------------------------------
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 60],
                tickfont=dict(size=25, color='#333333'),
                gridcolor='rgba(100, 100, 100, 0.2)',
                linecolor='gray',
                linewidth=2,
                nticks=0
            ),
            angularaxis=dict(
                tickfont=dict(size=35, color='#333333'),
                linecolor='gray',
                gridcolor='rgba(100, 100, 100, 0.1)',
                rotation=90
            ),
            bgcolor='white'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="center",
            x=0.5,
            font=dict(size=30, color='#333333'),
            itemwidth=40,
            itemsizing='constant',
            bordercolor='gray',
            borderwidth=1
        ),
        margin=dict(t=150, b=80),
        width=1000,
        height=700,
        paper_bgcolor='white'
    )
    
    if show_plot:
        fig.show()
    if save_image:
        fig.write_image(f"./nasa_tlx_{user_name}.svg")
    
def leggi_dati_excel(file_path):
    # Reads an Excel file and creates a list of User objects for each row.
    df = pd.read_excel(file_path)
    users = []
    for _, row in df.iterrows():
        users.append(User(row))
    return users

class User:
    def __init__(self, row):
        # Personal information
        self.gender = str(row["Gender"])
        self.age = str(row["Age"]) if pd.notna(row["Age"]) else None
        self.vr_experience = str(row["VR Experience Level "])
        self.qualification = str(row["Academic/Professional Qualification"])
        
        # SUM questionnaire data
        self.sum = {
            "errori": {
                "Missing 2x Pinch Zoom": int(row["Missing 2x Pinch Zoom"]) if pd.notna(row["Missing 2x Pinch Zoom"]) else None,
                "Missing Pinch Move": int(row["Missing Pinch Move"]) if pd.notna(row["Missing Pinch Move"]) else None,
                "Missing Rotation": int(row["Missing Rotation"]) if pd.notna(row["Missing Rotation"]) else None,
                "Missing Ask Map Functionality": int(row["Missing Ask Map Functionality"]) if pd.notna(row["Missing Ask Map Functionality"]) else None,
                "Number of try asking a position": int(row["Number of try asking a position"]) if pd.notna(row["Number of try asking a position"]) else None,
                "Number of try to enter VR": int(row["Number of try to enter VR"]) if pd.notna(row["Number of try to enter VR"]) else None
            },
            "task1": {
                "difficulty": str(row["Task 1: Introduction & Initial Interaction\n\nHow would you describe how difficult or easy it was to complete this task?   "]),
                "satisfaction": str(row["Task 1: Introduction & Initial Interaction\n\nHow satisfied are you with using this application to complete this task?   "]),
                "time_rating": str(row["Task 1: Introduction & Initial Interaction\n\nHow would you rate the amount of time it took to complete this task?  "]),
                "time": int(row["Task 1 time (in seconds)"]) if pd.notna(row["Task 1 time (in seconds)"]) else None
            },
            "task2": {
                "difficulty": str(row["Task 2: VR/MR Tutorial  \n\nHow would you describe how difficult or easy it was to complete this task?   "]),
                "satisfaction": str(row["Task 2: VR/MR Tutorial  \n\nHow satisfied are you with using this application to complete this task?   "]),
                "time_rating": str(row["Task 2: VR/MR Tutorial  \n\nHow would you rate the amount of time it took to complete this task?  "]),
                "time": int(row["Task 2 time  (in seconds)"]) if pd.notna(row["Task 2 time  (in seconds)"]) else None
            },
            "task3": {
                "difficulty": str(row["Task 3: Map Interaction for Information Retrieval  \n\nHow would you describe how difficult or easy it was to complete this task?   "]),
                "satisfaction": str(row["Task 3: Map Interaction for Information Retrieval  \n\nHow satisfied are you with using this application to complete this task?   "]),
                "time_rating": str(row["Task 3: Map Interaction for Information Retrieval  \n\nHow would you rate the amount of time it took to complete this task?  "]),
                "time": int(row["Task 3 time  (in seconds)"]) if pd.notna(row["Task 3 time  (in seconds)"]) else None
            },
            "task4": {
                "difficulty": str(row["Task 4: VR Navigation (First-Person Experience)  \n\nHow would you describe how difficult or easy it was to complete this task?   "]),
                "satisfaction": str(row["Task 4: VR Navigation (First-Person Experience)  \n\nHow satisfied are you with using this application to complete this task?   "]),
                "time_rating": str(row["Task 4: VR Navigation (First-Person Experience)  \n\nHow would you rate the amount of time it took to complete this task?  "]),
                "time": int(row["Task 4 time  (in seconds)"]) if pd.notna(row["Task 4 time  (in seconds)"]) else None,
                "execution_count": int(row["Task 4 number of times"]) if pd.notna(row["Task 4 number of times"]) else None
            },
            "first_person_experience": str(row["SUM Questionnaire\n\nDid you experience the first-person VR navigation?"])
        }
        
        # SUS questionnaire data
        self.sus = {
            "1_use_freq": str(row["1) I think that I would like to use this system frequently.  "]),
            "2_complexity": str(row["2) I found the system unnecessarily complex.  "]),
            "3_ease": str(row["3) I thought the system was easy to use.  "]),
            "4_support_needed": str(row["4) I think that I would need the support of a technical person to be able to use this system.  "]),
            "5_integration": str(row["5) I found the various functions in this system were well integrated.  "]),
            "6_inconsistency": str(row["6) I thought there was too much inconsistency in this system.  "]),
            "7_learn_speed": str(row["7) I would imagine that most people would learn to use this system very quickly.  "]),
            "8_cumbersome": str(row["8) I found the system very cumbersome to use.  "]),
            "9_confidence": str(row["9) I felt very confident using the system.  "]),
            "10_learning_curve": str(row["10) I needed to learn a lot of things before I could get going with this system.  "])
        }
        
        
        # NASA TLX questionnaire data along with computed comparison wins
        self.nasa_tlx = {
            "task1": {
                "ratings": {
                    "mental_demand": str(row["Task 1: Introduction & Initial Interaction\nMental Demand:\nHow mentally demanding was this task?"]),
                    "physical_demand": str(row["Task 1: Introduction & Initial Interaction\nPhysical Demand\nHow physically demanding was this task?"]),
                    "temporal_demand": str(row["Task 1: Introduction & Initial Interaction\nTemporal Demand\nHow hurried or rushed was the pace of the task?"]),
                    "performance": str(row["Task 1: Introduction & Initial Interaction\nPerformance\nHow successful were you in accomplishing what you were asked to do?\nN.B.\n0 = Perfect\n10 = Failure"]),
                    "effort": str(row["Task 1: Introduction & Initial Interaction\nEffort\nHow hard did you have to work to accomplish your level of performance?  "]),
                    "frustration": str(row["Task 1: Introduction & Initial Interaction\nFrustration\nHow insecure, discouraged, irritated, stressed, and annoyed wereyou?  "])
                },
                "comparison_wins": build_comparison_wins("Task 1: Introduction & Initial Interaction", row)
            },
            "task2": {
                "ratings": {
                    "mental_demand": str(row["Task 2: VR/MR Tutorial\nMental Demand:\nHow mentally demanding was this task?"]),
                    "physical_demand": str(row["Task 2: VR/MR Tutorial\nPhysical Demand\nHow physically demanding was this task?"]),
                    "temporal_demand": str(row["Task 2: VR/MR Tutorial\nTemporal Demand\nHow hurried or rushed was the pace of the task?"]),
                    "performance": str(row["Task 2: VR/MR Tutorial\nPerformance\nHow successful were you in accomplishing what you were asked to do?\nN.B.\n0 = Perfect\n10 = Failure"]),
                    "effort": str(row["Task 2: VR/MR Tutorial\nEffort\nHow hard did you have to work to accomplish your level of performance?  "]),
                    "frustration": str(row["Task 2: VR/MR Tutorial\nFrustration\nHow insecure, discouraged, irritated, stressed, and annoyed wereyou?  "])
                },
                "comparison_wins": build_comparison_wins("Task 2: VR/MR Tutorial", row)
            },
            "task3": {
                "ratings": {
                    "mental_demand": str(row["Task 3: Map Interaction for Information Retrieval\nMental Demand:\nHow mentally demanding was this task?"]),
                    "physical_demand": str(row["Task 3: Map Interaction for Information Retrieval\nPhysical Demand\nHow physically demanding was this task?"]),
                    "temporal_demand": str(row["Task 3: Map Interaction for Information Retrieval\nTemporal Demand\nHow hurried or rushed was the pace of the task?"]),
                    "performance": str(row["Task 3: Map Interaction for Information Retrieval\nPerformance\nHow successful were you in accomplishing what you were asked to do?\nN.B.\n0 = Perfect\n10 = Failure"]),
                    "effort": str(row["Task 3: Map Interaction for Information Retrieval\nEffort\nHow hard did you have to work to accomplish your level of performance?  "]),
                    "frustration": str(row["Task 3: Map Interaction for Information Retrieval\nFrustration\nHow insecure, discouraged, irritated, stressed, and annoyed wereyou?  "])
                },
                "comparison_wins": build_comparison_wins("Task 3: Map Interaction for Information Retrieval", row)
            },
            "task4": {
                "ratings": {
                    "mental_demand": str(row["Task 4: VR Navigation (First-Person Experience)\nMental Demand:\nHow mentally demanding was this task?"]),
                    "physical_demand": str(row["Task 4: VR Navigation (First-Person Experience)\nPhysical Demand\nHow physically demanding was this task?"]),
                    "temporal_demand": str(row["Task 4: VR Navigation (First-Person Experience)\nTemporal Demand\nHow hurried or rushed was the pace of the task?"]),
                    "performance": str(row["Task 4: VR Navigation (First-Person Experience)\nPerformance\nHow successful were you in accomplishing what you were asked to do?\nN.B.\n0 = Perfect\n10 = Failure"]),
                    "effort": str(row["Task 4: VR Navigation (First-Person Experience)\nEffort\nHow hard did you have to work to accomplish your level of performance?  "]),
                    "frustration": str(row["Task 4: VR Navigation (First-Person Experience)\nFrustration\nHow insecure, discouraged, irritated, stressed, and annoyed wereyou?  "])
                },
                "comparison_wins": build_comparison_wins("Task 4: VR Navigation (First-Person Experience)", row)
            },
            "nasa_vr_experience": str(row["Nasa TLX Questionnaire\nDid you experience the first-person VR navigation?"])
        }

def calculate_sus_scores(users):    
    """
    Calculate the System Usability Scale (SUS) score for each user.
    For each user, odd-numbered items contribute positively while even-numbered items contribute negatively.
    The final score is adjusted by adding 20 and multiplying by 2.5.
    Returns a list of dictionaries with each user's name and SUS score, and the average SUS score.
    """
    sus_scores = []
    for user in users:
        total_score_positive = 0
        total_score_negative = 0
        # Iterate through the 10 SUS items
        for i in range(1, 11):
            # Create the key using the index and the corresponding label
            key = f"{i}_" + {
                1: "use_freq",
                2: "complexity",
                3: "ease",
                4: "support_needed",
                5: "integration",
                6: "inconsistency",
                7: "learn_speed",
                8: "cumbersome",
                9: "confidence",
                10: "learning_curve"
            }[i]
            
            score = int(user.sus.get(key))
            # Even-numbered items are negative; odd-numbered items are positive
            if i%2 == 0:
                total_score_negative -= score
            else:
                total_score_positive += score
            total_score = total_score_negative + total_score_positive
        
        # Adjust the total score and scale it to obtain the final SUS score
        total_score += 20
        total_score *= 2.5
        sus_scores.append(total_score)
    sus_scores_value = [sus_score for sus_score in sus_scores]
    return sus_scores, round(sum(sus_scores_value) / len(sus_scores_value), 2)

def calculate_nasa_tlx(users, num_task=4):
    """
    Calculate the NASA TLX scores for each user.
    For each task, this function computes:
        1. A weighted TLX score based on ratings and comparison wins.
        2. The unweighted mean score for each workload dimension.
    Returns the mean score per dimension per task, the raw score per task, and the weighted score per task.
    """
    tasks = ["task" + str(i+1) for i in range(4)]
    # Initialize containers for summing scores and counting ratings for each dimension across tasks
    dimensions = ['mental_demand', 'physical_demand', 'temporal_demand', 'performance', 'effort', 'frustration']
    dimension_scores_task = {
        'mental_demand': [0]*num_task,
        'physical_demand': [0]*num_task,
        'temporal_demand': [0]*num_task,
        'performance': [0]*num_task,
        'effort': [0]*num_task,
        'frustration': [0]*num_task
    }
    dimension_scores_counts_task = {dim: [0]*num_task for dim in dimension_scores_task.keys()}
    
    dimension_scores_task_weighted_list = []
    dimension_scores_task_list = []
    for user in users:
        # Temporary lists to hold the mean scores for the current user per task
        dimension_scores_task_mean_weighted = [0]*num_task
        dimension_scores_task_mean = [0]*num_task
        for i, task_key in enumerate(tasks):
            # Skip task 4 for users who did not experience first-person VR navigation
            if task_key == "task4" and user.nasa_tlx["nasa_vr_experience"] == "No":
                continue
            
            ratings = user.nasa_tlx[task_key]["ratings"]
            comparison = user.nasa_tlx[task_key]["comparison_wins"]
            task_dimension_sum_weighted = 0
            task_dimension_sum = 0
            # Sum scores for each dimension with and without weighting by comparison wins
            for dimension in dimensions:
                task_dimension_sum_weighted += float(ratings[dimension])*10*float(comparison[dimension])
                task_dimension_sum += float(ratings[dimension])*10
                dimension_scores_task[dimension][i] += float(ratings[dimension])*10
                dimension_scores_counts_task[dimension][i] += 1
            # Compute the average weighted and unweighted score for the current task
            dimension_scores_task_mean_weighted[i] = round(task_dimension_sum_weighted/15, 2)
            dimension_scores_task_mean[i] = round(task_dimension_sum/6, 2)
            
        dimension_scores_task_weighted_list.append(dimension_scores_task_mean_weighted)
        dimension_scores_task_list.append(dimension_scores_task_mean)     
    
    # Calculate the mean score per dimension for each task
    dimension_scores_mean_task = {dim: [0]*num_task for dim in dimension_scores_task.keys()}
    for dimension, tasks_value in dimension_scores_task.items():
        for i, task_value in enumerate(tasks_value):
            if dimension_scores_counts_task[dimension][i] == 0:
                continue
            dimension_scores_mean_task[dimension][i] = round(task_value/dimension_scores_counts_task[dimension][i], 2)
    
    # Calculate the average weighted score (w_score) per task
    w_score = [0]*num_task
    w_score_counter = [0]*num_task
    for user_idx, weighted_scores in enumerate(dimension_scores_task_weighted_list):
        for i, weighted_task in enumerate(weighted_scores):
            if i == 3 and users[user_idx].nasa_tlx["nasa_vr_experience"] == "No":
                continue
            w_score[i] += weighted_task
            w_score_counter[i] += 1
    w_score = [round(w_score_i/w_score_counter_i, 2) for w_score_i, w_score_counter_i in zip(w_score, w_score_counter)]
    
    # Calculate the average unweighted (raw) score (r_score) per task
    r_score = [0]*num_task
    r_score_counter = [0]*num_task
    for user_idx, mean_scores in enumerate(dimension_scores_task_list):
        for i, mean_task in enumerate(mean_scores):
            if i == 3 and users[user_idx].nasa_tlx["nasa_vr_experience"] == "No":
                continue
            r_score[i] += mean_task
            r_score_counter[i] += 1
    r_score = [round(r_score_i/r_score_counter_i, 2) for r_score_i, r_score_counter_i in zip(r_score, r_score_counter)]
    
    return dimension_scores_mean_task, r_score, w_score

def calculate_sum_score_complation(users):
    """
    Calculate task completion rates.
    For tasks 1-3, every user is considered to have completed the task.
    For task 4, only users who experienced first-person navigation are counted.
    Returns both the raw counts and the completion percentages for each task.
    """
    complation_raw = {
        "task1" : 0,
        "task2" : 0,
        "task3" : 0,
        "task4" : 0,
    }
    for user in users:
        complation_raw["task1"] += 1
        complation_raw["task2"] += 1
        complation_raw["task3"] += 1
        if user.sum["first_person_experience"] == "Yes":
            complation_raw["task4"] += 1
        
    complation_std = {
        "task1" : round(100*complation_raw["task1"]/len(users), 2),
        "task2" : round(100*complation_raw["task2"]/len(users), 2),
        "task3" : round(100*complation_raw["task3"]/len(users), 2),
        "task4" : round(100*complation_raw["task4"]/len(users), 2),
    }
    return complation_raw, complation_std

def calculate_sum_score_time_on_task(users):
    """
    Calculate the time-on-task scores.
    For each task, this function gathers the time data and computes:
        - The mean time, standard deviation, and a specified percentile time (spec_time) based on a satisfaction threshold.
        - Z-scores comparing the mean time to the specified percentile.
        - Standardized time scores using the normal cumulative distribution.
    Returns both the raw time statistics and the standardized scores.
    """
    spec_satisfaction = 4
    spec_time = [0, 0, 0, 0]
    spec_time_percentage = 95
    
    # Containers for time data for each task and for those meeting the satisfaction criteria
    time_on_task_list = {
        "task1" : [],
        "task2" : [],
        "task3" : [],
        "task4" : [],
        "task1_spec" : [],
        "task2_spec" : [],
        "task3_spec" : [],
        "task4_spec" : [],
    }
    for user in users:
        # Calculate satisfaction scores for tasks 1-3 as the average of difficulty, satisfaction, and time rating
        satisfaction_score_task1 = (float(user.sum["task1"]["difficulty"]) + float(user.sum["task1"]["satisfaction"]) + float(user.sum["task1"]["time_rating"]))/3
        satisfaction_score_task2 = (float(user.sum["task2"]["difficulty"]) + float(user.sum["task2"]["satisfaction"]) + float(user.sum["task2"]["time_rating"]))/3
        satisfaction_score_task3 = (float(user.sum["task3"]["difficulty"]) + float(user.sum["task3"]["satisfaction"]) + float(user.sum["task3"]["time_rating"]))/3
        
        # Append time values for tasks that meet or exceed the satisfaction threshold
        if satisfaction_score_task1 >= spec_satisfaction:
            time_on_task_list["task1_spec"].append(float(user.sum["task1"]["time"]))
        if satisfaction_score_task2 >= spec_satisfaction:
            time_on_task_list["task2_spec"].append(float(user.sum["task2"]["time"]))
        if satisfaction_score_task3 >= spec_satisfaction:
            time_on_task_list["task3_spec"].append(float(user.sum["task3"]["time"]))
        # Always record time values for tasks 1-3
        time_on_task_list["task1"].append(float(user.sum["task1"]["time"]))
        time_on_task_list["task2"].append(float(user.sum["task2"]["time"]))
        time_on_task_list["task3"].append(float(user.sum["task3"]["time"]))
        
        # For task 4, include time only if the user experienced first-person VR navigation
        if user.sum["first_person_experience"] == "Yes":
            time_on_task_list["task4"].append(float(user.sum["task4"]["time"]))
            satisfaction_score_task4 = (float(user.sum["task4"]["difficulty"]) + float(user.sum["task4"]["satisfaction"]) + float(user.sum["task4"]["time_rating"]))/3
            if satisfaction_score_task4 >= spec_satisfaction:
                time_on_task_list["task4_spec"].append(float(user.sum["task4"]["time"]))

    # Compute the specified time (95th percentile) for each task from the satisfied subset
    spec_time[0] = np.percentile(time_on_task_list["task1_spec"], spec_time_percentage)   
    spec_time[1] = np.percentile(time_on_task_list["task2_spec"], spec_time_percentage)   
    spec_time[2] = np.percentile(time_on_task_list["task3_spec"], spec_time_percentage)   
    spec_time[3] = np.percentile(time_on_task_list["task4_spec"], spec_time_percentage)   
    
    # Calculate raw time statistics: mean, standard deviation, and spec_time for each task
    time_on_task_raw = {
        "task1" : [np.mean(time_on_task_list["task1"]), np.std(time_on_task_list["task1"]), spec_time[0]],
        "task2" : [np.mean(time_on_task_list["task2"]), np.std(time_on_task_list["task2"]), spec_time[1]],
        "task3" : [np.mean(time_on_task_list["task3"]), np.std(time_on_task_list["task3"]), spec_time[2]],
        "task4" : [np.mean(time_on_task_list["task4"]), np.std(time_on_task_list["task4"]), spec_time[3]],
    }
    
    # Compute z-scores for each task: how far the mean is from the spec_time, scaled by the standard deviation
    z_scores_time = {
        "task1" : -(time_on_task_raw["task1"][0] - time_on_task_raw["task1"][2]) / time_on_task_raw["task1"][1],
        "task2" : -(time_on_task_raw["task2"][0] - time_on_task_raw["task2"][2]) / time_on_task_raw["task2"][1],
        "task3" : -(time_on_task_raw["task3"][0] - time_on_task_raw["task3"][2]) / time_on_task_raw["task3"][1],
        "task4" : -(time_on_task_raw["task4"][0] - time_on_task_raw["task4"][2]) / time_on_task_raw["task4"][1],
    }
    
    # Convert z-scores into standardized time scores using the normal cumulative distribution function
    time_on_task_std = {
        "task1": round(100*norm.cdf(z_scores_time["task1"]), 2),
        "task2": round(100*norm.cdf(z_scores_time["task2"]), 2),
        "task3": round(100*norm.cdf(z_scores_time["task3"]), 2),
        "task4": round(100*norm.cdf(z_scores_time["task4"]), 2),
    }
    return time_on_task_raw, time_on_task_std

def calculate_sum_score_satisfaction(users):
    """
    Calculate satisfaction scores for each task.
    For tasks 1-3 (and task 4 if applicable), compute a satisfaction score as the average of difficulty, satisfaction, and time rating.
    Returns raw satisfaction statistics (mean, std, and target satisfaction) and standardized satisfaction scores.
    """
    spec_satisfaction = 4
    
    satisfaction_list = {
        "task1" : [],
        "task2" : [],
        "task3" : [],
        "task4" : [],
    }
    for user in users:
        satisfaction_score_task1 = (float(user.sum["task1"]["difficulty"]) + float(user.sum["task1"]["satisfaction"]) + float(user.sum["task1"]["time_rating"]))/3
        satisfaction_score_task2 = (float(user.sum["task2"]["difficulty"]) + float(user.sum["task2"]["satisfaction"]) + float(user.sum["task2"]["time_rating"]))/3
        satisfaction_score_task3 = (float(user.sum["task3"]["difficulty"]) + float(user.sum["task3"]["satisfaction"]) + float(user.sum["task3"]["time_rating"]))/3
        satisfaction_list["task1"].append(satisfaction_score_task1)
        satisfaction_list["task2"].append(satisfaction_score_task2)
        satisfaction_list["task3"].append(satisfaction_score_task3)
        if user.sum["first_person_experience"] == "Yes":
            satisfaction_score_task4 = (float(user.sum["task4"]["difficulty"]) + float(user.sum["task4"]["satisfaction"]) + float(user.sum["task4"]["time_rating"]))/3
            satisfaction_list["task4"].append(satisfaction_score_task4)
    
    # Calculate raw satisfaction statistics for each task: mean, standard deviation, and the target satisfaction value
    satisfaction_raw = {
        "task1" : [np.mean(satisfaction_list["task1"]), np.std(satisfaction_list["task1"]), spec_satisfaction],
        "task2" : [np.mean(satisfaction_list["task2"]), np.std(satisfaction_list["task2"]), spec_satisfaction],
        "task3" : [np.mean(satisfaction_list["task3"]), np.std(satisfaction_list["task3"]), spec_satisfaction],
        "task4" : [np.mean(satisfaction_list["task4"]), np.std(satisfaction_list["task4"]), spec_satisfaction],
    }    
    
    # Compute z-scores for satisfaction based on the deviation from the target
    z_scores_satisfaction = {
        "task1" : (satisfaction_raw["task1"][0] - satisfaction_raw["task1"][2]) / satisfaction_raw["task1"][1],
        "task2" : (satisfaction_raw["task2"][0] - satisfaction_raw["task2"][2]) / satisfaction_raw["task2"][1],
        "task3" : (satisfaction_raw["task3"][0] - satisfaction_raw["task3"][2]) / satisfaction_raw["task3"][1],
        "task4" : (satisfaction_raw["task4"][0] - satisfaction_raw["task4"][2]) / satisfaction_raw["task4"][1],
    }
    
    # Convert z-scores to standardized satisfaction scores using the normal cumulative distribution function
    satisfaction_std = {
        "task1": round(100*norm.cdf(z_scores_satisfaction["task1"]), 2),
        "task2": round(100*norm.cdf(z_scores_satisfaction["task2"]), 2),
        "task3": round(100*norm.cdf(z_scores_satisfaction["task3"]), 2),
        "task4": round(100*norm.cdf(z_scores_satisfaction["task4"]), 2),
    }
    return satisfaction_raw, satisfaction_std

def calculate_sum_score_error(users):
    """
    Calculate error scores for each task based on various error metrics.
    This function sums errors from different categories for each user and computes:
        - The mean error per category.
        - A scaling factor for each error type.
        - An "opportunity" score based on the scaled error.
    Finally, it calculates the standardized error score per task as a percentage.
    Returns both the raw error scores and the standardized error scores.
    """
    error_sum_count = {
        "Missing 2x Pinch Zoom": [0, 0],
        "Missing Pinch Move": [0, 0],
        "Missing Rotation": [0, 0],
        "Missing Ask Map Functionality": [0, 0],
        "Number of try asking a position": [0, 0],
        "Number of try to enter VR": [0, 0] 
    }
    for user in users:
        error_sum_count["Missing 2x Pinch Zoom"][0] += float(user.sum["errori"]["Missing 2x Pinch Zoom"])
        error_sum_count["Missing Pinch Move"][0] += float(user.sum["errori"]["Missing Pinch Move"])
        error_sum_count["Missing Rotation"][0] += float(user.sum["errori"]["Missing Rotation"])
        error_sum_count["Missing Ask Map Functionality"][0] += float(user.sum["errori"]["Missing Ask Map Functionality"])
        error_sum_count["Number of try asking a position"][0] += float(user.sum["errori"]["Number of try asking a position"])
        if user.sum["first_person_experience"] == "Yes":
            error_sum_count["Number of try to enter VR"][0] += float(user.sum["errori"]["Number of try to enter VR"])
        
        error_sum_count["Missing 2x Pinch Zoom"][1] += 1
        error_sum_count["Missing Pinch Move"][1] += 1
        error_sum_count["Missing Rotation"][1] += 1
        error_sum_count["Missing Ask Map Functionality"][1] += 1
        error_sum_count["Number of try asking a position"][1] += 1
        if user.sum["first_person_experience"] == "Yes":
            error_sum_count["Number of try to enter VR"][1] += 1
            
    # Compute the mean error for each category
    error_mean = {
        "Missing 2x Pinch Zoom": error_sum_count["Missing 2x Pinch Zoom"][0]/error_sum_count["Missing 2x Pinch Zoom"][1],
        "Missing Pinch Move": error_sum_count["Missing Pinch Move"][0]/error_sum_count["Missing Pinch Move"][1],
        "Missing Rotation": error_sum_count["Missing Rotation"][0]/error_sum_count["Missing Rotation"][1],
        "Missing Ask Map Functionality": error_sum_count["Missing Ask Map Functionality"][0]/error_sum_count["Missing Ask Map Functionality"][1],
        "Number of try asking a position": error_sum_count["Number of try asking a position"][0]/error_sum_count["Number of try asking a position"][1],
        "Number of try to enter VR": error_sum_count["Number of try to enter VR"][0]/error_sum_count["Number of try to enter VR"][1] 
    }
    # Define scaling factors for each error type
    scale_error = {
        "Missing 2x Pinch Zoom": 1,
        "Missing Pinch Move": error_mean["Missing 2x Pinch Zoom"]/error_mean["Missing Pinch Move"],
        "Missing Rotation": error_mean["Missing Pinch Move"]/error_mean["Missing Rotation"],
        "Missing Ask Map Functionality": 1,
        "Number of try asking a position": error_mean["Missing Ask Map Functionality"]/error_mean["Number of try asking a position"],
        "Number of try to enter VR":  error_mean["Number of try asking a position"]/error_mean["Number of try to enter VR"]
    }
    
    # Map the scaled error value to an opportunity score between 0 and 4
    def opportunity_mapping(error, scale):
        value_to_check = error*scale
        if value_to_check == 0:
            return 0
        elif value_to_check <= 3:
            return 1
        elif value_to_check <= 6:
            return 2
        elif value_to_check <= 9:
            return 3
        else:
            return 4
        
    # Initialize raw error scores for each task with the maximum possible error score
    error_raw = {
        "task1": [0, 4*len(users)],
        "task2": [0, 12*len(users)],
        "task3": [0, 4*len(users)],
        "task4": [0, 4*len(users)],
    }
    
    # Accumulate opportunity scores for each task based on the user's error counts
    for user in users:
        error_raw["task1"][0] += opportunity_mapping(float(user.sum["errori"]["Missing Ask Map Functionality"]), scale_error["Missing Ask Map Functionality"])
        error_raw["task2"][0] += opportunity_mapping(float(user.sum["errori"]["Missing 2x Pinch Zoom"]), scale_error["Missing 2x Pinch Zoom"])
        error_raw["task2"][0] += opportunity_mapping(float(user.sum["errori"]["Missing Pinch Move"]), scale_error["Missing Pinch Move"])
        error_raw["task2"][0] += opportunity_mapping(float(user.sum["errori"]["Missing Rotation"]), scale_error["Missing Rotation"])
        error_raw["task3"][0] += opportunity_mapping(float(user.sum["errori"]["Number of try asking a position"]), scale_error["Number of try asking a position"])
        if user.sum["first_person_experience"] == "Yes":
            error_raw["task4"][0] += opportunity_mapping(float(user.sum["errori"]["Number of try to enter VR"]), scale_error["Number of try to enter VR"])
    
    # Compute the standardized error score for each task as a percentage
    error_std = {
        "task1": round(100*(error_raw["task1"][1] - error_raw["task1"][0]) / error_raw["task1"][1], 2),
        "task2": round(100*(error_raw["task2"][1] - error_raw["task2"][0]) / error_raw["task2"][1], 2),
        "task3": round(100*(error_raw["task3"][1] - error_raw["task3"][0]) / error_raw["task3"][1], 2),
        "task4": round(100*(error_raw["task4"][1] - error_raw["task4"][0]) / error_raw["task4"][1], 2),
    }
    return error_raw, error_std

def calculate_sum_score(users):
    """
    Aggregate scores from completion, time-on-task, satisfaction, and error metrics into a single SUM score per task,
    and compute an overall SUM score across all tasks.
    Returns all intermediate raw and standardized scores, as well as the aggregated task scores and overall score.
    """
    complation_raw, complation_std = calculate_sum_score_complation(users)
    time_on_task_raw, time_on_task_std = calculate_sum_score_time_on_task(users)
    satisfaction_raw, satisfaction_std = calculate_sum_score_satisfaction(users)
    error_raw, error_std = calculate_sum_score_error(users)
    
    # Compute the SUM score per task by averaging the standardized scores of all metrics
    sum_result_task = {
        "task1": round((complation_std["task1"] + time_on_task_std["task1"] + satisfaction_std["task1"] + error_std["task1"]) / 4, 2),
        "task2": round((complation_std["task2"] + time_on_task_std["task2"] + satisfaction_std["task2"] + error_std["task2"]) / 4, 2),
        "task3": round((complation_std["task3"] + time_on_task_std["task3"] + satisfaction_std["task3"] + error_std["task3"]) / 4, 2),
        "task4": round((complation_std["task4"] + time_on_task_std["task4"] + satisfaction_std["task4"] + error_std["task4"]) / 4, 2),
    }
    
    # Compute the overall SUM score as the average of the task SUM scores
    sum_result = round((sum_result_task["task1"] + sum_result_task["task2"] + sum_result_task["task3"] + sum_result_task["task4"]) / 4, 2)
    return complation_raw, complation_std, time_on_task_raw, time_on_task_std, satisfaction_raw, satisfaction_std, error_raw, error_std, sum_result_task, sum_result

def print_scores(users, title):
    """
    Calculate various scores (SUS, NASA-TLX, SUM score) and print them.
    The printing lines are commented out; the function ultimately calls plot_nasa_tlx_spider
    with the mean dimension scores and a lowercased title.
    """
    _, sus_score = calculate_sus_scores(users)
    dimension_scores_mean_per_task, r_score, w_score = calculate_nasa_tlx(users)   
    complation_raw, complation_std, time_on_task_raw, time_on_task_std, satisfaction_raw, satisfaction_std, error_raw, error_std, sum_result_task, sum_result = calculate_sum_score(users)
    print(title.upper())
    print("SUS SCORE")
    print(sus_score)
    print()
    print()
    print("NASA-TLX RESULTS")
    print("DIMENSION SCORES MEAN PER TASK")
    print(json.dumps(dimension_scores_mean_per_task, indent=4))
    print()
    print("RAW SCORES PER TASK")
    print(r_score)
    print()
    print("WEIGHTED SCORES PER TASK")
    print(w_score)
    print()
    print()
    
    print("COMPLATION RAW/STD")
    print(json.dumps(complation_raw, indent=4))
    print(json.dumps(complation_std, indent=4))
    print()
    
    print("TIME-ON-TASK RAW/STD")
    print(json.dumps(time_on_task_raw, indent=4))
    print(json.dumps(time_on_task_std, indent=4))
    print()
    
    print("SATISFACTION RAW/STD")
    print(json.dumps(satisfaction_raw, indent=4))
    print(json.dumps(satisfaction_std, indent=4))
    print()

    print("ERROR RAW/STD")
    print(json.dumps(error_raw, indent=4))
    print(json.dumps(error_std, indent=4))
    print()

    print("SUM SCORE PER TASK")
    print(json.dumps(sum_result_task, indent=4))
    print()
    
    print("SUM SCORE")
    print(json.dumps(sum_result, indent=4))
    print()
    
    plot_nasa_tlx_spider(dimension_scores_mean_per_task, title.lower())

if __name__ == "__main__":
    # Read user data from an Excel file and generate statistical plots.
    users = leggi_dati_excel("./answer.xlsx")    
    plot_statistics(users)
    
    inexperienced_users = [user for user in users if user.vr_experience == "1" or user.vr_experience == "2"]
    average_users = [user for user in users if user.vr_experience == "3" or user.vr_experience == "4"]
    experienced_users = [user for user in users if user.vr_experience == "5" or user.vr_experience == "6"]
    print_scores(users, "All Users")
    print_scores(inexperienced_users, "Inexperienced Users")
    print_scores(average_users, "Average Users")
    print_scores(experienced_users, "Experienced Users")
