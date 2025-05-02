#include "file_processor.h"

int create_directories(const char *path);

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

void read_filenames(const char* path, Result *result) {
    // Open directory
    DIR* dir = opendir(path);
    if (!dir) {
        perror("opendir failed");
        exit(EXIT_FAILURE);
    }

    // Array allocation
    int capacity = 60;
    int size = 0;
    int* ids = malloc(capacity * sizeof(int));
    if (!ids) {
        perror("malloc failed");
        closedir(dir);
        exit(EXIT_FAILURE);
    }

    // Go through files in directory
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        // Skip . and ..
        if (entry->d_type != DT_REG) continue; // regular files only
        const char* name = entry->d_name;

        // Check for ".g6" extension
        size_t len = strlen(name);
        if (len <= 3 || strcmp(name + len - 3, ".g6") != 0)
            continue;

        // Cut off .g6 and convert to int
        char number_part[256];
        strncpy(number_part, name, len - 3);
        number_part[len - 3] = '\0';

        int id = atoi(number_part);
        if (size >= capacity) {
            capacity *= 2;
            ids = realloc(ids, capacity * sizeof(int));
            if (!ids) {
                perror("realloc failed");
                closedir(dir);
                exit(EXIT_FAILURE);
            }
        }

        ids[size] = id;
        size++;
    }

    closedir(dir);
    result->count = size;
    result->nodes = ids;
}

void write_to_csv(const char *filename, Result *result_i, Result *result_ni, bool only_isomorphic) {
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
    for (int i = 0; i < result_i->count; i++) {
        fprintf(file, "%d,%f,true\n", (result_i->nodes)[i], (result_i->time)[i]);
    }

    if (!only_isomorphic) {
        for (int i = 0; i < result_ni->count; i++) {
             fprintf(file, "%d,%f,false\n", (result_ni->nodes)[i], (result_ni->time)[i]);
        }
    }

    fclose(file);
    printf("Data written to %s successfully.\n", filename);
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
