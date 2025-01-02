#!/usr/bin/env bash

function tree_nodes_pipeline() {
    DATASET_DIR="dataset/tree/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
    PROCESSED_FILENAME="processed/tree/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.csv"
    PICTURE_FILENAME="pictures/tree/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.png"

    # Generation
    sage -python generation.sage --type tree --start $START --end $END --step $STEP --set_size $SET_SIZE --output_dir $DATASET_DIR

    # Processing
    ./process $START $END $STEP $DATASET_DIR $PROCESSED_FILENAME

    # Visualisation
    python draw.py --data_file $PROCESSED_FILENAME --output_file $PICTURE_FILENAME --title "Trees"
}