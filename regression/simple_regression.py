# Simple regression example using sklearn
# Derived from 
# https://stackabuse.com/linear-regression-in-python-with-scikit-learn/
# By by Cássia Sampaio
# Created by Sally Goldin, 9 July 2022

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

# Substitute the path_to_file content by the path to your data.csv file 
path_to_file = 'home/projects/datasets/student_scores.csv'
df = pd.read_csv(path_to_file)

df.head()


print(df.describe())

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = df['Hours'], y = df['Scores'])
plt.title("Relationship of Test Scores to Hours Studying")
plt.xlabel("Hours")
plt.ylabel("Scores")

plt.show()


# Reshape the data frames into the expected form which must
# be a 2 dimensional array. The second dimension arrays
# have a single value in this example, but would have
# more than one value for a multiple regression
y = df['Scores'].values.reshape(-1, 1)
X = df['Hours'].values.reshape(-1, 1)

SEED = 42  # remove if you want a different split on each run

# Split to train and test so we can evaluate the accuracy of prediction
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = SEED)


# Create a class instance to do the calculations
regressor = LinearRegression()
# And run to get the equation
regressor.fit(X_train, y_train)

#Print the equation
print("\nRegression Equation")
print("Y = {} + {} * X"
      .format(regressor.intercept_,regressor.coef_))

# Let's see how the testing data does
y_pred = regressor.predict(X_test)


df_preds = pd.DataFrame({'Actual': y_test.squeeze(), 'Predicted': y_pred.squeeze()})
print("\nTest Results: Actual versus Predicted")
print(df_preds)


rsquared = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("\nMetrics")
print(f'Root mean squared error: {rmse:.2f}')
print(f'R-squared: {rsquared:.2f}')


