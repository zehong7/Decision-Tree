from hunt_algorithm import *

class DecisionTree:
    def __init__(self, num_bins=200, max_depth=None, min_samples_split=2):
        self.tree = None
        self.attribute_names = None
        self.num_bins = num_bins
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
    
    def fit(self, data, target_index=-1):
        """
        Train the decision tree
        """
        self.attribute_names = data[0]
        data = data[1:]
        self.tree = build_tree(data, target_index, attribute_names=self.attribute_names, 
                               max_depth=self.max_depth, min_samples_split=self.min_samples_split,
                               num_bins=self.num_bins)
        
    def predict_instance(self, tree, instance):
        """
        Predict the label for a single instance
        """
        if not isinstance(tree, dict):
            return tree
        
        for key, subtree in tree.items():
            if "<=" in key:
                # numeric attribute
                attr_name = key.split()[1]
                threshold = float(key.split()[-1])
                if float(instance[self.attribute_names.index(attr_name)]) <= threshold:
                    return self.predict_instance(subtree["True"], instance)
                else:
                    return self.predict_instance(subtree["False"], instance)
            else:
                # categorical attribute
                attr_name = key.split()[1]
                attr_value = ""
                try:
                    attr_value= instance[self.attribute_names.index(attr_name)]
                    if attr_value in subtree:
                        return self.predict_instance(subtree[attr_value], instance)
                    else:
                        return max_majority_label([row[-1] for row in tree])
                except IndexError:
                    return max_majority_label([row[-1] for row in tree])
    
    def predict(self, data):
        """
        Predict labels for a specific dataset
        """
        return [[self.predict_instance(self.tree, instance)] for instance in data]
    
    def evaluate(self, y_actual, y_pred):
        """
        Evaluate the decision tree on the given dataset
        """
        correct_num = sum(1 for a, p in zip(y_actual, y_pred) if a == p)
        accuracy = correct_num / len(y_actual)
        return accuracy
    
    def save_tree(self, filename):
        """
        Save the decision tree to a file
        """
        with open(filename, 'w') as f:
            write_tree(self.tree, 0, f)
        