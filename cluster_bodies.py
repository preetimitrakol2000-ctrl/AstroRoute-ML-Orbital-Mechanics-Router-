import random
import math

class MiniKMeans:
    """A lightweight K-Means implementation built from scratch without scikit-learn."""
    def __init__(self, k=3, max_iters=20):
        self.k = k
        self.max_iters = max_iters

    def fit(self, points):
        if len(points) < self.k:
            return points

        # Step 1: Randomly initialize centroids
        centroids = random.sample(points, self.k)

        for _ in range(self.max_iters):
            # Step 2: Assign points to closest centroids
            clusters = [[] for _ in range(self.k)]
            for p in points:
                distances = [math.dist(p, c) for c in centroids]
                closest_idx = distances.index(min(distances))
                clusters[closest_idx].append(p)

            # Step 3: Recompute centroids as averages of clusters
            new_centroids = []
            for i in range(self.k):
                if not clusters[i]:
                    new_centroids.append(centroids[i]) # Keep old if empty
                    continue
                avg_x = sum(p[0] for p in clusters[i]) / len(clusters[i])
                avg_y = sum(p[1] for p in clusters[i]) / len(clusters[i])
                new_centroids.append((avg_x, avg_y))

            centroids = new_centroids
        return centroids
