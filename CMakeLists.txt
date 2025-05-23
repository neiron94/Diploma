cmake_minimum_required(VERSION 3.30)
project(project C)

set(CMAKE_C_STANDARD 11)

add_executable(
        process.exe
        process_sources/main.c
        process_sources/file_processor.c
        process_sources/graph_processor.c
        process_sources/nauty_isomorphism.c
        process_sources/tree_optimization.c
        process_sources/my_graph.c
)

# Path to nauty.a lib
link_directories(${CMAKE_SOURCE_DIR}/nauty2_8_9)

# Path to nauty headers
include_directories(${CMAKE_SOURCE_DIR}/nauty2_8_9)

# Add nauty.a static library
add_library(nauty STATIC IMPORTED)
set_target_properties(nauty PROPERTIES IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/nauty2_8_9/nauty.a)

# Link nauty.a to your target
target_link_libraries(process.exe PRIVATE nauty)