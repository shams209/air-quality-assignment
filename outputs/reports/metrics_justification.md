# Metrics Justification

For this regression task (predicting a continuous AQI value), I chose the following metrics:

1. **MAE (Mean Absolute Error):** I used this to understand the average error in actual AQI points. It is highly interpretable. For example, an MAE of 10 means my model's predictions are off by an average of 10 AQI points.
2. **RMSE (Root Mean Squared Error):** I used RMSE because it heavily penalizes large errors. In environmental data, a massive error (e.g., predicting an AQI of 50 when it is actually 300) is much worse than a small error. RMSE ensures we catch these large mistakes.
3. **R² (R-squared):** I used R² to see how much of the variance in the target variable (AQI) is explained by my features. An R² of 1.0 is perfect, while 0.0 means the model is no better than just guessing the average.

**Why not Accuracy?** 
Accuracy is a classification metric used for predicting discrete categories (like "Spam" vs. "Not Spam"). Because AQI is a continuous number, using accuracy would be mathematically invalid.