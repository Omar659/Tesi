import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px 
import numpy as np
from scipy.stats import norm
import plotly.io as pio

pio.kaleido.scope.default_format = "pdf"
pio.kaleido.scope.default_width = 1200
pio.kaleido.scope.default_height = 800
pio.kaleido.scope.default_scale = 1.5  # Aumenta la risoluzione

def build_comparison_wins(prefix, row):
    """
    Costruisce un dizionario che mappa le 6 dimensioni (usando le stesse etichette di 'ratings')
    al numero di vittorie ottenute, a partire dai 15 item di confronto.
    Il prefisso rappresenta la parte comune dell'intestazione delle domande di comparison,
    ad esempio "Task 1: Introduction & Initial Interaction".
    """
    # Mappa per convertire le risposte (con etichette in formato "Mental Demand", etc.)
    # nelle stesse chiavi usate in "ratings"
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

def plot_statistics(users):
    """
    Creates statistical plots:
    - A pie chart for the distribution of users by gender.
    - A pie chart for the distribution of users by qualification/profession.
    - A bar chart for the VR Experience level, with custom colors:
      Levels 1-2 as "Inexperienced", 3-4 as "Average", and 5-6 as "Experienced".
      Each bar shows the VR Experience level, user category, Number of Users, and percentage.
    """
    # Build a DataFrame with the relevant information
    data = {
        'gender': [user.gender for user in users],
        'qualification': [user.qualification for user in users],
        'vr_experience': [user.vr_experience for user in users]
    }
    df = pd.DataFrame(data)
    
    # Pie chart for gender distribution
    fig_gender = px.pie(df, names='gender', title='Distribution of Users by Gender')
    fig_gender.update_traces(textinfo='label+value+percent')
    fig_gender.update_layout(
        title_font=dict(size=45), 
        legend=dict(
            font=dict(size=28),  
            title_font=dict(size=30)  
        )
    )
    fig_gender.show()
    
    # Pie chart for qualification/profession distribution
    fig_qual = px.pie(df, names='qualification', title='Distribution of Users by Qualification/Profession')
    fig_qual.update_traces(textinfo='label+value+percent')
    fig_qual.update_layout(
        title_font=dict(size=45),
        legend=dict(
            font=dict(size=28),
            title_font=dict(size=30) 
        )
    )
    fig_qual.show()
    
    # Bar chart for VR Experience level
    # Count users per VR level
    vr_counts = df['vr_experience'].value_counts().reset_index()
    vr_counts.columns = ['vr_experience', 'count']
    
    # Convert vr_experience to numeric and sort in ascending order
    vr_counts['vr_experience'] = pd.to_numeric(vr_counts['vr_experience'], errors='coerce')
    vr_counts = vr_counts.sort_values('vr_experience')
    
    # Define groups based on VR levels with new labels
    def get_group(x):
        if x in [1, 2]:
            return 'Inexperienced'
        elif x in [3, 4]:
            return 'Average'
        elif x in [5, 6]:
            return 'Experienced'
        else:
            return 'Other'
    
    vr_counts['group'] = vr_counts['vr_experience'].apply(get_group)
    
    # Calculate percentage for each VR level
    total_users = df.shape[0]
    vr_counts['percentage'] = (vr_counts['count'] / total_users * 100).round(2)
    
    # Create a text column with more explicit labels
    vr_counts['text'] = (
        "XR Experience: " + vr_counts['vr_experience'].astype(str) + "<br>" +
        "User Category: " + vr_counts['group'] + "<br>" +
        "Number of Users: " + vr_counts['count'].astype(str) + "<br>" +
        "Percentage: " + vr_counts['percentage'].astype(str) + "%"
    )
    
    # Define a custom color mapping using softer colors (from the Plotly default palette)
    color_map = {
        'Inexperienced': '#1f77b4',
        'Average': '#ff7f0e',
        'Experienced': '#2ca02c',
        'Other': '#7f7f7f'
    }
    
    fig_vr = px.bar(
        vr_counts,
        x='vr_experience',
        y='count',
        color='group',
        color_discrete_map=color_map,
        labels={'vr_experience': 'XR Experience', 'count': 'Number of Users', 'group': 'User Category'},
        title='XR Experience Level',
        text=vr_counts['text']
    )
    fig_vr.update_traces(textposition='inside')
    fig_vr.update_layout(
        title_font=dict(size=45),
        legend=dict(
            font=dict(size=28),
            title_font=dict(size=30)
        ),
        # Eventuale aggiunta per ingrandire le etichette degli assi
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=14))
    )
    fig_vr.show()


