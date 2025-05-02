#ifndef NAUTY_ISOMORPHISM_H
#define NAUTY_ISOMORPHISM_H

#include <stdbool.h>
#include <time.h>
#include "nauty.h"

double check_isomorphism_nauty(graph **graphs, const int graphs_count, const int n, bool should_be_isomorphic);

#endif