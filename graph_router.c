#include <stdio.h>
#include <math.h>
#include <float.h>

// Calculates Euclidean distance between two points
double get_distance(double x1, double y1, double x2, double y2) {
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
}

// Finds the optimal next planetary jump based on closest proximity to the destination
int find_next_jump(double current_x, double current_y, double* cluster_x, double* cluster_y, int num_clusters, double dest_x, double dest_y) {
    int best_index = -1;
    double min_score = DBL_MAX;

    for (int i = 0; i < num_clusters; i++) {
        // Distance from current position to cluster midpoint
        double dist_to_node = get_distance(current_x, current_y, cluster_x[i], cluster_y[i]);
        // Distance from cluster midpoint to destination target
        double dist_to_dest = get_distance(cluster_x[i], cluster_y[i], dest_x, dest_y);
        
        // Total routing cost heuristic (Greedy / A* approach)
        double total_cost = dist_to_node + dist_to_dest;

        if (total_cost < min_score) {
            min_score = total_cost;
            best_index = i;
        }
    }
    return best_index;
}
