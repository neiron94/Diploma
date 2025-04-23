#!/usr/bin/env bash

function tree_pipeline() {
    # shellcheck disable=SC2086
    if [ $RUN_GEN = "true" ]; then
        DATASET_DIR="generated_dataset/tree/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
        PROCESSED_FILENAME="processed/tree/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.csv"
        PICTURE_DIR="pictures/tree/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
    else
        PROCESSED_FILENAME="processed/tree/drop_gen/${TIMESTAMP}.csv"
        PICTURE_DIR="pictures/tree/drop_gen/${TIMESTAMP}/"
    fi

    # Generation
    if [ "$RUN_GEN" = "true" ]; then
        sage -python generation.py --type tree --start "$START" --end "$END" --step "$STEP" --set_size "$SET_SIZE" --output_dir "$DATASET_DIR"
    fi

    # Processing
    if [ "$RUN_PROC" = "true" ]; then
        ./process.exe "$DATASET_DIR" "$PROCESSED_FILENAME"
    fi

    # Visualisation
    if [ "$RUN_VIS" = "true" ]; then
        python draw.py --data_file : --output_dir "$PICTURE_DIR" --title "Trees"
    fi

    # Estimation
    if [ "$RUN_EST" = "true" ]; then
        python estimate.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR"
    fi
}