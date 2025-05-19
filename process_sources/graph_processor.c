#include "graph_processor.h"

double process_graph_set(graph**, const int, const int, bool, bool);
bool try_tree_optimization(graph*, graph*, const int, bool, double*);
void free_graphs(graph**, const int);

void process_graphs(const char *path, const bool is_isomorphic, Result *result, bool opt_tree) {
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
        const double time = process_graph_set(graphs, graph_count, (result->nodes)[i], is_isomorphic, opt_tree);
        (result->time)[i] = time;

        // Free
        free_graphs(graphs, graph_count);
    }

    printf("%s graphs are processed.\n", is_isomorphic ? "Isomorphic" : "Non-isomorphic");
}

double process_graph_set(graph **graphs, const int graph_count, const int n, bool is_isomorphic, bool opt_tree_flag) {
    double total_time = 0.0;  // Total time for isomorphism checks
    int num_checks = 0;       // Number of comparisons made
    for (int i = 0; i < graph_count; i++) {
        for (int j = i + 1; j < graph_count; j++) {
            // Try optimization for trees, if flag --opt_tree was set
            bool opt_tree_success = opt_tree_flag ? try_tree_optimization(graphs[i], graphs[j], n, is_isomorphic, &total_time) : false;

            // If no optimization successed, then run common nauty algorithm
            if (!opt_tree_success) {
                total_time += check_isomorphism_nauty(graphs[i], graphs[j], n, is_isomorphic);
            }

            num_checks++;
        }
    }

    return total_time / num_checks;
}

bool try_tree_optimization(graph *graph1, graph *graph2, const int n, bool should_be_isomorphic, double *total_time) {
    // Check if first graph is a tree
    myGraph *my_graph1 = convert_nauty_to_mygraph(graph1, n);

    const clock_t first_tree_check_start = clock();
    bool is_tree_first = is_tree(my_graph1);
    const clock_t first_tree_check_end = clock();

    *total_time += (double)(first_tree_check_end - first_tree_check_start) / CLOCKS_PER_SEC;
    if (!is_tree_first) return false;

    // Check if second graph is a tree
    myGraph *my_graph2 = convert_nauty_to_mygraph(graph2, n);

    const clock_t second_tree_check_start = clock();
    bool is_tree_second = is_tree(my_graph2);
    const clock_t second_tree_check_end = clock();

    *total_time += (double)(second_tree_check_end - second_tree_check_start) / CLOCKS_PER_SEC;
    if (!is_tree_second) return false;

    // Run tree isomorphism algorithm
    const clock_t isomorphism_check_start = clock();
    bool result = check_isomorphism_tree(my_graph1, my_graph2);
    const clock_t isomorphism_check_end = clock();

    *total_time += (double)(isomorphism_check_end - isomorphism_check_start) / CLOCKS_PER_SEC;

    // Check for error
    if (result != should_be_isomorphic) {
        printf("Error: graphs with n=%d vertexes should be is_isomorphic=%hhd but was is_isomorphic=%hhd\n", n, should_be_isomorphic, result);
        exit(EXIT_FAILURE);
    }

    // Free memory
    free_mygraph(my_graph1);
    free_mygraph(my_graph2);

    return true;
}

void free_graphs(graph **graphs, const int count) {
    for (int i = 0; i < count; i++) {
        free(graphs[i]);
    }
    free(graphs);
}
