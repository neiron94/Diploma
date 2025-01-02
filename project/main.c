#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <sys/stat.h>
#include "nauty.h"
#include "gtools.h"

void read_all_graphs_from_file(const char *filename, graph ***graphs, int *count) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Error: Unable to open file %s\n", filename);
        exit(EXIT_FAILURE);
    }

    int capacity = 10;
    *graphs = malloc(capacity * sizeof(graph *));
    if (!*graphs) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    *count = 0;
    graph *g = NULL;
    int reqm = 0, m, n;
    while ((g = readg(file, NULL, reqm, &m, &n)) != NULL) {
        if (*count >= capacity) {
            capacity *= 2;
            *graphs = realloc(*graphs, capacity * sizeof(graph*));
            if (!*graphs) {
                fprintf(stderr, "Error: Memory reallocation failed\n");
                fclose(file);
                exit(EXIT_FAILURE);
            }
        }
        (*graphs)[*count] = g;
        (*count)++;
    }

    fclose(file);
}

double check_isomorphism(graph **graphs, const int graphs_count, const int n, bool should_be_isomorphic) {
    DYNALLSTAT(int,lab1,lab1_sz);
    DYNALLSTAT(int,lab2,lab2_sz);
    DYNALLSTAT(int,ptn,ptn_sz);
    DYNALLSTAT(int,orbits,orbits_sz);
    DYNALLSTAT(int,map,map_sz);
    DYNALLSTAT(graph,g1,g1_sz);
    DYNALLSTAT(graph,g2,g2_sz);
    DYNALLSTAT(graph,cg1,cg1_sz);
    DYNALLSTAT(graph,cg2,cg2_sz);
    static DEFAULTOPTIONS_GRAPH(options);
    statsblk stats;
    options.getcanon = TRUE;

    const int m = SETWORDSNEEDED(n);
    nauty_check(WORDSIZE,m,n,NAUTYVERSIONID);
    DYNALLOC1(int,lab1,lab1_sz,n,"malloc");
    DYNALLOC1(int,lab2,lab2_sz,n,"malloc");
    DYNALLOC1(int,ptn,ptn_sz,n,"malloc");
    DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
    DYNALLOC1(int,map,map_sz,n,"malloc");
    DYNALLOC2(graph,g1,g1_sz,n,m,"malloc");
    DYNALLOC2(graph,g2,g2_sz,n,m,"malloc");
    DYNALLOC2(graph,cg1,cg1_sz,n,m,"malloc");
    DYNALLOC2(graph,cg2,cg2_sz,n,m,"malloc");

    double total_time = 0.0;  // Total time for isomorphism checks
    int num_checks = 0;       // Number of comparisons made
    for (int i = 0; i < graphs_count; i++) {
        for (int j = i + 1; j < graphs_count; j++) {

            // Create canonical graphs
            const clock_t start = clock();
            densenauty(graphs[i],lab1,ptn,orbits,&options,&stats,m,n,cg1);
            densenauty(graphs[j],lab2,ptn,orbits,&options,&stats,m,n,cg2);

            // Compare canonically labelled graphs
            size_t k;
            for (k = 0; k < m*(size_t)n; ++k)
                if (cg1[k] != cg2[k]) break;
            bool is_isomorphic = k == m*(size_t)n;
            if (should_be_isomorphic != is_isomorphic) {
                printf("Error: graphs on indecies %d and %d should be is_isomorphic=%hhd but was is_isomorphic=%hhd\n", i, j, should_be_isomorphic, is_isomorphic);
                exit(EXIT_FAILURE);
            }
            const clock_t end = clock();

            total_time += (double)(end - start) / CLOCKS_PER_SEC;
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

void process_graphs(const int start, const int end, const int step, const char *path, const bool is_isomorphic, int *result_count, double **result) {
    *result_count = 0;
    int capacity = 60;
    *result = malloc(capacity * sizeof(double));
    if (!*result) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    for (int i = start; i <= end; i += step) {
        graph **graphs;
        int graph_count;

        // Read
        char filename[512];
        snprintf(filename, sizeof(filename), "%s%s%d.g6", path, is_isomorphic ? "isomorphic/" : "non_isomorphic/", i);
        read_all_graphs_from_file(filename, &graphs, &graph_count);

        // Process
        const double time = check_isomorphism(graphs, graph_count, i, is_isomorphic);
        (*result)[(i - start) / step] = time;
        (*result_count)++;

        if (*result_count >= capacity) {
            capacity *= 2;
            *result = realloc(*result, capacity * sizeof(double));
            if (!*result) {
                fprintf(stderr, "Error: Memory reallocation failed\n");
                exit(EXIT_FAILURE);
            }
        }

        // Free
        free_graphs(graphs, graph_count);
    }

    printf("%s graphs are processed.\n", is_isomorphic ? "Isomorphic" : "Non-isomorphic");
}

int create_directories(const char *path) {
    char *tmp = strdup(path); // Duplicate the path to modify it
    char *p = NULL;
    size_t len = strlen(tmp);

    // Remove trailing slash if present
    if (tmp[len - 1] == '/') {
        tmp[len - 1] = '\0';
    }

    // Iterate through the path and create directories
    for (p = tmp + 1; *p; p++) {
        if (*p == '/') {
            *p = '\0'; // Temporarily end the string here

            // Create directory if it does not exist
            if (mkdir(tmp, 0755) != 0 && errno != EEXIST) {
                perror("mkdir");
                free(tmp);
                return -1;
            }

            *p = '/'; // Restore the slash
        }
    }

    // Create the final directory
    if (mkdir(tmp, 0755) != 0 && errno != EEXIST) {
        perror("mkdir");
        free(tmp);
        return -1;
    }

    free(tmp);
    return 0;
}

void write_to_csv(const int start, const int end, const int step, const char *filename, const double *result_i, const double *result_ni) {
    // Create directories
    char *dir = strdup(filename);
    char *last_slash = strrchr(dir, '/');
    if (last_slash) {
        *last_slash = '\0'; // Truncate to get the directory path
        if (create_directories(dir) != 0)
            fprintf(stderr, "Failed to create directories for: %s\n", dir);
    } else {
        printf("No directory part in filename.\n");
    }
    free(dir);

    // Write to file
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    // Write CSV header
    fprintf(file, "node_count,average_time,is_isomorphic\n");

    // Write data for result_i (is_isomorphic = true) and result_ni (is_isomorphic = false)
    for (int i = start; i <= end; i += step) {
        fprintf(file, "%d,%f,true\n", i, result_i[(i - start) / step]);
        fprintf(file, "%d,%f,false\n", i, result_ni[(i - start) / step]);
    }

    fclose(file);
    printf("Data written to %s successfully.\n", filename);
}

int main(const int argc, char *argv[]) {
    if (argc != 6)
        exit(EXIT_FAILURE);

    const int start = atoi(argv[1]), end = atoi(argv[2]), step = atoi(argv[3]);
    const char *dataset_path = argv[4];
    const char *result_file = argv[5];

    int result_count_i, result_count_ni;
    double *result_i;
    double *result_ni;

    // Process
    process_graphs(start, end, step, dataset_path, true, &result_count_i, &result_i);
    process_graphs(start, end, step, dataset_path, false, &result_count_ni, &result_ni);

    // Save to CSV
    write_to_csv(start, end, step, result_file, result_i, result_ni);

    // Free
    free(result_i);
    free(result_ni);

    return EXIT_SUCCESS;
}