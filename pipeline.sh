#!/usr/bin/env bash

HELPTEXT=$(cat <<-END
Usage: pipeline.sh [GENERAL_OPTIONS] [GENERATION_OPTIONS] TYPE [TYPE_OPTIONS]

This script runs pipelines for generating, processing, and visualizing graph datasets. 
Each pipeline corresponds to a specific type of graph: trees, random graphs, or regular graphs. 

General Options:
  Run all stages by default: generation, processing, visualization and estimation.
  --drop_gen <dataset_path>     Run all stages except generation. Then path to existing dataset should be provided.

Generation Options:
  --start <value>       Starting size for graphs (default: 10)
  --end <value>         Maximum size for graphs (default: 500)
  --step <value>        Increment step for graph sizes (default: 10)
  --set_num <value>     Number of graphs to generate per size (default: 5)
  -h, --help, ?         Display this help message

TYPE (required):
  Specify the type of graph pipeline to execute:
  tree                  Execute the tree graph pipeline
  random                Execute the random graph pipeline
  regular               Execute the regular graph pipeline

TYPE_OPTIONS:
  Each graph type has additional options:

  Tree Graph Pipeline:
    No additional options

  Random Graph Pipeline:
    -d, --density <value>    Set the density of random graphs (default: 0.5)

  Regular Graph Pipeline:
    -d, --degree <value>     Set the degree of regular graphs (default: 3)

Examples:
  Generate and process tree graphs with default settings:
    ./pipeline.sh tree

  Generate random graphs with density 0.7 and graph sizes from 20 to 100:
    ./pipeline.sh --start 20 --end 100 random --density 0.7

  Generate regular graphs of degree 4 with default graph sizes:
    ./pipeline.sh regular --degree 4

END
)

# General variables
TIMESTAMP=$(date +%s)
GRAPH_TYPE="default"
RUN_GEN="true"
RUN_PROC="true"
RUN_VIS="true"
RUN_EST="true"

# Common generation variables
START=10
END=500
STEP=10
SET_SIZE=5
ONLY_ISOMORPHIC="false"

# Specific generation variables
DEGREE=3
DENSITY=0.5

# Process arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        # General variables
        -h | --help | ?)
            echo -e "${HELPTEXT}"
            exit 0;;
        --drop_gen)
            RUN_GEN="false"
            DATASET_DIR=$2
            shift;;
        --drop_proc)
            RUN_GEN="false"
            RUN_PROC="false"
            PROCESSED_FILENAME=$2
            shift;;
        --type)
            GRAPH_TYPE=$2
            shift;;
        # Common generation arguments
        --start)
            START=$2
            shift;;
        --end)
            END=$2
            shift;;
        --step)
            STEP=$2
            shift;;
        --set_num)
            SET_SIZE=$2
            shift;;
        --oi)
            ONLY_ISOMORPHIC="true"
            ;;
        # Specific generation arguments
        --degree)
            DEGREE=$2
            shift;;
        --density)
            DENSITY=$2
            shift;;
        *)
            echo "Unknown parameter: $1, type --help for help"
            exit 1;;
    esac
    shift
done

# Force some parameters for some graph types
case "$GRAPH_TYPE" in
    srg|planar)
        RUN_GEN="false"
        DATASET_DIR="prepared_dataset/${GRAPH_TYPE}/"
        ;;
    regular|cycle|complete|regular_bipartite)
        ONLY_ISOMORPHIC="true"
        ;;
esac

# Create files and directories names
if [ "$RUN_GEN" = "true" ]; then
    DATASET_DIR="generated_dataset/${GRAPH_TYPE}/${TIMESTAMP}/"
fi
if [ "$RUN_PROC" = "true" ]; then
    PROCESSED_FILENAME="processed/${GRAPH_TYPE}/${TIMESTAMP}.csv"
fi
PICTURE_DIR="pictures/${GRAPH_TYPE}/${TIMESTAMP}/"


# Execute pipeline
echo "Executing pipeline. Graph type = ${GRAPH_TYPE}, timestamp = ${TIMESTAMP}."

# 1. Generation
if [ "$RUN_GEN" = "true" ]; then
    echo "Start generation stage"
    GEN_ARGS=(
      --type "$GRAPH_TYPE"
      --density "$DENSITY"
      --degree "$DEGREE"
      --start "$START"
      --end "$END"
      --step "$STEP"
      --set_size "$SET_SIZE"
      --output_dir "$DATASET_DIR"
    )
    if [ "$ONLY_ISOMORPHIC" = "true" ]; then
      GEN_ARGS+=(--oi)
    fi

    sage -python generation.py "${GEN_ARGS[@]}"
else
    echo "Drop generation stage"
fi

# 2. Processing
if [ "$RUN_PROC" = "true" ]; then
    echo "Start processing stage"
    if [ ! -f ./process.exe ]; then
        mkdir -p build
        cd build
        cmake ..
        make
        cp ./process.exe ../process.exe
        cd ..
    fi

    ./process.exe "$DATASET_DIR" "$PROCESSED_FILENAME"
else
    echo "Drop processing stage"
fi

# 3. Visualisation
if [ "$RUN_VIS" = "true" ]; then
    echo "Start visualisation stage"
    python draw.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR"
else
    echo "Drop visualisation stage"
fi

# 4. Estimation
if [ "$RUN_EST" = "true" ]; then
    echo "Start estimation stage"
    python estimate.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR"
else
    echo "Drop estimation stage"
fi