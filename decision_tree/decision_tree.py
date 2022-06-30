# Simple decision tree example using sklearn
# Adapted from https://towardsdatascience.com/decision-tree-classifier-explained-in-real-life-picking-a-vacation-destination-6226b2b60575
# By Carolina Bento
#
# Adapted by YOUR NAME HERE for flower classification data set

import numpy as np
from sklearn import preprocessing

def encode_feature(array):
    """ Encode a categorical array into a number array
    
    :param array: array to be encoded
    :return: numerical array
    """
  
    encoder = preprocessing.LabelEncoder()
    encoder.fit(array)
    return encoder.transform(array)

feature_names = ['number_days', 'family_joining', 'personal_budget', 'weather_forecast', 'explore_new_places']
class_names = ['Countryside', 'Beach']
features = np.array([[10, 'Yes', 950, 75, 'Yes'],
                     [10, 'Yes', 250, 78, 'Yes'],
                     [7, 'Yes', 600, 80, 'No'],
                     [8, 'Yes', 750, 67, 'Yes'],
                     [10, 'Yes', 800, 73, 'Yes'],
                     [8, 'Yes', 850, 64, 'Yes'],
                     [15, 'No', 350, 78, 'No'],
                     [8, 'Yes', 850, 81, 'Yes'],
                     [6, 'No', 750, 59, 'Yes'],
                     [12, 'Yes', 1050, 54, 'Yes'],
                     [10, 'No', 230, 74, 'No'],
                     [3, 'Yes', 630, 74, 'Yes'],
                     [10, 'Yes', 830, 74, 'No'],
                     [12, 'No', 730, 52, 'Yes']])

# Encoding categorical features
features[:, 1] = encode_feature(features[:, 1])
features[:, 4] = encode_feature(features[:, 4])
targets = np.array(['Countryside','Beach','Beach','Countryside',
                    'Beach', 'Countryside', 'Beach','Countryside',
                    'Beach', 'Beach', 'Countryside','Countryside',
                    'Beach', 'Beach'])

targets = encode_feature(targets)

#Pre-processing done. Now it's time to build and visualize the Decision Tree.

import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def print_feature_importance(names_array, importances_array):
    """ Prints out a feature importance array as a dataframe. """
    importances = pd.DataFrame(data=names_array)
    importances[1] = importances_array
    importances = importances.T
    importances.drop(0, axis=0, inplace=True)
    importances.columns = feature_names
    
    print(str(importances.reset_index(drop=True)))

def build_tree(features, targets, feature_names, class_names):
    """ Builds a decision tree.
        Prints out the decision tree 1) as a plot, 2) as text.
        Also outputs: 1) feature importance, 2) training set and test set mean accuracy of tree
    
        :param features: model features
        :param targets: model targets
        :param feature_names: names of the dataset features
    """
  
    train_features, test_features, train_targets, test_targets = train_test_split(features, targets, test_size=0.2, random_state=123)

    decision_tree = tree.DecisionTreeClassifier(random_state=456)
    decision_tree = decision_tree.fit(train_features, train_targets)
    
    # Visualizing the decision tree
    
    # 1. Saving the image of the decision as a png   
    plt.subplots(figsize=(17, 12))
    tree.plot_tree(decision_tree, feature_names=feature_names, filled=True, rounded=True, class_names=class_names)
    plt.savefig("decision_tree.png")
    # 2. Output the tree as text in the console
    tree_as_text = tree.export_text(decision_tree, feature_names=feature_names)
    print(tree_as_text)
    # Feature Importance
    # Turns the feature importance array into a dataframe, so it has a table-like output format
    print_feature_importance(feature_names, decision_tree.feature_importances_)
    # Training and test mean accuracy
    train_error = np.round(decision_tree.score(train_features, train_targets), 2)
    test_error = np.round(decision_tree.score(test_features, test_targets), 2)
    
    print("Training Set Mean Accuracy = " + str(train_error))
    print("Test Set Mean Accuracy = " + str(test_error))

build_tree(features, targets, feature_names, class_names)
