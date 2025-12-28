import streamlit as st
import pandas as pd
import numpy as np
from calc_weights import calculate_ahp_weights

def render_home_page():
    st.title("Welcome to Note-Taking Application Selection DSS")
    st.markdown("""
    This system combines **Crowd Wisdom (AHP Survey)** with your **Personal Preferences**.
    
    The final recommendation is calculated by:
    $$ Final Weight = AHP Weight \\times Your Preference $$
    """)
    
    # --- 1. 定义基础数据 Define data---
    criteria = [
        "Ease of Use",
        "Functionality",
        "Cross-Device Sync",
        "Cost",
        "Storage & Security"
    ]

    alternatives = [
        "GoodNotes",
        "Notability",
        "Microsoft OneNote",
        "Flexcil",
        "Kilonote"
    ]

    # --- 2. 预先加载 AHP 权重 (作为基准) Preload AHP weight ---
    try:
        file_path = "Note-Taking Application Selection (Responses) - Form responses 1.csv"
        # 这里的 ahp_weights 是一个字典，例如 {'Cost': 0.14, 'Functionality': 0.26 ...}
        # ahp_weights is a dictionary
        ahp_weights = calculate_ahp_weights(file_path)
    except Exception as e:
        st.error(f"Error loading AHP data: {e}")
        st.stop()

    # --- 3. Sidebar: User input ---
    with st.sidebar:
        st.header("🎯 Customize Your Needs")
        st.info("The system uses Survey Data as a baseline. Adjust the sliders to influence the result based on your personal needs.")
        
        user_inputs = {}
        
        # show a explaination
        st.markdown("### Rate Importance (0-10)")
        
        for c in criteria:
            # 获取该准则的 AHP 权重，用于显示给用户参考（可选）
            base_w = ahp_weights.get(c, 0)
            
            # Create Sliders
            user_val = st.slider(
                f"{c}", 
                min_value=0, 
                max_value=10, 
                value=5, # 默认值为5 Default value = 5
                help=f"Survey Crowd Weight: {base_w:.1%}" # 鼠标悬停显示AHP参考值
            )
            user_inputs[c] = user_val

        calc_btn = st.button("Calculate Recommendation", type="primary")

    # --- 4. Core algorithm logic ---
    if calc_btn or True:
        
        # === Step A: Calculate Hybrid Weighting ===
        # Hybrid Weighting = AHP weight * user sliders' value
        raw_hybrid_weights = {}
        
        for c in criteria:
            w_ahp = ahp_weights.get(c, 0)       # 基准权重
            u_score = user_inputs.get(c, 0)     # 用户打分
            
            raw_hybrid_weights[c] = w_ahp * u_score
            
        # === Step B: Normalization ===
        # sum of all weight must be 1
        total_score = sum(raw_hybrid_weights.values())
        
        if total_score == 0:
            # 防止除以零（如果用户把所有滑块都拖到0）
            # precent user put all weight = 0 occur error
            final_weights = {k: 1/len(criteria) for k in criteria}
        else:
            final_weights = {k: v / total_score for k, v in raw_hybrid_weights.items()}
            
        # === Step C: Show weight change (visualisation) ===
        st.subheader("1. Weight Analysis: AHP vs. Final")
        
        # 构建一个对比表格方便画图
        comparison_data = []
        for c in criteria:
            comparison_data.append({
                "Criteria": c,
                "Source": "Survey Baseline (AHP)",
                "Weight": ahp_weights[c]
            })
            comparison_data.append({
                "Criteria": c,
                "Source": "Your Customized Weight",
                "Weight": final_weights[c]
            })
        
        df_chart = pd.DataFrame(comparison_data)
        
        # 使用 Altair 或 Streamlit 原生图表展示对比
        # 这里用简单的 bar_chart 分组显示可能不支持，我们直接分开显示或用 st.dataframe
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.markdown("**User Adjusted Weights (Final)**")
            st.dataframe(pd.DataFrame.from_dict(final_weights, orient='index', columns=['Weight']).style.format("{:.1%}"))
        with col_w2:
            st.markdown("**Difference from Crowd**")
            # 简单的条形图展示最终权重
            st.bar_chart(pd.Series(final_weights))

        # === Step D: 读取性能矩阵并计算 Read Performance matrix and calculate ===
        try:
            # Read App Score matrix
            matrix_df = pd.read_csv('average_matrix_result.csv', header=None)
            matrix_df.index = criteria       
            matrix_df.columns = alternatives 
            performance_df = matrix_df.T # Transform：Row=App, Column=Criteria
            
        except FileNotFoundError:
            st.error("⚠️ Data cleaning result not found.")
            st.stop()
        
        # === 步骤 E: 最终得分计算 (矩阵乘法) ===
        # 准备权重向量 (确保顺序一致)
        weight_vector = [final_weights[c] for c in criteria]
        
        # 计算：App分数 = 性能矩阵 • 最终权重向量
        scores = performance_df.dot(weight_vector)
        
        results_df = pd.DataFrame(scores, columns=["Score"]).sort_values(by="Score", ascending=False)
        
        # === 步骤 F: 展示结果 ===
        st.markdown("---")
        st.subheader("🏆 Final Recommendation")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.bar_chart(results_df)
        with c2:
            winner = results_df.index[0]
            st.success(f"Best Match:\n\n### **{winner}**")
            st.write(results_df.style.format("{:.4f}"))