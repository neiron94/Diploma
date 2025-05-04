#ifndef GRAPH_PROCESSOR_H
#define GRAPH_PROCESSOR_H

#include <stdbool.h>
#include <time.h>
#include "result_struct.h"
#include "nauty_isomorphism.h"
#include "file_processor.h"
#include "tree_optimization.h"
#include "my_graph.h"

void process_graphs(const char*, const bool, Result*, bool);

#endif