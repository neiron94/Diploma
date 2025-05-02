#ifndef GRAPH_PROCESSOR_H
#define GRAPH_PROCESSOR_H

#include <stdbool.h>
#include "result_struct.h"
#include "nauty_isomorphism.h"
#include "file_processor.h"

void process_graphs(const char *path, const bool is_isomorphic, Result *result);

#endif