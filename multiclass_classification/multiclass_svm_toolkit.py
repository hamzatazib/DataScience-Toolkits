# Author: Hamza Tazi Bouardi
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, auc
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class SVM_Toolkit():
    def __init__(
            self, 
            X_train: pd.DataFrame, 
            X_test: pd.DataFrame, 
            y_train: pd.Series, 
            y_test: pd.Series
    ):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.X_train_scaled = None
        self.X_test_scaled = None
        self.svm_rbf_model_best = None
        self.accuracy_test_svm_rbf = None
        self.svm_linear_model_best = None
        self.accuracy_test_svm_linear = None
        
    def scale_data(self):
        # Scaling data (speeds up a lot the fitting)
        scaler = StandardScaler()
        scaler.fit(self.X_train)
        self.X_train_scaled = scaler.transform(self.X_train)
        self.X_test_scaled = scaler.transform(self.X_test)

    def svm_toolkit(self):
        self.scale_data()
        self.X_train = None  # For memory purposes
        self.X_test = None  # For memory purposes
        self.linear_svm_toolkit()
        self.gaussian_svm_toolkit()

    def linear_svm_toolkit(self):
        ## Linear Kernel
        svm_linear_model = SVC(
            kernel="linear",
            random_state=0
        )
        gs_params_svm_linear = {
            "C": np.linspace(0, 10, 50),
        }
        gs_cv_obj_svm_linear = GridSearchCV(svm_linear_model, gs_params_svm_linear, cv=3, n_jobs=-1, scoring="accuracy")
        gs_cv_obj_svm_linear.fit(self.X_train_scaled, self.y_train)
        results_svm_linear = pd.DataFrame(gs_cv_obj_svm_linear.cv_results_)
        dict_best_params_svm_linear = results_svm_linear[results_svm_linear.rank_test_score == 1]["params"].values[0]
        print("Linear SVM \n", dict_best_params_svm_linear)
        self.svm_linear_model_best = SVC(
            kernel="linear",
            C=dict_best_params_svm_linear["C"],
            random_state=0,
            probability=True
        )
        self.svm_linear_model_best.fit(self.X_train_scaled, self.y_train)
        # Scores on train
        y_pred_train_svm_linear = self.svm_linear_model_best.predict(self.X_train_scaled)
        accuracy_train_svm_linear = accuracy_score(self.y_train, y_pred_train_svm_linear)
        print(f"SVM Linear scores on Train\t Accuracy={round(accuracy_train_svm_linear,3)}")
        # Scores on test
        y_pred_svm_linear = self.svm_linear_model_best.predict(self.X_test_scaled)
        self.accuracy_test_svm_linear = accuracy_score(self.y_test, y_pred_svm_linear)
        print(f"SVM Linear scores on Test " +
              f"set:\t Accuracy={round(self.accuracy_test_svm_linear,3)}")

    def gaussian_svm_toolkit(self):
        ## Gaussian Kernel
        svm_rbf_model = SVC(
            kernel="rbf",
            random_state=0
        )
        gs_params_svm_rbf = {
            "C": np.linspace(9, 50, 60),
        }
        gs_cv_obj_svm_rbf = GridSearchCV(svm_rbf_model, gs_params_svm_rbf, cv=3, n_jobs=-1, scoring="accuracy")
        gs_cv_obj_svm_rbf.fit(self.X_train_scaled, self.y_train)
        results_svm_rbf = pd.DataFrame(gs_cv_obj_svm_rbf.cv_results_)
        dict_best_params_svm_rbf = results_svm_rbf[results_svm_rbf.rank_test_score == 1]["params"].values[0]
        print("Gaussian SVM \n", dict_best_params_svm_rbf)
        self.svm_rbf_model_best = SVC(
            kernel="rbf",
            C=dict_best_params_svm_rbf["C"],
            random_state=0,
            probability=True
        )
        self.svm_rbf_model_best.fit(self.X_train_scaled, self.y_train)
        # Scores on train
        y_pred_train_svm_rbf = self.svm_rbf_model_best.predict(self.X_train_scaled)
        accuracy_train_svm_rbf = accuracy_score(self.y_train, y_pred_train_svm_rbf)
        print(f"SVM Gaussian scores on Train\t Accuracy={round(accuracy_train_svm_rbf,3)}")
        # Scores on test
        y_pred_svm_rbf = self.svm_rbf_model_best.predict(self.X_test_scaled)
        self.accuracy_test_svm_rbf = accuracy_score(self.y_test, y_pred_svm_rbf)
        print(f"SVM Gaussian scores on Test " +
              f"set:\t Accuracy={round(self.accuracy_test_svm_rbf,3)}")