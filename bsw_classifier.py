import numpy as np

class BSWClassifier:
    def __init__(self):
        self.hidden_nodes = []
        self.output_thresholds = {}
        self.classes = []

    def hamming_distance(self, a, b):
        return np.sum(a != b)

    def train(self, X_train, y_train):
        self.classes = np.unique(y_train)
        for cls in self.classes:
            cls_indices = np.where(y_train == cls)[0]
            not_cls_indices = np.where(y_train != cls)[0]

            patterns_cls = X_train[cls_indices]
            patterns_not_cls = X_train[not_cls_indices]

            Ave = np.round(np.mean(patterns_cls, axis=0)).astype(int)
            key = min(patterns_cls, key=lambda x: self.hamming_distance(x, Ave))
            Yes_dis = max(patterns_cls, key=lambda x: self.hamming_distance(x, key))
            No_clo = min(patterns_not_cls, key=lambda x: self.hamming_distance(x, key))

            Dist = 0
            while self.hamming_distance(key, Yes_dis) >= self.hamming_distance(key, No_clo):
                Dist += 1
                if Dist > self.hamming_distance(key, Yes_dis):
                    break

            threshold = Dist + 0.5 - np.sum(key)
            weights = np.where(key == 0, -1, 1)
            self.hidden_nodes.append({'weights': weights, 'threshold': threshold, 'class': cls})

            self.output_thresholds[cls] = self.output_thresholds.get(cls, 0) + 1

        for cls in self.classes:
            self.output_thresholds[cls] -= 0.5

    def predict(self, input_vector):
        activation_counts = {cls: 0 for cls in self.classes}
        for node in self.hidden_nodes:
            activation = np.dot(node['weights'], input_vector) >= node['threshold']
            if activation:
                activation_counts[node['class']] += 1

        predictions = [cls for cls in self.classes if activation_counts[cls] >= self.output_thresholds[cls]]

        return predictions if predictions else ['Unknown']
