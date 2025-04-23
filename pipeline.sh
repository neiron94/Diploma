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
echo "Run with timestamp $TIMESTAMP"
RUN_GEN="true"
RUN_PROC="true"
RUN_VIS="true"
RUN_EST="true"

# Generation variables
START=10
END=500
STEP=10
SET_SIZE=5

# Load all pipeline subscripts
for script in pipeline_scripts/*.sh; do
    source "$script"
done

# Process general arguments
case $1 in
    --drop_gen)
        echo "Drop generation stage"
        RUN_GEN="false"
        DATASET_DIR=$2
        shift
        shift
        ;;
    *)
        echo "Run all stages"
        ;;
esac

# Process generation arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
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
        *)
            break
            ;;
    esac
    shift
done

# Process type argument
case $1 in
    -h | --help | ?)
        echo -e "${HELPTEXT}"
        exit 0;;
    tree)
        echo "Executing tree pipeline"
        shift
        tree_pipeline "$@"
        ;;
    random)
        echo "Executing random graph pipeline"
        shift
        random_pipeline "$@"
        ;;
    regular)
        echo "Executing regular graph pipeline"
        shift
        regular_pipeline "$@"
        ;;
    *)
        echo "Unknown parameter: $1, type --help for help"
        exit 1;;
esac
