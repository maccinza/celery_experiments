#!/bin/bash

parent_directory=$(dirname $(pwd))
export PYTHONPATH=$PYTHONPATH:$parent_directory

uvicorn main:app --reload
