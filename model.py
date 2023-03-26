from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV


class Model:
    def __init__(self):
        self.scaler = StandardScaler()
        self.regressor = None

    def prepare_data(self, X, Y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.2, random_state=42)
        self.scaler.fit(X_train)
        X_train = self.scaler.transform(X_train)
        X_test = self.scaler.transform(X_test)
        return X_train, X_test, y_train, y_test

    def train(self, X, Y):
        X_train, _, y_train, _ = self.prepare_data(X, Y)
        X_train, X_valid, y_train, y_valid = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42)
        self._cross_validation(X_valid, y_valid)

    def _cross_validation(self, X, Y, kernels=['linear', 'rbf'],
                          C=[0.1, 1, 10]):
        GrS = GridSearchCV(
            SVR(), {'C': C, 'kernel': kernels}, cv=5, return_train_score=False)
        GrS.fit(X, Y)
        self.regressor = GrS.best_estimator_

    def predict(self, X):
        return self.regressor.predict(X)
