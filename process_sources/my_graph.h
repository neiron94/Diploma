#ifndef MY_GRAPH_H
#define MY_GRAPH_H

#include "nauty.h"

typedef struct {
    int id;
    int *neighbours;
    int neighbour_count;
} myVertex;

typedef struct {
    myVertex *vertices;
    int vertex_count;
} myGraph;

myGraph* convert_nauty_to_mygraph(graph*, int);
void free_mygraph(myGraph*);

#endif
