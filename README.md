# Investment

The basket module creates an object that holds each commodity and the corresponding shares owned.
The dataloader module, that loads, merges my data and performs some feature engineering.
The model module contains an SVM regressor model for predicting each ETF's close value. Each commodity utilises a different model instance. In order to model the market sentiment and some macroeconomic factors, my predictors are:

-The 5days Highest value
-The 5days Lowest value
-A 5days exponential average
-A 30days exponential average
-A 60days exponential average
-US CPI factor
-US 10Y-bond 

Also, a grid search over parameters is performed.

