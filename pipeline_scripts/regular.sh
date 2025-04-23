#!/usr/bin/env bash

DEGREE=3

function regular_pipeline() {

    while [[ "$#" -gt 0 ]]; do
        case $1 in
            -d | --degree)
                DEGREE=$2
                shift;;
            *)
                echo "Unknown parameter: $1, type --help for help";
                exit 1;;
        esac
        shift
    done

    if [ "$RUN_GEN" = "true" ]; then
        DATASET_DIR="generated_dataset/regular/${DEGREE}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
        PROCESSED_FILENAME="processed/regular/${DEGREE}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}.csv"
        PICTURE_DIR="pictures/regular/${DEGREE}/${START}_${END}_${STEP}_${SET_SIZE}/${TIMESTAMP}/"
    else
        PROCESSED_FILENAME="processed/regular/drop_gen/${TIMESTAMP}.csv"
        PICTURE_DIR="pictures/regular/drop_gen/${TIMESTAMP}/"
    fi

    # Generation
    if [ "$RUN_GEN" = "true" ]; then
        sage -python generation.py --type regular --degree "$DEGREE" --start "$START" --end "$END" --step "$STEP" --set_size "$SET_SIZE" --output_dir "$DATASET_DIR" --oi True
    fi

    # Processing
    if [ "$RUN_PROC" = "true" ]; then
        ./process.exe "$DATASET_DIR" "$PROCESSED_FILENAME" --oi
    fi

    # Visualisation
    if [ "$RUN_VIS" = "true" ]; then
        python draw.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR" --title "Regular Graphs with degree ${DEGREE}" --oi True
    fi

    # Estimation
    if [ "$RUN_EST" = "true" ]; then
        python estimate.py --data_file "$PROCESSED_FILENAME" --output_dir "$PICTURE_DIR"
    fi
}