#!/bin/bash
# Set up raw sources from seeds and initial snapshot
cd etl_spike && dbt seed && dbt snapshot