#!/usr/bin/env bash

DENSITY=0.5

function random_pipeline() {

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

    if [ "$RUN_GEN" = "true" ]; then
        DATASET_DIR="generated_dataset/random/${DENSITY}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
        PROCESSED_FILENAME="processed/random/${DENSITY}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.csv"
        PICTURE_DIR="pictures/random/${DENSITY}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
    else
        PROCESSED_FILENAME="processed/random/drop_gen/${TIMESTAMP}.csv"
        PICTURE_DIR="pictures/random/drop_gen/${TIMESTAMP}/"
    fi

    # Generation
    if [ "$RUN_GEN" = "true" ]; then
        sage -python generation.py --type random --density "$DENSITY" --start "$START" --end "$END" --step "$STEP" --set_size "$SET_SIZE" --output_dir "$DATASET_DIR"
    fi

    # Processing
    if [ "$RUN_PROC" = "true" ]; then
        ./process.exe "$DATASET_DIR" "$PROCESSED_FILENAME"
    fi

    # Visualisation
    if [ "$RUN_VIS" = "true" ]; then
        python draw.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR" --title "Random Graphs with density ${DENSITY}"
    fi

    # Estimation
    if [ "$RUN_EST" = "true" ]; then
        # shellcheck disable=SC2086
        python estimate.py --data_file "$PROCESSED_FILENAME" --output_dir $PICTURE_DIR
    fi
}