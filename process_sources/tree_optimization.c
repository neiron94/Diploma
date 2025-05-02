#include "tree_optimization.h"

bool dfs_find_cycle(myGraph*, int, int, bool*);
int* find_tree_centers(myGraph*, int*);
char* encode_tree(myGraph*, int, int);

bool is_tree(myGraph *graph) {
    if (!graph || graph->vertex_count == 0)
        return false;

    bool *visited = calloc(graph->vertex_count, sizeof(bool));
    if (!visited) {
        perror("calloc");
        return false;
    }

    // Start DFS from vertex 0
    if (!dfs_find_cycle(graph, 0, -1, visited)) {
        free(visited);
        return false;  // Found a cycle
    }

    // Check if all vertices were visited (graph is connected)
    for (int i = 0; i < graph->vertex_count; ++i) {
        if (!visited[i]) {
            free(visited);
            return false;  // Graph is disconnected
        }
    }

    free(visited);
    return true;
}

bool check_isomorphism_tree(myGraph *g1, myGraph *g2) {
    if (g1->vertex_count != g2->vertex_count) {
        return false;
    }

    // Find centers
    int center_count1, center_count2;
    int *centers1 = find_tree_centers(g1, &center_count1);
    int *centers2 = find_tree_centers(g2, &center_count2);

    // Prepare memory for encodings for centers2
    char **encodings2 = malloc(center_count2 * sizeof(char*));

    // Create encodings for centers1 and compare to encodings for centers2
    for (int i = 0; i < center_count1; i++) {
        char *encoding1 = encode_tree(g1, centers1[i], -1);
        for (int j = 0; j < center_count2; j++) {
            // Create only once
            if (i == 0) encodings2[j] = encode_tree(g2, centers2[j], -1);
            // If encoding are the same, then trees are isomorphic
            if (strcmp(encoding1, encodings2[j]) == 0) {
                // Free memory
                for (int k = 0; k < center_count1; k++) {
                    free(encodings2[k]);
                }
                free(encodings2);
                free(encoding1);
                free(centers1);
                free(centers2);
                return true;
            }
        }
        free(encoding1);
    }

    // Free memory
    for (int i = 0; i < center_count1; i++) {
        free(encodings2[i]);
    }
    free(encodings2);
    free(centers1);
    free(centers2);
    return false;
}

bool dfs_find_cycle(myGraph *graph, int current, int parent, bool *visited) {
    visited[current] = true;

    myVertex v = graph->vertices[current];
    for (int i = 0; i < v.neighbour_count; i++) {
        int neighbor = v.neighbours[i];

        if (!visited[neighbor]) {
            if (!dfs_find_cycle(graph, neighbor, current, visited))
                return false;
        } else if (neighbor != parent) {
            // Found a cycle
            return false;
        }
    }
    return true;
}

/* Iteratively removes leaves of graph, so in the end only the center will remain  */
int* find_tree_centers(myGraph *graph, int *center_count) {
    int n = graph->vertex_count;
    int *degree = malloc(n * sizeof(int));
    int *leaves = malloc(n * sizeof(int));
    int leaf_count = 0;

    // Initiate degree list and origin leaves list
    for (int i = 0; i < n; i++) {
        degree[i] = graph->vertices[i].neighbour_count;
        if (degree[i] <= 1) {
            leaves[leaf_count++] = i;
        }
    }

    int processed = leaf_count;
    // Repeat until all nodes are processed (removed as leaves)
    while (processed < n) {
        // List for new leaves
        int new_leaves[graph->vertex_count];
        int new_leaf_count = 0;

        // Iterate through each current leaf and "remove" it (just decrement degree of neighbors)
        for (int i = 0; i < leaf_count; i++) {
            int leaf = leaves[i];
            // Iterate through neighbors of leaf and decrement degree
            for (int j = 0; j < graph->vertices[leaf].neighbour_count; j++) {
                int neighbor = graph->vertices[leaf].neighbours[j];
                degree[neighbor]--;
                // If degree becomes 1, new leaf has appeared
                if (degree[neighbor] == 1) {
                    new_leaves[new_leaf_count++] = neighbor;
                }
            }
        }

        // New leaves are now old leaves
        memcpy(leaves, new_leaves, new_leaf_count * sizeof(int));
        leaf_count = new_leaf_count;

        processed += new_leaf_count;
    }

    // One or two last leaves are center(s)
    int *centers = malloc(leaf_count * sizeof(int));
    memcpy(centers, leaves, leaf_count * sizeof(int));
    *center_count = leaf_count;

    // Free memory
    free(degree);
    free(leaves);

    return centers;
}

/* AHU encoding for tree isomorphism detection algorithm with linear complexity. */
char* encode_tree(myGraph *graph, int root, int parent) {
    int child_count = 0;
    char **child_encodings = malloc(graph->vertex_count * sizeof(char*));

    // Recursive step
    for (int i = 0; i < graph->vertices[root].neighbour_count; i++) {
        int neighbor = graph->vertices[root].neighbours[i];
        if (neighbor != parent) {
            child_encodings[child_count++] = encode_tree(graph, neighbor, root);
        }
    }

    // Sort the child encodings
    for (int i = 0; i < child_count - 1; i++) {
        for (int j = i + 1; j < child_count; j++) {
            if (strcmp(child_encodings[i], child_encodings[j]) > 0) {
                char *temp = child_encodings[i];
                child_encodings[i] = child_encodings[j];
                child_encodings[j] = temp;
            }
        }
    }

    // Concatenate the encodings
    int total_length = 2; // for the parentheses
    for (int i = 0; i < child_count; i++) {
        total_length += strlen(child_encodings[i]);
    }

    char *encoding = malloc((total_length + 1) * sizeof(char));
    encoding[0] = '(';
    int pos = 1;
    for (int i = 0; i < child_count; i++) {
        strcpy(encoding + pos, child_encodings[i]);
        pos += strlen(child_encodings[i]);
        free(child_encodings[i]);
    }
    encoding[pos++] = ')';
    encoding[pos] = '\0';

    free(child_encodings);
    return encoding;
}
