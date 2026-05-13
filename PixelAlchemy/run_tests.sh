#!/bin/bash
echo "Running PixelAlchemy Tests..."
python3 -m unittest discover -s tests -p "test_*.py" > test_report.txt 2>&1
echo "Tests complete. Check test_report.txt for results."
cat test_report.txt
