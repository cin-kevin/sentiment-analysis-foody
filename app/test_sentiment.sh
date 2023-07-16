#! /usr/bin/env bash

cp -R ../model-research/phobert-base-vietnamese-sentiment/phobert-base-vietnamese-sentiment sentiment

python -m unittest sentiment/tests/test_sentiment_tasks.py

rm -rf sentiment/phobert-base-vietnamese-sentiment