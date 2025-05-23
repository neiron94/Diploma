#!/usr/bin/env bash

HELPTEXT=$(cat <<-END
Usage: ./pipeline.sh [OPTIONS]

This script runs a complete pipeline for generating, processing, and visualizing graph datasets.
It supports multiple graph types including trees, random graphs, regular graphs, and more.

GENERAL OPTIONS:
  -h, --help, ?                 Show this help message and exit.

GRAPH TYPE (required if generation stage is not dropped):
  --type <graph_type>           The type of graph to generate or process.

  Supported graph types:
    path
    regular_bipartite
    complete_bipartite
    bipartite
    tree
    random
    random_connected
    regular
    cactus
    cycle
    complete
    srg
    planar

FLOW OPTIONS:
  --drop_gen <dataset_path>     Skip generation stage and use an existing dataset at the given path.
  --drop_proc <processed_file>  Skip both generation and processing stages. Provide path to an existing processed .csv file.
  --drop_vis <processed_file>   Skip generation, processing and visualisation stages. Provide path to an existing processed .csv file.
  --only_gen                    Run only generation stage.
  --only_proc <dataset_path>    Run only processing stage with dataset at the given path.
  --only_vis <processed_file>   Run only visualisation stage with provided processed .csv file.
  --only_est <processed_file>   Run only estimation stage with provided processed .csv file.

GENERATION OPTIONS (used if generation is not dropped):
  --start <int>                 Starting graph size (default: 10).
  --end <int>                   Ending graph size (default: 500).
  --step <int>                  Step size between graph sizes (default: 10).
  --set_num <int>               Number of graphs to generate per size (default: 3).
  --oi                          Only generate isomorphic graphs.

TYPE-SPECIFIC GENERATION OPTIONS:
  For 'random' and 'bipartite':
    --density <float>           Density of random graphs (default: 0.5).

  For 'regular' and 'regular_bipartite':
    --degree <int>              Degree of each vertex (default: 3).

PROCESSING OPTIONS:
    --opt_tree                  Run processing stage with optimization for trees.

NOTES:
  - For 'srg' and 'planar' types, generation is skipped automatically and pre-prepared datasets are used.
  - For 'cycle', 'complete', 'path', 'complete_bipartite' types, only isomorphic graphs are generated by default.

EXAMPLES:
  Generate and process tree graphs with default settings:
    ./pipeline.sh --type tree

  Generate random graphs of size 20 to 100 with density 0.7:
    ./pipeline.sh --start 20 --end 100 --type random --density 0.7

  Use existing dataset and skip generation:
    ./pipeline.sh --drop_gen generated_dataset/random/123456/

  Use existing processed file and skip gen/proc:
    ./pipeline.sh --drop_proc processed/regular/123456.csv
END
)

# General variables
TIMESTAMP=$(date +%s)
GRAPH_TYPE="default"

# Flow manipulation variables
RUN_GEN="true"
RUN_PROC="true"
RUN_VIS="true"
RUN_EST="true"

# Common generation variables
START=10
END=500
STEP=10
SET_SIZE=3
ONLY_ISOMORPHIC="false"

# Specific generation variables
DEGREE=3
DENSITY=0.5

# Processing variables
OPT_TREE="false"

# Process arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        # General variables
        -h | --help | ?)
            echo -e "${HELPTEXT}"
            exit 0;;
        --type)
            GRAPH_TYPE=$2
            shift;;
        # Flow manipulation
        --drop_gen)
            RUN_GEN="false"
            DATASET_DIR=$2
            shift;;
        --drop_proc)
            RUN_GEN="false"
            RUN_PROC="false"
            PROCESSED_FILENAME=$2
            shift;;
        --drop_vis|--only_est)
            RUN_GEN="false"
            RUN_PROC="false"
            RUN_VIS="false"
            PROCESSED_FILENAME=$2
            shift;;
        --only_gen)
            RUN_PROC="false"
            RUN_VIS="false"
            RUN_EST="false"
            shift;;
        --only_proc)
            RUN_GEN="false"
            RUN_VIS="false"
            RUN_EST="false"
            DATASET_DIR=$2
            shift;;
        --only_vis)
            RUN_GEN="false"
            RUN_PROC="false"
            RUN_EST="false"
            PROCESSED_FILENAME=$2
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
        # Processing arguments
        --opt_tree)
            OPT_TREE="true"
            ;;
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
    cycle|complete|path|complete_bipartite)
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

    # Set generation arguments
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

    # Compile process.exe if running for the first time
    if [ ! -f ./process.exe ]; then
        mkdir -p build
        cd build || { echo "Failed to compile process.exe"; exit 1; }
        cmake ..
        make
        cp ./process.exe ../process.exe
        cd ..
    fi

    # Set processing arguments
    PROC_ARGS=(
      "$DATASET_DIR"
      "$PROCESSED_FILENAME"
    )
    if [ "$OPT_TREE" = "true" ]; then
      PROC_ARGS+=(--opt_tree)
    fi

    ./process.exe "${PROC_ARGS[@]}" || { echo "Processing stage failed, stop pipeline"; exit 1; }
else
    echo "Drop processing stage"
fi

# 3. Visualisation
if [ "$RUN_VIS" = "true" ]; then
    echo "Start visualisation stage"

    # Set visualisation arguments
    VIS_ARGS=(
      --data_file "$PROCESSED_FILENAME"
      --output_dir "$PICTURE_DIR"
    )

    python3 draw.py "${VIS_ARGS[@]}" || { echo "Visualisation stage failed, stop pipeline"; exit 1; }
else
    echo "Drop visualisation stage"
fi

# 4. Estimation
if [ "$RUN_EST" = "true" ]; then
    echo "Start estimation stage"

    # Set estimation arguments
    EST_ARGS=(
      --data_file "$PROCESSED_FILENAME"
      --output_dir "$PICTURE_DIR"
    )

    python3 estimate.py "${EST_ARGS[@]}" || { echo "Estimation stage failed, stop pipeline"; exit 1; }
else
    echo "Drop estimation stage"
fi