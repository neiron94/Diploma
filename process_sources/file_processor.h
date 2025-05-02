#ifndef FILE_PROCESSOR_H
#define FILE_PROCESSOR_H

#include <dirent.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <stdio.h>
#include "gtools.h"
#include "result_struct.h"

void read_all_graphs_from_file(const char*, graph***, int*);
void read_filenames(const char*, Result*);
void write_to_csv(const char*, Result*, Result*, bool);

#endif
