import pandas as pd

path = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\train.csv"

try:
    print("Trying to load using python engine...")
    df = pd.read_csv(path, engine='python', on_bad_lines='skip')
    print("Loaded successfully with python engine!")
except Exception as e:
    print("Python engine failed:", e)
    print("Trying C engine...")
    df = pd.read_csv(path, on_bad_lines='skip')
    print("Loaded successfully with C engine!")

print("\n=== DATA HEAD ===")
print(df.head())

print("\n=== SHAPE (ROWS, COLUMNS) ===")
print(df.shape)
