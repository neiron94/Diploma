#!/usr/bin/env bash

for i in {1..500}; do
  # Use Boltzmann planar graph generator
  cd BoltzmannPlanarGraphs/build/classes
  echo 1000 | java boltzmannplanargraphs.Main

  # Convert Boltzmann graph from edges to graph6 format
  cd ../../..
  sage -python edges_to_graph6.py BoltzmannPlanarGraphs/ListEdges.txt graph6_single/planar/
done
