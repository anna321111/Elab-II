import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from efficient_apriori import apriori
from scipy.stats import chi2_contingency


# Clustering-based anomaly detection
def clustering_method(data):
    model = KMeans(n_clusters=5)
    model.fit(data[['numeric_feature1', 'numeric_feature2']])
    scores = model.transform(data[['numeric_feature1', 'numeric_feature2']]).max(axis=1)
    return scores


# Association rule mining for anomaly detection
def association_rules_method(data):
    transactions = [tuple(row) for row in data[['category_feature']].to_numpy()]
    itemsets, rules = apriori(transactions, min_support=0.05, min_confidence=0.7)
    rules_scores = {rule: rule.lift for rule in rules}
    return np.array([rules_scores.get(tuple(row), 1) for row in transactions])


# Statistical hypothesis testing for anomaly detection
def statistical_test_method(data):
    observed = pd.crosstab(data['category_feature1'], data['category_feature2'])
    chi2, p, dof, expected = chi2_contingency(observed)
    return np.array([p] * len(data))  # Assume lower p-value means higher fraud score


# Main function to coordinate fraud detection
def detect_fraud(data, threshold):
    weights = {
        'clustering': 1.5,
        'association': 1.0,
        'statistical': 1.2
    }

    scores = np.zeros(len(data))
    scores += clustering_method(data) * weights['clustering']
    scores += association_rules_method(data) * weights['association']
    scores += statistical_test_method(data) * weights['statistical']

    data['fraud_score'] = scores
    data['is_fraud'] = data['fraud_score'] > threshold
    return data


# Example usage
data = pd.read_csv('data.csv')
fraud_results = detect_fraud(data, threshold=2.5)
print(fraud_results[['fraud_score', 'is_fraud']])

