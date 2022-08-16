set -x

{ echo "Deleting cleaned data files"; } 2>/dev/null
find data/clean -type f -not -name "*.md" -delete

{ echo "Deleting output files"; } 2>/dev/null
find output -type f -not -name "*.md" -delete