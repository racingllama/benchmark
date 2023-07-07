"""Test output module."""

from rlb.output import output
from unittest.mock import Mock
import sys


def test_denormalize_results():
    """Test denormalize_results."""
    results = [
        {
            "name": "test1",
            "parameters": "param1",
            "quant": 1,
            "data": {
                "eval": {"fastest": 10, "slowest": 20, "mean": 15, "median": 12},
                "prompt": {"fastest": 5, "slowest": 10, "mean": 7, "median": 6},
            },
        },
        {
            "name": "test2",
            "parameters": "param2",
            "quant": 2,
            "data": {
                "eval": {"fastest": 30, "slowest": 40, "mean": 35, "median": 32},
                "prompt": {"fastest": 25, "slowest": 30, "mean": 27, "median": 26},
            },
        },
    ]

    expected = [
        {
            "name": "test1",
            "parameters": "param1",
            "quant": 1,
            "eval_fastest": 10,
            "eval_slowest": 20,
            "eval_mean": 15,
            "eval_median": 12,
            "prompt_fastest": 5,
            "prompt_slowest": 10,
            "prompt_mean": 7,
            "prompt_median": 6,
        },
        {
            "name": "test2",
            "parameters": "param2",
            "quant": 2,
            "eval_fastest": 30,
            "eval_slowest": 40,
            "eval_mean": 35,
            "eval_median": 32,
            "prompt_fastest": 25,
            "prompt_slowest": 30,
            "prompt_mean": 27,
            "prompt_median": 26,
        },
    ]

    assert output.denormalize(results) == expected


def test_results_directory():
    """Test results with directory type."""
    parser = Mock()
    parser.parse_args.return_value.runs = 3
    parser.parse_args.return_value.threads = 4
    parser.parse_args.return_value.gpu = True
    parser.parse_args.return_value.seed = 123
    results = [
        {
            "name": "test1",
            "parameters": "param1",
            "quant": 1,
            "data": {
                "eval": {"fastest": 10, "slowest": 20, "mean": 15, "median": 12},
                "prompt": {"fastest": 5, "slowest": 10, "mean": 7, "median": 6},
            },
        },
        {
            "name": "test2",
            "parameters": "param2",
            "quant": 2,
            "data": {
                "eval": {"fastest": 30, "slowest": 40, "mean": 35, "median": 32},
                "prompt": {"fastest": 25, "slowest": 30, "mean": 27, "median": 26},
            },
        },
    ]

    expected = """Racing Llama Benchmark

System Information:
OS: MacOS
ARCH: arm64
CPU: Apple M2 - 8 cores (4 performance and 4 efficiency)
GPU: Apple M2 - 10 cores
RAM: 16 GB
Runs: 3
llama-cpp-python version: 0.1.68
CPU Threads: 4
GPU Acceleration: True
Seed: 123

Eval Tokens per second:
| Model   | Params   |   Quant |   Fastest |   Slowest |   Mean |   Median |
|---------|----------|---------|-----------|-----------|--------|----------|
| test1   | param1   |       1 |        10 |        20 |     15 |       12 |
| test2   | param2   |       2 |        30 |        40 |     35 |       32 |

Prompt Tokens per second:
| Model   | Params   |   Quant |   Fastest |   Slowest |   Mean |   Median |
|---------|----------|---------|-----------|-----------|--------|----------|
| test1   | param1   |       1 |         5 |        10 |      7 |        6 |
| test2   | param2   |       2 |        25 |        30 |     27 |       26 |"""

    assert output.results(results, parser, type="directory") == expected


def test_results_model():
    """Test results with model type."""
    parser = Mock()
    parser.parse_args.return_value.runs = 3
    parser.parse_args.return_value.threads = 4
    parser.parse_args.return_value.gpu = True
    parser.parse_args.return_value.model = "fake_model"
    parser.parse_args.return_value.seed = 123

    results = {
        0: {
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens ": 30,
            },
            "load": {"time": 100.00},
            "sample": {
                "ms_per_token": 1.23,
                "runs": 456,
                "time": 100.10,
                "tokens_per_sec": 1000.95,
            },
            "prompt": {
                "ms_per_token": 32.42,
                "runs": 2,
                "time": 104.00,
                "tokens_per_sec": 20.00,
            },
            "eval": {
                "ms_per_token": 75,
                "runs": 200,
                "time": 13000.1,
                "tokens_per_sec": 16.10,
            },
            "total": {"time": 16000.95},
        },
        1: {
            "usage": {
                "prompt_tokens": 20,
                "completion_tokens": 30,
                "total_tokens": 50,
            },
            "load": {"time": 200.10},
            "sample": {
                "ms_per_token": 3.14,
                "runs": 20,
                "time": 150.01,
                "tokens_per_sec": 130,
            },
            "prompt": {
                "ms_per_token": 50.50,
                "runs": 2,
                "time": 110.10,
                "tokens_per_sec": 22.22,
            },
            "eval": {
                "ms_per_token": 60.60,
                "runs": 60,
                "time": 12500.5,
                "tokens_per_sec": 15.15,
            },
            "total": {"time": 13500.50},
        },
    }

    expected = """Racing Llama Benchmark

System Information:
OS: MacOS
ARCH: arm64
CPU: Apple M2 - 8 cores (4 performance and 4 efficiency)
GPU: Apple M2 - 10 cores
RAM: 16 GB
Runs: 3
llama-cpp-python version: 0.1.68
CPU Threads: 4
GPU Acceleration: True
Model: fake_model
Seed: 123
Prompt Tokens Per Second:
Fastest: 22.22
Slowest: 20.00
Mean:    21.11
Median:  21.11

Eval Tokens Per Second:
Fastest: 16.10
Slowest: 15.15
Mean:    15.62
Median:  15.62"""

    assert output.results(results, parser) == expected
