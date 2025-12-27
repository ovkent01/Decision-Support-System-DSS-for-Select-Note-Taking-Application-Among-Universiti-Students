import pandas as pd
import numpy as np

# 1. read CSV file
df = pd.read_csv('Note-Taking Application Selection (Responses) - Form responses 1.csv')

# select the last 25 column of data
data_only = df.iloc[:, -25:] 

# print and observe correct or not
print("First 5 row data preview：")
print(data_only.head())

# 2. change to NumPy data collection
data_array = data_only.to_numpy()

print(f"Original Data Shape: {data_array.shape}")


# reshape become (number of respondents, 5 criteria, 5 app)
matrix_stack = data_array.reshape(-1, 5, 5)

print(f"Shape Data After Reshape: {matrix_stack.shape}")

# 4. calculate average matrix
average_matrix = np.mean(matrix_stack, axis=0)

print("\n--- Final Average 5x5 Matrix ---")
print(average_matrix)

# this step generate a csv file to save the result
pd.DataFrame(average_matrix).to_csv('average_matrix_result.csv', header=False, index=False)