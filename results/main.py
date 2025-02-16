import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def plot_nasa_tlx_spider(dimension_scores_mean_task):
    """
    Crea uno spider chart (radar chart) per ciascun task.
    - Le dimensioni (assi) sono le chiavi del dizionario: mental_demand, physical_demand, ecc.
    - Per ogni task (indice nelle liste) viene creato un grafico a radar.
    """    
    key_mapping = {
        "mental_demand": "Mental Demand",
        "physical_demand": "Physical Demand",
        "temporal_demand": "Temporal Demand",
        "performance": "Performance",
        "effort": "Effort",
        "frustration": "Frustration",
    }
    
    task_names = [
        "Task 1: Introduction and Initial Interaction", 
        "Task 2: VR/MR Tutorial", 
        "Task 3: Map Interaction For Information Retrieval", 
        "Task 4: VR Navigation"]
    
    dimensions = ['mental_demand', 'physical_demand', 'temporal_demand', 'performance', 'effort', 'frustration']
    dimensions_label = [key_mapping[dimension] for dimension in dimensions]
    num_tasks = len(dimension_scores_mean_task[dimensions[0]])
    
    # Calcolo del range massimo per l'asse radiale
    max_val = max(max(dimension_scores_mean_task[dim]) for dim in dimensions)
    max_range = max_val * 1.1
    
    # Creazione della figura con subplots (layout 2x2)
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'polar'}],
               [{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=task_names
    )
    
    
    row_col = [(1, 1), (1, 2), (2, 1), (2, 2)]
    
    for i in range(num_tasks):
        # Estrae i valori per ciascuna dimensione per il task i-esimo
        values = [dimension_scores_mean_task[dim][i] for dim in dimensions]
        # Aggiunge il primo valore alla fine per chiudere il poligono
        values.append(values[0])
        # Crea una lista di etichette per gli assi (aggiungendo la prima in coda)
        labels = dimensions_label + [dimensions_label[0]]
        
        r, c = row_col[i]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=task_names[i]
        ), row=r, col=c)
    
    fig.update_layout(
        title="Nasa TLX results",
        showlegend=False,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_range]
            )
        )
    )    
    fig.show()
    
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

def sum(users):
    pass

if __name__ == "__main__":
    users = leggi_dati_excel("./risposte.xlsx")
    
    sus_results, sus_mean = calculate_sus_scores(users)
    dimension_scores_mean_per_task, r_score, w_score = calculate_nasa_tlx(users)   
    
    print("SUS Score:", sus_mean)
    print()
    print("Nasa TLX results:")
    print("Dimension Scores Mean per task: ", json.dumps(dimension_scores_mean_per_task, indent=4))
    print("Raw Scores per task:", r_score)
    print("Weighted Scores per task:", w_score)
    print()
    
    plot_nasa_tlx_spider(dimension_scores_mean_per_task)