#!/bin/bash
set -e
mkdir -p dist
cp *.html dist/
cp *.css dist/
cp *.js dist/
cp *.png dist/ 2>/dev/null || true
cp *.zip dist/ 2>/dev/null || true
