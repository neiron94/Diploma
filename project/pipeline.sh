#!/usr/bin/env bash

HELPTEXT="TODO"

START=10
END=500
STEP=10
SET_SIZE=5
TIMESTAMP=$(date +%s)

# Load all subscripts
for script in pipeline_scripts/*.sh; do
    source "$script"
done

# Process general arguments
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
            GRAPH_SET_SIZE=$2
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
        echo -e "${HELPTEXT}"; 
        exit 0;;
    -t | --tree)
        echo "Executing tree pipeline";
        shift;
        tree_nodes_pipeline "$@"
        ;;
    -r | --random)
        echo "Executing random graph pipeline";
        shift;
        random_nodes_pipeline "$@"
        ;;
    *)
        echo "Unknown parameter: $1, type --help for help";
        exit 1;;
esac
