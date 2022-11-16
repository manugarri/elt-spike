#!/bin/bash
# Set up raw sources from seeds and initial snapshot
cd elt_spike && dbt seed && dbt snapshot