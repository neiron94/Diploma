#!/usr/bin/env bash

for i in {1..500}; do
  cd BoltzmannPlanarGraphs/build/classes
  echo 1000 | java boltzmannplanargraphs.Main

  cd ../../..
  sage -python edges_to_graph6.py BoltzmannPlanarGraphs/ListEdges.txt test/planar/
done
