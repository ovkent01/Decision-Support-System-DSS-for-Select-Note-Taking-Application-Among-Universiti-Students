import pandas as pd
import numpy as np
from scipy.stats import gmean

def calculate_ahp_weights(file_path):
    # 1. Read CSV
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Successfully read file, total {len(df)} rows.")
    except Exception as e:
        print(f"❌ Read error: {e}")
        return {}

    # 2. Define criteria (Standardized to match home.py)
    criteria = [
        "Ease of Use",          # Index 0
        "Functionality",        # Index 1
        "Cross-Device Sync",    # Index 2
        "Cost",                 # Index 3
        "Storage & Security"    # Index 4
    ]
    n = len(criteria)
    
    # 3. Define the comparison combinations for each question
    # Based on CSV data structure, the comparison relationships for the 10 questions are as follows
    # Format: (Question_Number, Index_A, Index_B)
    # Example: Q1 corresponds to CSV columns 7 & 8, comparing criteria[0] and criteria[1]
    question_map = [
        (0, 0, 1), # Q1: Ease vs Functionality
        (1, 0, 2), # Q2: Ease vs Sync
        (2, 0, 3), # Q3: Ease vs Cost
        (3, 0, 4), # Q4: Ease vs Storage
        (4, 1, 2), # Q5: Functionality vs Sync
        (5, 1, 3), # Q6: Functionality vs Cost
        (6, 1, 4), # Q7: Functionality vs Storage
        (7, 2, 3), # Q8: Sync vs Cost
        (8, 2, 4), # Q9: Sync vs Storage
        (9, 3, 4)  # Q10: Cost vs Storage
    ]

    # Initialize a dictionary to store all scores for each pair
    # key: (row, col), value: list of scores
    pair_scores = {}
    for i in range(n):
        for j in range(i+1, n):
            pair_scores[(i, j)] = []

    # 4. Iterate through each respondent
    for index, row in df.iterrows():
        # Iterate through 10 questions
        for q_idx, idx_a, idx_b in question_map:
            # Calculate column index in CSV
            # Q1 is at Col 7 (Choice) and Col 8 (Score) (Index starts at 0)
            # Q2 is at Col 9 (Choice) and Col 10 (Score)... and so on
            col_choice = 7 + q_idx * 2
            col_score = 8 + q_idx * 2
            
            choice = str(row.iloc[col_choice]).strip()
            score = float(row.iloc[col_score])
            
            name_a = criteria[idx_a]
            name_b = criteria[idx_b]
            
            # Application Logic:
            # If A is chosen, Matrix(A, B) = score
            # If B is chosen, Matrix(A, B) = 1 / score
            # Using .lower() for case-insensitive comparison (e.g., "Ease of use" vs "Ease of Use")
            if choice.lower() == name_a.lower():
                val = score
            elif choice.lower() == name_b.lower():
                val = 1.0 / score
            else:
                # Error handling: if unexpected value, default to 1 (Equal importance)
                val = 1.0 
            
            pair_scores[(idx_a, idx_b)].append(val)

    # 5. Construct Aggregated Matrix (Using Geometric Mean)
    agg_matrix = np.ones((n, n))
    
    for (i, j), scores in pair_scores.items():
        if scores:
            geo_mean_val = gmean(scores) # Calculate geometric mean for this pair
            agg_matrix[i, j] = geo_mean_val
            agg_matrix[j, i] = 1.0 / geo_mean_val

    # 6. Calculate CR (Consistency Ratio)
    eig_vals, eig_vecs = np.linalg.eig(agg_matrix)
    lambda_max = np.max(eig_vals).real
    
    ci = (lambda_max - n) / (n - 1)
    ri_dict = {3: 0.58, 4: 0.90, 5: 1.12} # RI Standard Table
    ri = ri_dict.get(n, 1.12)
    cr = ci / ri
    
    # 7. Calculate Weights
    weights = eig_vecs[:, np.argmax(eig_vals)].real
    weights = weights / weights.sum()

    # --- Output Results (Console Log) ---
    print("-" * 30)
    print("📊 AHP Calculation Results")
    print("-" * 30)
    print(f"Consistency Ratio (CR): {cr:.4f}")
    if cr < 0.1:
        print("✅ Result Valid (CR < 0.1)")
    else:
        print("⚠️ Consistency Insufficient (CR >= 0.1)")
    
    print("\nCriteria Weights:")
    for name, w in zip(criteria, weights):
        print(f"{name:20s}: {w:.4f}")
        
    # Return dictionary for use in home.py
    return dict(zip(criteria, weights))

if __name__ == "__main__":
    # Test run
    file_path = 'Note-Taking Application Selection (Responses) - Form responses 1.csv'
    calculate_ahp_weights(file_path)