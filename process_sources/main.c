#include <stdbool.h>
#include "result_struct.h"
#include "graph_processor.h"
#include "file_processor.h"

int main(const int argc, char *argv[]) {
    // Process arguments
    if (argc < 3)
        exit(EXIT_FAILURE);

    const char *dataset_path = argv[1];
    const char *result_file = argv[2];

    // Init results
    Result result_i;
    Result result_ni;
    bool only_isomorphic = true;

    // Process isomorphic graphs
    char iso_path[1024];
    snprintf(iso_path, sizeof(iso_path), "%s%s", dataset_path, "isomorphic/");

    struct stat st1;
    if (stat(iso_path, &st1) == 0 && S_ISDIR(st1.st_mode)) { // directory exists
        process_graphs(iso_path, true, &result_i);
    }
    else {
        process_graphs(dataset_path, true, &result_i);
    }

    // Process non-isomorphic graphs
    char non_iso_path[1024];
    snprintf(non_iso_path, sizeof(non_iso_path), "%s%s", dataset_path, "non_isomorphic/");

    struct stat st2;
    if (stat(non_iso_path, &st2) == 0 && S_ISDIR(st2.st_mode)) { // directory exists
        only_isomorphic = false;
        process_graphs(non_iso_path, false, &result_ni);
    }

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