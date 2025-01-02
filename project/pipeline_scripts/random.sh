#!/usr/bin/env bash

DENSITY=0.5

function random_nodes_pipeline() {

    while [[ "$#" -gt 0 ]]; do
        case $1 in
            -d | --density)
                DENSITY=$2
                shift;;
            *)
                echo "Unknown parameter: $1, type --help for help";
                exit 1;;
        esac
        shift
    done

    DATASET_DIR="dataset/random/${DENSITY}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
    PROCESSED_FILENAME="processed/random/${DENSITY}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.csv"
    PICTURE_FILENAME="pictures/random/${DENSITY}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.png"

    # Generation
    sage -python generation.sage --type random --density $DENSITY --start $START --end $END --step $STEP --set_size $SET_SIZE --output_dir $DATASET_DIR

    # Processing
    ./process $START $END $STEP $DATASET_DIR $PROCESSED_FILENAME

    # Visualisation
    python draw.py --data_file $PROCESSED_FILENAME --output_file $PICTURE_FILENAME --title "Random Graphs with density ${DENSITY}"
}