import streamlit as st
import pandas as pd
import numpy as np

def render_home_page():
    """
    function of rendering Home page
    """
    st.title("Welcome to Note-Taking Application Selection Decision Support System")
    st.markdown("""
    This system is using **AHP (Analytic Hierarchy Process)** to help your most suitable note-taking app."""
    """
    Please set your preferences in slidebar at left side.
    """)
    
    # --- 1. define data ---
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

    # --- 2. Slidebar ---
    with st.sidebar:
        st.header("🎯 Your Preferences Setting")
        st.info("Please drag the slider to set the importance of each criteria for you. (0-10)")
        
        raw_weights = {}
        for c in criteria:
            raw_weights[c] = st.slider(f"{c}", 0, 10, 5)

        calc_btn = st.button("Start", type="primary")

    # --- 3. Algorithm Logic ---
    if calc_btn or True:
        total_score = sum(raw_weights.values())
        
        if total_score == 0:
            st.error("Please at least give one mark in any criteria.")
            return

        normalized_weights = {k: v / total_score for k, v in raw_weights.items()}
        
        # 显示权重分布show weight distribution
        st.subheader("1. Your preference weightages")
        weights_df = pd.DataFrame(list(normalized_weights.items()), columns=["criteria", "weight"])
        st.bar_chart(weights_df.set_index("criteria"))

        # ---------------------------------------------------------
        # 替换部分：尝试读取真实 CSV 数据
        # ---------------------------------------------------------
        try:
            # 读取你刚才生成的 CSV，header=None 表示没有标题行
            # 原始 CSV 结构是：行=准则，列=App
            matrix_df = pd.read_csv('average_matrix_result.csv', header=None)
            
            # 给数据加上标签，方便后续对应
            matrix_df.index = criteria       # 行索引设为：易用性、功能性...
            matrix_df.columns = alternatives # 列名设为：GoodNotes, Notability...
            
            # 【关键】转置矩阵 (.T)
            # 因为下面的计算逻辑要求：行=App，列=准则
            performance_df = matrix_df.T
            
        except FileNotFoundError:
            st.error("⚠️ Can't found 'average_matrix_result.csv' file. Please run datacleanning.py file to generate this file.")
            st.stop() # 停止运行，防止后续报错
        
        # 计算
        weight_vector = [normalized_weights[c] for c in criteria]
        final_scores = performance_df.dot(weight_vector)
        results_df = pd.DataFrame(final_scores, columns=["Overall Point"]).sort_values(by="Overall Point", ascending=False)
        
        st.markdown("""
            Please scroll down to view the result."""
            )

        # 显示结果
        st.markdown("---")
        st.subheader("🏆 Recommendation Ranking")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(results_df)
        with col2:
            winner = results_df.index[0]
            st.success(f"Recommend First Choice：\n\n### **{winner}**")
            st.dataframe(results_df.style.format("{:.2f}"))