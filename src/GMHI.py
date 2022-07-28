from sklearn.base import BaseEstimator
from sklearn.metrics import balanced_accuracy_score
import numpy as np
import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

"""
Class that implements the GMHI algorithm. Extends sklearn base estimator for
cross validation compatibility
"""


class GMHI(BaseEstimator):

    def __init__(self, use_shannon=False, theta_f=1, theta_d=0):
        self.use_shannon = use_shannon
        self.fitted = False
        self.thresh = 0.00001
        self.health_abundant = None
        self.health_scarce = None
        self.features = None
        self.theta_f = theta_f
        self.theta_d = theta_d

    def fit(self, X, y):
        """
        Identifies health_abundant and health_scarce
        columns/features
        """
        self.features = X.columns
        self.classes_ = np.unique(y)
        if(isinstance(X, pd.DataFrame)):
            X = X.values
        if(isinstance(y, pd.DataFrame)):
            y = y.values
        self.fitted = True
        difference, fold_change = self.get_proportion_comparisons(X, y)
        self.select_features(difference, fold_change)

    def get_proportion_comparisons(self, X, y):
        # get healthy and unhealthy samples
        healthies = X[y.flatten(), :]
        unhealthies = X[~y.flatten(), :]

        # get proportions for each species
        proportion_healthy = self.get_proportions(healthies)
        proportion_unhealthy = self.get_proportions(unhealthies)

        # get differences and fold change
        diff = proportion_healthy - proportion_unhealthy
        fold = proportion_healthy / proportion_unhealthy
        return diff, fold

    def get_proportions(self, samples_of_a_class):
        num_samples = samples_of_a_class.shape[0]
        p = np.sum(samples_of_a_class > self.thresh, axis=0) / num_samples
        return p

    def select_features(self, difference, fold_change):
        # based on proportion differences and fold change, select health abundant
        # and health scarce
        self.health_abundant = self.features[self.cutoff(difference, fold_change)]
        self.health_scarce = self.features[self.cutoff(-1 * difference, 1 / fold_change)]

    def cutoff(self, diff, fold):
        diff_cutoff = diff > self.theta_d
        fold_cutoff = fold > self.theta_f
        both_cutoff = np.bitwise_and(diff_cutoff, fold_cutoff)
        columns = np.where(both_cutoff)
        return columns[0]

    def decision_function(self, X):
        if not self.fitted:
            return None
        if list(X.columns) != list(self.features):
            raise Exception("Model was trained with (different) feature names than input")
        # if(isinstance(X, pd.DataFrame)):
        #    X = X.values
        X_healthy_features = X[self.health_abundant]
        X_unhealthy_features = X[self.health_scarce]
        psi_MH = self.get_psi(X_healthy_features.values) / (
            X_healthy_features.shape[1])
        psi_MN = self.get_psi(X_unhealthy_features.values) / (
            (X_unhealthy_features.shape[1]))
        num = psi_MH + self.thresh
        dem = psi_MN + self.thresh
        return np.log10(num / dem)

    def get_psi(self, X):
        psi = self.richness(X) * 1.0
        if self.use_shannon:
            shan = self.shannon(X)
            psi *= shan
        return psi

    def richness(self, X):
        """
        Returns the number of nonzero values for each sample (row) in X
        """
        rich = np.sum(X > self.thresh, axis=1)
        return rich

    def shannon(self, X):
        logged = np.log(X)
        logged[logged == -np.inf] = 0
        logged[logged == np.inf] = 0
        shan = logged * X * -1
        return np.sum(shan, axis=1)

    def predict(self, X):
        return self.decision_function(X) > 0