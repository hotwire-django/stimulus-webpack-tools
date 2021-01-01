#!/usr/bin/env bash

# Release to pypi
./package.sh
twine upload --repository pypi dist/*