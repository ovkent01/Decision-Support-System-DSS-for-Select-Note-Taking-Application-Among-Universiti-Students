import pandas as pd
import numpy as np
from scipy.stats import gmean

def calculate_ahp_weights(file_path):
    # 1. read data
    df = pd.read_csv(file_path)

    # 2. 定义准则顺序 (必须与你 home.py 中的顺序完全一致) define criteria(must same arrangement with home.py)
    criteria = [
        "Ease of Use",
        "Functionality",
        "Cross-Device Sync",
        "Cost",
        "Storage & Security"
    ]
    
    # 建立名称映射 (处理 CSV 中可能的大小写不一致, 如 'Ease of use')
    # make all word same, prevent error
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

    # 3. 定义 10 组对比题目对应的列索引 (基于对你 CSV 的分析)
    # 每一组是 (Winner_Column_String, Intensity_Column_String) 的包含关键字
    # 我们通过遍历找到对应的列
    q_cols = [c for c in df.columns if "Which is more important" in c]
    i_cols = [c for c in df.columns if "how much more important" in c]

    # 手动定义题目对应的准则对索引 (A_index, B_index)
    # 顺序对应 Q1 到 Q10
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

    # 4. 构建每个受访者的矩阵
    num_respondents = len(df)
    all_matrices = np.zeros((num_respondents, n, n))

    for r in range(num_respondents):
        mat = np.eye(n) # 初始化单位矩阵
        row = df.iloc[r]
        
        for q_idx, (idx_a, idx_b) in enumerate(pairs):
            winner_raw = str(row[q_cols[q_idx]]).strip()
            intensity = float(row[i_cols[q_idx]])
            
            # 映射标准名称
            winner_clean = name_map.get(winner_raw)
            
            if winner_clean:
                winner_idx = criteria_idx[winner_clean]
                
                # 确定输家
                loser_idx = idx_b if winner_idx == idx_a else idx_a
                
                # 填入矩阵
                mat[winner_idx, loser_idx] = intensity
                mat[loser_idx, winner_idx] = 1.0 / intensity
        
        all_matrices[r] = mat

    # 5. 群决策聚合：计算所有矩阵的几何平均值 (Consensus Matrix)
    consensus_matrix = gmean(all_matrices, axis=0)

    # 6. 计算权重 (特征向量法)
    eigvals, eigvecs = np.linalg.eig(consensus_matrix)
    max_idx = np.argmax(np.real(eigvals))
    weights = np.real(eigvecs[:, max_idx])
    weights = weights / weights.sum() # 归一化

    # 返回字典格式 return dictionary
    return dict(zip(criteria, weights))

if __name__ == "__main__":
    # test run
    file = 'Note-Taking Application Selection (Responses) - Form responses 1.csv'
    weights = calculate_ahp_weights(file)
    print("--- 计算出的 AHP 权重 ---")
    for k, v in weights.items():
        print(f"{k}: {v:.4f}")