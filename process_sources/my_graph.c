#include "my_graph.h"

myGraph* convert_nauty_to_mygraph(graph *g, int n) {
    int m = SETWORDSNEEDED(n);
    myGraph *result = malloc(sizeof(myGraph));
    result->vertex_count = n;
    result->vertices = calloc(n, sizeof(myVertex));

    for (int u = 0; u < n; ++u) {
        result->vertices[u].id = u;

        // Count degree first
        int deg = 0;
        set *row = GRAPHROW(g, u, m);
        for (int v = 0; v < n; ++v) {
            if (ISELEMENT(row, v)) deg++;
        }

        result->vertices[u].neighbours = malloc(deg * sizeof(int));
        result->vertices[u].neighbour_count = deg;

        // Fill neighbors
        int idx = 0;
        for (int v = 0; v < n; ++v) {
            if (ISELEMENT(row, v)) {
                result->vertices[u].neighbours[idx] = v;
                idx++;
            }
        }
    }

    return result;
}

void free_mygraph(myGraph *g) {
    if (!g) return;
    for (int i = 0; i < g->vertex_count; ++i) {
        free(g->vertices[i].neighbours);
    }
    free(g->vertices);
    free(g);
}
