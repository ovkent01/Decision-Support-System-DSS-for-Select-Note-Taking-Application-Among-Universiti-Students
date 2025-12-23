import pandas as pd
import numpy as np

# 1. 读取 CSV 文件
df = pd.read_csv('Note-Taking Application Selection (Responses) - Form responses 1.csv')

# ---------------------------------------------------------
# 修正部分：筛选正确的数值列
# ---------------------------------------------------------
# 原来的 df.iloc[:, 0:25] 选到了文字列。
# 你的 5x5 矩阵数据都在最后 25 列，所以我们用 -25: 来选取
data_only = df.iloc[:, -25:] 

# 打印一下看看选对了没有（应该全是数字，没有 Name 或 Timestamp）
print("前 5 行数据预览：")
print(data_only.head())

# 2. 转换成 NumPy 数组
data_array = data_only.to_numpy()

print(f"原始数据形状: {data_array.shape}")
# 应该显示 (41, 25) -> 41 个人，25 个评分

# 3. 核心操作：Reshape
# 变成 (人数, 5个维度, 5个App)
matrix_stack = data_array.reshape(-1, 5, 5)

print(f"变形后的形状: {matrix_stack.shape}")

# 4. 计算平均矩阵
average_matrix = np.mean(matrix_stack, axis=0)

print("\n--- 最终的平均 5x5 Matrix ---")
print(average_matrix)

# 这一步将计算出的 5x5 矩阵保存为 CSV
pd.DataFrame(average_matrix).to_csv('average_matrix_result.csv', header=False, index=False)