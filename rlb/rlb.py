#!/usr/bin/env python3
"""Racing Llama Benchmark Alpha - a benchmarking application for llama.cpp."""

import argparse
import llama_bench
import sysinfo
from output import print_results

parser = argparse.ArgumentParser()
parser.add_argument(
    "-g", "--gpu", action="store_true", default=False, help="Enable GPU acceleration."
)
parser.add_argument(
    "-p", "--prompt", type=str, default="test", help="Prompt to use for benchmarking."
)
parser.add_argument(
    "-r", "--runs", type=int, default=5, help="Number of runs to perform."
)
parser.add_argument(
    "-s", "--seed", type=int, default=42, help="Seed to use for benchmarking."
)
parser.add_argument(
    "-t",
    "--threads",
    type=int,
    default=sysinfo.threads(),
    help="Number of threads to use for benchmarking.",
)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-m", "--model", type=str)
group.add_argument("-d", "--directory", type=str)


if __name__ == "__main__":
    llm = llama_bench.Benchmark(
        model=parser.parse_args().model,
        threads=parser.parse_args().threads,
        seed=parser.parse_args().seed,
        gpu=parser.parse_args().gpu,
    )
    results = llm.multiple_runs(parser.parse_args().prompt, parser.parse_args().runs)
    print_results(results, parser)
