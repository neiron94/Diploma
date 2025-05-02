#include <stdbool.h>
#include "result_struct.h"
#include "graph_processor.h"
#include "file_processor.h"

void process_arguments(const int, char**, const char*, const char*, bool*, bool*);
void start_process(const char*, bool, Result*, bool*, bool, bool);

int main(const int argc, char *argv[]) {
    // Process arguments
    const char *dataset_path = argv[1];
    const char *result_file = argv[2];
    bool opt_tree = false;
    bool opt_planar = false;
    process_arguments(argc, argv, dataset_path, result_file, &opt_tree, &opt_planar);

    // Init results
    Result result_i;
    Result result_ni;
    bool only_isomorphic = true;

    // Start isomorphic/non-isomorphic graph processing
    start_process(dataset_path, true, &result_i, NULL, opt_tree, opt_planar);
    start_process(dataset_path, false, &result_ni, &only_isomorphic, opt_tree, opt_planar);

    // Save to CSV
    write_to_csv(result_file, &result_i, &result_ni, only_isomorphic);

    // Free
    free(result_i.nodes);
    free(result_i.time);
    if (!only_isomorphic) {
        free(result_ni.nodes);
        free(result_ni.time);
    }

    return EXIT_SUCCESS;
}

void process_arguments(const int argc, char **argv, const char *dataset_path, const char *result_file, bool *opt_tree, bool *opt_planar) {
    // Process required flags
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <dataset_path> <result_file> [--opt_tree] [--opt_planar]\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    dataset_path = argv[1];
    result_file = argv[2];

    // Process optional flags
    for (int i = 3; i < argc; ++i) {
        if (strcmp(argv[i], "--opt_tree") == 0) {
            *opt_tree = true;
        } else if (strcmp(argv[i], "--opt_planar") == 0) {
            *opt_planar = true;
        } else {
            fprintf(stderr, "Unknown option: %s\n", argv[i]);
            exit(EXIT_FAILURE);
        }
    }
}

void start_process(const char *dataset_path, bool is_isomorphic, Result *result, bool *only_isomorphic, bool opt_tree, bool opt_planar) {
    // Construct path with subdirectory
    char path[1024];
    snprintf(path, sizeof(path), "%s%s", dataset_path, is_isomorphic ? "isomorphic/" : "non_isomorphic/");

    // If subdirectory exists, use data from it
    struct stat st;
    if (stat(path, &st) == 0 && S_ISDIR(st.st_mode)) { // directory exists
        // If "non-isomorphic" subdirectory exists, then dataset contains non-isomorphic data
        if (!is_isomorphic) {
          *only_isomorphic = false;
        }
        process_graphs(path, is_isomorphic, result, opt_tree, opt_planar);
    }
    // Else use data directly from dataset_path (it is consedered isomorphic)
    else if (is_isomorphic) {
        process_graphs(dataset_path, is_isomorphic, result, opt_tree, opt_planar);
    }
}