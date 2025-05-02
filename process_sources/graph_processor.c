#include "graph_processor.h"

void free_graphs(graph**, const int);

void process_graphs(const char *path, const bool is_isomorphic, Result *result) {
    // Fills result->count and result->nodes
    read_filenames(path, result);

    // Time result allocation
    result->time = malloc((result->count) * sizeof(double));
    if (!(result->time)) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    // Read and process each file
    for (int i = 0; i < result->count; i++) {
        graph **graphs;
        int graph_count;

        // Read
        char filename[512];
        snprintf(filename, sizeof(filename), "%s%d.g6", path, (result->nodes)[i]);
        read_all_graphs_from_file(filename, &graphs, &graph_count);

        // Process
        const double time = check_isomorphism_nauty(graphs, graph_count, (result->nodes)[i], is_isomorphic);
        (result->time)[i] = time;

        // Free
        free_graphs(graphs, graph_count);
    }

    printf("%s graphs are processed.\n", is_isomorphic ? "Isomorphic" : "Non-isomorphic");
}

void free_graphs(graph **graphs, const int count) {
    for (int i = 0; i < count; i++) {
        free(graphs[i]);
    }
    free(graphs);
}
