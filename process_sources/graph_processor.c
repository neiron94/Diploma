#include "graph_processor.h"

double process_graph_set(graph**, const int, const int, bool);
void free_graphs(graph**, const int);

void process_graphs(const char *path, const bool is_isomorphic, Result *result, bool opt_tree, bool opt_planar) {
    // Fills result->count and result->nodes
    read_filenames(path, result);

    // Time result allocation
    result->time = malloc((result->count) * sizeof(double));
    if (!(result->time)) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < result->count; i++)
        (result->time)[i] = 0;

    // Read and process each file
    for (int i = 0; i < result->count; i++) {
        graph **graphs;
        int graph_count;

        // Read
        char filename[512];
        snprintf(filename, sizeof(filename), "%s%d.g6", path, (result->nodes)[i]);
        read_all_graphs_from_file(filename, &graphs, &graph_count);

        // Process graph set
        const double time = process_graph_set(graphs, graph_count, (result->nodes)[i], is_isomorphic);
        (result->time)[i] = time;

        // Free
        free_graphs(graphs, graph_count);
    }

    printf("%s graphs are processed.\n", is_isomorphic ? "Isomorphic" : "Non-isomorphic");
}

double process_graph_set(graph **graphs, const int graph_count, const int n, bool is_isomorphic) {
    double total_time = 0.0;  // Total time for isomorphism checks
    int num_checks = 0;       // Number of comparisons made
    for (int i = 0; i < graph_count; i++) {
        for (int j = i + 1; j < graph_count; j++) {
            total_time += check_isomorphism_nauty(graphs[i], graphs[j], n, is_isomorphic);
            num_checks++;
        }
    }

    return total_time / num_checks;
}

void free_graphs(graph **graphs, const int count) {
    for (int i = 0; i < count; i++) {
        free(graphs[i]);
    }
    free(graphs);
}
