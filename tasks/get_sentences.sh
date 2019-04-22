#!/usr/bin/env bash

function download_sentences() {
    echo "Downloading sentences from Tatoeba.org"
    wget http://downloads.tatoeba.org/exports/sentences.tar.bz2 -O sentences.tar.bz2
}

function extract_sentences() {
    echo "Extracting sentences"
    tar -xjvf sentences.tar.bz2
    sentences=$(cat sentences.csv | wc -l)
    echo "Extracted file contains ${sentences} sentences"
}

function find_english_sentences() {
    echo "Looking for English sentences"
    # extract only English sentences
    # line format is: ID	lang_code	sentence
    grep -P '\teng\t' sentences.csv | \
    cut -f3- | \
    sort -u > eng_sentences.txt
    sentences=$(cat eng_sentences.txt | wc -l)
    echo "Found ${sentences} English sentences"
}

function filter_by_length() {
    echo "Filtering sentences by length"
    MIN_LENGTH="40"
    MAX_LENGTH="120"
    awk -v MIN_LENGTH="$MIN_LENGTH" -v MAX_LENGTH="$MAX_LENGTH" 'length($0)>MIN_LENGTH && length($0)<MAX_LENGTH' eng_sentences.txt > eng_sentences_filtered_by_length.txt
}

function filter_out_offensive() {
    echo "Filtering out sentences containing offensive words"
    grep -vwFi -f blocked_words.txt eng_sentences_filtered_by_length.txt > eng_sentences_without_blocked.txt
}

function replace_special_characters() {
    echo "Replacing special characters"
    while read bad good; do sed -i "s/$bad/$good/g" eng_sentences_without_blocked.txt; done < special_chars.txt
}

function other_replacements() {
    echo "Getting rid of leading blank spaces"
    sed -i 's/^[ \t]*//' eng_sentences_without_blocked.txt
    echo "Getting rid of double spaces"
    sed -i "s/  / /g" eng_sentences_without_blocked.txt
}

function sort_and_remove_duplicates() {
    echo "Sorting final list and removing duplicates"
    sort -u eng_sentences_without_blocked.txt > eng_sentences.txt
    sentences=$(cat eng_sentences.txt | wc -l)
    echo "Final list contains ${sentences} English sentences"
}


function remove_temporary_files() {
    echo "Removing temporary files"
    rm eng_sentences_filtered_by_length.txt
    rm eng_sentences_without_blocked.txt
    rm sentences.csv
    rm sentences.tar.bz2
}

function move_to_static(){
    mv eng_sentences.txt ../app/static/
}

function get_clean_sentences() {
    download_sentences
    extract_sentences
    find_english_sentences
    filter_by_length
    filter_out_offensive
    replace_special_characters
    other_replacements
    sort_and_remove_duplicates
    remove_temporary_files
    move_to_static
}


get_clean_sentences