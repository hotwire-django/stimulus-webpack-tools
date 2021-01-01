#!/usr/bin/env bash
rm -Rf build
rm -Rf dist
rm -Rf iotdb_session.egg_info
# See https://packaging.python.org/tutorials/packaging-projects/
python setup.py sdist bdist_wheel