def plot_nasa_tlx_spider(dimension_scores_mean_task, user_name):
    """
    Crea un radar chart avanzato con:
    - Scala logaritmica personalizzata (range 4-100)
    - 10 cerchi concentrici con etichette significative
    - Legenda orizzontale sopra il grafico
    - Marker grandi con bordi contrastanti
    - Colori ad alto contrasto
    - Anti-overlap per valori identici
    """
    
    import math
    import plotly.graph_objects as go
    
    # =========================================================================
    # 1. CONFIGURAZIONE INIZIALE E MAPPATURA DATI
    # =========================================================================
    
    # Mappatura delle dimensioni per le etichette
    KEY_MAPPING = {
        "mental_demand": "MD",
        "physical_demand": "PD",
        "temporal_demand": "TD",
        "performance": "P",
        "effort": "E",
        "frustration": "F",
    }
    
    # Nomi dei task con formattazione HTML per ritorni a capo
    TASK_NAMES = [
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4"
    ]
    
    # Configurazione colori e marker
    COLORS = [
        'rgba(0, 92, 230, 0.9)',    # Blu elettrico
        'rgba(255, 0, 0, 0.9)',      # Rosso acceso
        'rgba(0, 163, 0, 0.9)',      # Verde neon
        'rgba(163, 0, 163, 0.9)'     # Viola intenso
    ]
    MARKERS = ['circle', 'square', 'diamond', 'x']
    
    # =========================================================================
    # 2. FUNZIONI DI SUPPORTO
    # =========================================================================
        
    def adjust_overlaps(values):
        """
        Aggiunge piccoli offset ai valori identici per prevenire sovrapposizioni
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
    
    # =========================================================================
    # 3. PREPARAZIONE DATI
    # =========================================================================
    
    # Lista delle dimensioni da visualizzare
    dimensions = list(KEY_MAPPING.keys())
    
    # Applica la trasformazione logaritmica a tutti i valori
    log_normalized = {
        dim: [x for x in dimension_scores_mean_task[dim]] 
        for dim in dimensions
    }
    
    # Applica correzione anti-overlap
    adjusted_values = {dim: adjust_overlaps(log_normalized[dim]) for dim in dimensions}
    
    
    # =========================================================================
    # 4. COSTRUZIONE GRAFICO
    # =========================================================================
    
    fig = go.Figure()
    
    # Aggiungi ogni task come traccia separata
    for i in range(4):
        # Estrai e formatta i valori
        values = [adjusted_values[dim][i] for dim in dimensions]
        values += [values[0]]  # Chiudi il poligono
        
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
            fillcolor=COLORS[i].replace('0.9)', '0.2)'),  # Riempimento trasparente
            mode='lines+markers'
        ))
    
    # =========================================================================
    # 5. FORMATTAZIONE FINALE
    # =========================================================================
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 60],
                # tickvals=tick_positions,
                # ticktext=[f"{x}" for x in LOG_TICKS],
                tickfont=dict(size=25, color='#333333'),
                gridcolor='rgba(100, 100, 100, 0.2)',
                linecolor='gray',
                linewidth=2,
                nticks=0  # Disabilita ticks automatici
            ),
            angularaxis=dict(
                tickfont=dict(size=35, color='#333333'),
                linecolor='gray',
                gridcolor='rgba(100, 100, 100, 0.1)',
                rotation=90  # Orientamento etichette
            ),
            bgcolor='white'  # Sfondo trasparente
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,  # Posizione sopra il grafico
            xanchor="center",
            x=0.5,
            font=dict(size=30, color='#333333'),
            itemwidth=40,
            itemsizing='constant',
            bordercolor='gray',
            borderwidth=1
        ),
        margin=dict(t=150, b=80),  # Spazio per legenda
        width=1000,
        height=700,
        paper_bgcolor='white'
    )
    
    fig.write_image(f"./nasa_tlx_{user_name}.svg")
    # fig.show()
    
def leggi_dati_excel(file_path):
    df = pd.read_excel(file_path)
    users = []
    for _, row in df.iterrows():
        users.append(User(row))
    return users

class User:
    def __init__(self, row):
        # Informazioni anagrafiche
        self.name = str(row["Name"])
        self.gender = str(row["Gender"])
        self.age = str(row["Age"]) if pd.notna(row["Age"]) else None
        self.vr_experience = str(row["VR Experience Level "])
        self.qualification = str(row["Academic/Professional Qualification"])
        
        # Questionario SUM (già definito in precedenza)
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
        
        # Questionario SUS
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
        
        # Questionario NASA TLX: per ogni task, oltre ai ratings, calcoliamo il dizionario
        # dei "vincitori" aggregati usando le stesse etichette di ratings
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
    sus_scores = []
    for user in users:
        total_score_positive = 0
        total_score_negative = 0
        for i in range(1, 11):
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
            if i%2 == 0:
                total_score_negative -= score
            else:
                total_score_positive += score
            total_score = total_score_negative + total_score_positive
        
        total_score += 20
        total_score *= 2.5
        sus_scores.append({"name":user.name, "sus_score": total_score})    
    sus_scores_value = [sus_score["sus_score"] for sus_score in sus_scores]
    return sus_scores, round(sum(sus_scores_value) / len(sus_scores_value), 2)

def calculate_nasa_tlx(users, num_task=4):
    """
    Calcola per ogni utente:
    1. Punteggio NASA TLX pesato per ogni task
    2. Media non pesata per ogni dimensione di carico su tutti i task
    """
    results = []
    tasks = ["task" + str(i+1) for i in range(4)]
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
        dimension_scores_task_mean_weighted = [0]*num_task
        dimension_scores_task_mean = [0]*num_task
        for i, task_key in enumerate(tasks):
            
            if task_key == "task4" and user.nasa_tlx["nasa_vr_experience"] == "No":
                continue
            
            ratings = user.nasa_tlx[task_key]["ratings"]
            comparison = user.nasa_tlx[task_key]["comparison_wins"]
            task_dimension_sum_weighted = 0
            task_dimension_sum = 0
            for dimension in dimensions:
                task_dimension_sum_weighted += float(ratings[dimension])*10*float(comparison[dimension])
                task_dimension_sum += float(ratings[dimension])*10
                dimension_scores_task[dimension][i] += float(ratings[dimension])*10
                dimension_scores_counts_task[dimension][i] += 1
            dimension_scores_task_mean_weighted[i] = round(task_dimension_sum_weighted/15, 2)
            dimension_scores_task_mean[i] = round(task_dimension_sum/6, 2)
            
        dimension_scores_task_weighted_list.append(dimension_scores_task_mean_weighted)
        dimension_scores_task_list.append(dimension_scores_task_mean)     
    
    dimension_scores_mean_task = {dim: [0]*num_task for dim in dimension_scores_task.keys()}
    for dimension, tasks_value in dimension_scores_task.items():
        for i, task_value in enumerate(tasks_value):
            if dimension_scores_counts_task[dimension][i] == 0:
                continue
            dimension_scores_mean_task[dimension][i] = round(task_value/dimension_scores_counts_task[dimension][i], 2)
    
    w_score = [0]*num_task
    w_score_counter = [0]*num_task
    for user_idx, weighted_scores in enumerate(dimension_scores_task_weighted_list):
        for i, weighted_task in enumerate(weighted_scores):
            if i == 3 and users[user_idx].nasa_tlx["nasa_vr_experience"] == "No":
                continue
            w_score[i] += weighted_task
            w_score_counter[i] += 1
    w_score = [round(w_score_i/w_score_counter_i, 2) for w_score_i, w_score_counter_i in zip(w_score, w_score_counter)]
    
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
    spec_satisfaction = 4
    spec_time = [0, 0, 0, 0]
    spec_time_percentage = 95
    
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
        satisfaction_score_task1 = (float(user.sum["task1"]["difficulty"]) + float(user.sum["task1"]["satisfaction"]) + float(user.sum["task1"]["time_rating"]))/3
        satisfaction_score_task2 = (float(user.sum["task2"]["difficulty"]) + float(user.sum["task2"]["satisfaction"]) + float(user.sum["task2"]["time_rating"]))/3
        satisfaction_score_task3 = (float(user.sum["task3"]["difficulty"]) + float(user.sum["task3"]["satisfaction"]) + float(user.sum["task3"]["time_rating"]))/3
        if satisfaction_score_task1 >= spec_satisfaction:
            time_on_task_list["task1_spec"].append(float(user.sum["task1"]["time"]))
        if satisfaction_score_task2 >= spec_satisfaction:
            time_on_task_list["task2_spec"].append(float(user.sum["task2"]["time"]))
        if satisfaction_score_task3 >= spec_satisfaction:
            time_on_task_list["task3_spec"].append(float(user.sum["task3"]["time"]))
        time_on_task_list["task1"].append(float(user.sum["task1"]["time"]))
        time_on_task_list["task2"].append(float(user.sum["task2"]["time"]))
        time_on_task_list["task3"].append(float(user.sum["task3"]["time"]))
        if user.sum["first_person_experience"] == "Yes":
            time_on_task_list["task4"].append(float(user.sum["task4"]["time"]))
            satisfaction_score_task4 = (float(user.sum["task4"]["difficulty"]) + float(user.sum["task4"]["satisfaction"]) + float(user.sum["task4"]["time_rating"]))/3
            if satisfaction_score_task4 >= spec_satisfaction:
                time_on_task_list["task4_spec"].append(float(user.sum["task4"]["time"]))

    spec_time[0] = np.percentile(time_on_task_list["task1_spec"], spec_time_percentage)   
    spec_time[1] = np.percentile(time_on_task_list["task2_spec"], spec_time_percentage)   
    spec_time[2] = np.percentile(time_on_task_list["task3_spec"], spec_time_percentage)   
    spec_time[3] = np.percentile(time_on_task_list["task4_spec"], spec_time_percentage)   
    
    time_on_task_raw = {
        "task1" : [np.mean(time_on_task_list["task1"]), np.std(time_on_task_list["task1"]), spec_time[0]],
        "task2" : [np.mean(time_on_task_list["task2"]), np.std(time_on_task_list["task2"]), spec_time[1]],
        "task3" : [np.mean(time_on_task_list["task3"]), np.std(time_on_task_list["task3"]), spec_time[2]],
        "task4" : [np.mean(time_on_task_list["task4"]), np.std(time_on_task_list["task4"]), spec_time[3]],
    }
    
    z_scores_time = {
        "task1" : -(time_on_task_raw["task1"][0] - time_on_task_raw["task1"][2]) / time_on_task_raw["task1"][1],
        "task2" : -(time_on_task_raw["task2"][0] - time_on_task_raw["task2"][2]) / time_on_task_raw["task2"][1],
        "task3" : -(time_on_task_raw["task3"][0] - time_on_task_raw["task3"][2]) / time_on_task_raw["task3"][1],
        "task4" : -(time_on_task_raw["task4"][0] - time_on_task_raw["task4"][2]) / time_on_task_raw["task4"][1],
    }
    
    time_on_task_std = {
        "task1": round(100*norm.cdf(z_scores_time["task1"]), 2),
        "task2": round(100*norm.cdf(z_scores_time["task2"]), 2),
        "task3": round(100*norm.cdf(z_scores_time["task3"]), 2),
        "task4": round(100*norm.cdf(z_scores_time["task4"]), 2),
    }
    return time_on_task_raw, time_on_task_std

def calculate_sum_score_satisfaction(users):    
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
    
    satisfaction_raw = {
        "task1" : [np.mean(satisfaction_list["task1"]), np.std(satisfaction_list["task1"]), spec_satisfaction],
        "task2" : [np.mean(satisfaction_list["task2"]), np.std(satisfaction_list["task2"]), spec_satisfaction],
        "task3" : [np.mean(satisfaction_list["task3"]), np.std(satisfaction_list["task3"]), spec_satisfaction],
        "task4" : [np.mean(satisfaction_list["task4"]), np.std(satisfaction_list["task4"]), spec_satisfaction],
    }    
    
    z_scores_satisfaction = {
        "task1" : (satisfaction_raw["task1"][0] - satisfaction_raw["task1"][2]) / satisfaction_raw["task1"][1],
        "task2" : (satisfaction_raw["task2"][0] - satisfaction_raw["task2"][2]) / satisfaction_raw["task2"][1],
        "task3" : (satisfaction_raw["task3"][0] - satisfaction_raw["task3"][2]) / satisfaction_raw["task3"][1],
        "task4" : (satisfaction_raw["task4"][0] - satisfaction_raw["task4"][2]) / satisfaction_raw["task4"][1],
    }
    
    satisfaction_std = {
        "task1": round(100*norm.cdf(z_scores_satisfaction["task1"]), 2),
        "task2": round(100*norm.cdf(z_scores_satisfaction["task2"]), 2),
        "task3": round(100*norm.cdf(z_scores_satisfaction["task3"]), 2),
        "task4": round(100*norm.cdf(z_scores_satisfaction["task4"]), 2),
    }
    return satisfaction_raw, satisfaction_std

def calculate_sum_score_error(users):    
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
            
    error_mean = {
        "Missing 2x Pinch Zoom": error_sum_count["Missing 2x Pinch Zoom"][0]/error_sum_count["Missing 2x Pinch Zoom"][1],
        "Missing Pinch Move": error_sum_count["Missing Pinch Move"][0]/error_sum_count["Missing Pinch Move"][1],
        "Missing Rotation": error_sum_count["Missing Rotation"][0]/error_sum_count["Missing Rotation"][1],
        "Missing Ask Map Functionality": error_sum_count["Missing Ask Map Functionality"][0]/error_sum_count["Missing Ask Map Functionality"][1],
        "Number of try asking a position": error_sum_count["Number of try asking a position"][0]/error_sum_count["Number of try asking a position"][1],
        "Number of try to enter VR": error_sum_count["Number of try to enter VR"][0]/error_sum_count["Number of try to enter VR"][1] 
    }
    scale_error = {
        "Missing 2x Pinch Zoom": 1,
        "Missing Pinch Move": error_mean["Missing 2x Pinch Zoom"]/error_mean["Missing Pinch Move"],
        "Missing Rotation": error_mean["Missing Pinch Move"]/error_mean["Missing Rotation"],
        "Missing Ask Map Functionality": 1,
        "Number of try asking a position": error_mean["Missing Ask Map Functionality"]/error_mean["Number of try asking a position"],
        "Number of try to enter VR":  error_mean["Number of try asking a position"]/error_mean["Number of try to enter VR"]
    }
    
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
        
    error_raw = {
        "task1": [0, 4*len(users)],
        "task2": [0, 12*len(users)],
        "task3": [0, 4*len(users)],
        "task4": [0, 4*len(users)],
    }
    
    for user in users:
        error_raw["task1"][0] += opportunity_mapping(float(user.sum["errori"]["Missing Ask Map Functionality"]), scale_error["Missing Ask Map Functionality"])
        error_raw["task2"][0] += opportunity_mapping(float(user.sum["errori"]["Missing 2x Pinch Zoom"]), scale_error["Missing 2x Pinch Zoom"])
        error_raw["task2"][0] += opportunity_mapping(float(user.sum["errori"]["Missing Pinch Move"]), scale_error["Missing Pinch Move"])
        error_raw["task2"][0] += opportunity_mapping(float(user.sum["errori"]["Missing Rotation"]), scale_error["Missing Rotation"])
        error_raw["task3"][0] += opportunity_mapping(float(user.sum["errori"]["Number of try asking a position"]), scale_error["Number of try asking a position"])
        if user.sum["first_person_experience"] == "Yes":
            error_raw["task4"][0] += opportunity_mapping(float(user.sum["errori"]["Number of try to enter VR"]), scale_error["Number of try to enter VR"])
    
    
    error_std = {
        "task1": round(100*(error_raw["task1"][1] - error_raw["task1"][0]) / error_raw["task1"][1], 2),
        "task2": round(100*(error_raw["task2"][1] - error_raw["task2"][0]) / error_raw["task2"][1], 2),
        "task3": round(100*(error_raw["task3"][1] - error_raw["task3"][0]) / error_raw["task3"][1], 2),
        "task4": round(100*(error_raw["task4"][1] - error_raw["task4"][0]) / error_raw["task4"][1], 2),
    }
    return error_raw, error_std

def calculate_sum_score(users):    
    complation_raw, complation_std = calculate_sum_score_complation(users)
    time_on_task_raw, time_on_task_std = calculate_sum_score_time_on_task(users)
    satisfaction_raw, satisfaction_std = calculate_sum_score_satisfaction(users)
    error_raw, error_std = calculate_sum_score_error(users)
    
    sum_result_task = {
        "task1": round((complation_std["task1"] + time_on_task_std["task1"] + satisfaction_std["task1"] + error_std["task1"]) / 4, 2),
        "task2": round((complation_std["task2"] + time_on_task_std["task2"] + satisfaction_std["task2"] + error_std["task2"]) / 4, 2),
        "task3": round((complation_std["task3"] + time_on_task_std["task3"] + satisfaction_std["task3"] + error_std["task3"]) / 4, 2),
        "task4": round((complation_std["task4"] + time_on_task_std["task4"] + satisfaction_std["task4"] + error_std["task4"]) / 4, 2),
    }
    
    sum_result = round((sum_result_task["task1"] + sum_result_task["task2"] + sum_result_task["task3"] + sum_result_task["task4"]) / 4, 2)
    return complation_raw, complation_std, time_on_task_raw, time_on_task_std, satisfaction_raw, satisfaction_std, error_raw, error_std, sum_result_task, sum_result

def print_scores(users, title):
    _, sus_score = calculate_sus_scores(users)
    dimension_scores_mean_per_task, r_score, w_score = calculate_nasa_tlx(users)   
    complation_raw, complation_std, time_on_task_raw, time_on_task_std, satisfaction_raw, satisfaction_std, error_raw, error_std, sum_result_task, sum_result = calculate_sum_score(users)
    # print(title.upper())
    # print("SUS SCORE")
    # print(sus_score)
    # print()
    # print()
    # print("NASA-TLX RESULTS")
    # print("DIMENSION SCORES MEAN PER TASK")
    # print(json.dumps(dimension_scores_mean_per_task, indent=4))
    # print()
    # print("RAW SCORES PER TASK")
    # print(r_score)
    # print()
    # print("WEIGHTED SCORES PER TASK")
    # print(w_score)
    # print()
    # print()
    
    # print("COMPLATION RAW/STD")
    # print(json.dumps(complation_raw, indent=4))
    # print(json.dumps(complation_std, indent=4))
    # print()
    
    # print("TIME-ON-TASK RAW/STD")
    # print(json.dumps(time_on_task_raw, indent=4))
    # print(json.dumps(time_on_task_std, indent=4))
    # print()
    
    # print("SATISFACTION RAW/STD")
    # print(json.dumps(satisfaction_raw, indent=4))
    # print(json.dumps(satisfaction_std, indent=4))
    # print()

    # print("ERROR RAW/STD")
    # print(json.dumps(error_raw, indent=4))
    # print(json.dumps(error_std, indent=4))
    # print()

    # print("SUM SCORE PER TASK")
    # print(json.dumps(sum_result_task, indent=4))
    # print()
    
    # print("SUM SCORE")
    # print(json.dumps(sum_result, indent=4))
    # print()
    
    plot_nasa_tlx_spider(dimension_scores_mean_per_task, title.lower())

if __name__ == "__main__":
    users = leggi_dati_excel("./risposte.xlsx")    
    # plot_statistics(users)
    
    inexperienced_users = [user for user in users if user.vr_experience == "1" or user.vr_experience == "2"]
    average_users = [user for user in users if user.vr_experience == "3" or user.vr_experience == "4"]
    experienced_users = [user for user in users if user.vr_experience == "5" or user.vr_experience == "6"]
    print_scores(users, "All Users")
    print_scores(inexperienced_users, "Inexperienced Users")
    print_scores(average_users, "Average Users")
    print_scores(experienced_users, "Experienced Users")
