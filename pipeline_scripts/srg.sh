#!/usr/bin/env bash

function srg_pipeline() {

    DATASET_DIR="prepared_dataset/srg/"
    PROCESSED_FILENAME="processed/srg/${TIMESTAMP}.csv"
    PICTURE_DIR="pictures/srg/${TIMESTAMP}/"

    # Processing
    if [ "$RUN_PROC" = "true" ]; then
        ./process.exe "$DATASET_DIR" "$PROCESSED_FILENAME" --oi
    fi

    # Visualisation
    if [ "$RUN_VIS" = "true" ]; then
        python draw.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR" --title "Strongly Regular Graphs" --oi True
    fi

    # Estimation
    if [ "$RUN_EST" = "true" ]; then
        python estimate.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR"
    fi
}