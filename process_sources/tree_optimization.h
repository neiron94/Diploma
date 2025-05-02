#ifndef TREE_OPTIMIZATION_H
#define TREE_OPTIMIZATION_H

#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "my_graph.h"

bool is_tree(myGraph*);
bool check_isomorphism_tree(myGraph*, myGraph*);

#endif
