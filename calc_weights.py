import pandas as pd
import numpy as np
from scipy.stats import gmean

def calculate_ahp_weights(file_path):
    # 1. read data
    df = pd.read_csv(file_path)

    # 2. define criteria (must be the same arrangement as home.py)
    criteria = [
        "Ease of Use",
        "Functionality",
        "Cross-Device Sync",
        "Cost",
        "Storage & Security"
    ]

    # Standardize all words to prevent errors
    name_map = {
        "Ease of use": "Ease of Use",
        "Ease of Use": "Ease of Use",
        "Functionality": "Functionality",
        "Cross-Device Sync": "Cross-Device Sync",
        "Cost": "Cost",
        "Storage & Security": "Storage & Security"
    }
    
    n = len(criteria)
    criteria_idx = {c: i for i, c in enumerate(criteria)}

    # 3. Define column indices for the 10 comparison questions (based on your CSV analysis)
    # Each group searches for keywords (Winner_Column_String, Intensity_Column_String)
    # We iterate to find the corresponding columns
    q_cols = [c for c in df.columns if "Which is more important" in c]
    i_cols = [c for c in df.columns if "how much more important" in c]

    # Manually define the criteria pair indices (A_index, B_index) corresponding to the questions
    # The order corresponds to Q1 to Q10
    pairs = [
        (0, 1), # Q1: Ease vs Func
        (0, 2), # Q2: Ease vs Sync
        (0, 3), # Q3: Ease vs Cost
        (0, 4), # Q4: Ease vs Storage
        (1, 2), # Q5: Func vs Sync
        (1, 3), # Q6: Func vs Cost
        (1, 4), # Q7: Func vs Storage
        (2, 3), # Q8: Sync vs Cost
        (2, 4), # Q9: Sync vs Storage
        (3, 4)  # Q10: Cost vs Storage
    ]

    # 4. Construct the matrix for each respondent
    num_respondents = len(df)
    all_matrices = np.zeros((num_respondents, n, n))

    for r in range(num_respondents):
        mat = np.eye(n) # Initialize identity matrix
        row = df.iloc[r]
        
        for q_idx, (idx_a, idx_b) in enumerate(pairs):
            winner_raw = str(row[q_cols[q_idx]]).strip()
            intensity = float(row[i_cols[q_idx]])
            
            # Map to standard criteria name
            winner_clean = name_map.get(winner_raw)
            
            if winner_clean:
                winner_idx = criteria_idx[winner_clean]
                
                # Determine the loser index
                loser_idx = idx_b if winner_idx == idx_a else idx_a
                
                # Populate the matrix
                mat[winner_idx, loser_idx] = intensity
                mat[loser_idx, winner_idx] = 1.0 / intensity
        
        all_matrices[r] = mat

    # 5. Group Decision Aggregation: Calculate the geometric mean of all matrices (Consensus Matrix)
    consensus_matrix = gmean(all_matrices, axis=0)

    # 6. Calculate weights (Eigenvector Method)
    eigvals, eigvecs = np.linalg.eig(consensus_matrix)
    max_idx = np.argmax(np.real(eigvals))
    weights = np.real(eigvecs[:, max_idx])
    weights = weights / weights.sum() # Normalize

    # Return dictionary format
    return dict(zip(criteria, weights))

if __name__ == "__main__":
    # test run
    file = 'Note-Taking Application Selection (Responses) - Form responses 1.csv'
    weights = calculate_ahp_weights(file)
    print("--- Calculated AHP Weights ---")
    for k, v in weights.items():
        print(f"{k}: {v:.4f}")