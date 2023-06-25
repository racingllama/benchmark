#!/usr/bin/env python3
"""Racing Llama Benchmark Alpha - a benchmarking application for llama.cpp."""

import argparse
import llama_bench
import os
import sysinfo

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gpu", action="store_true", default=False)
parser.add_argument("-m", "--model", type=str, required=True)
parser.add_argument("-p", "--prompt", type=str, default="test")
parser.add_argument("-r", "--runs", type=int, default=3)
parser.add_argument("-s", "--seed", type=int, default=42)
parser.add_argument("-t", "--threads", type=int, default=sysinfo.threads())


def print_results(results):
    """Print benchmark results.

    Args:
        results (dict): Benchmark results.
    """
    print(
        f"""
Racing Llama Benchmark

System Information:
{sysinfo.basic()}
Runs: {parser.parse_args().runs}
CPU Threads: {parser.parse_args().threads}
GPU Acceleration: {parser.parse_args().gpu}
Model: {os.path.basename(parser.parse_args().model)}
Seed: {parser.parse_args().seed}
Prompt: {parser.parse_args().prompt}
"""
    )
    print(llama_bench.summary(results))
    # print(f"Debug: {results}")


if __name__ == "__main__":
    llm = llama_bench.Benchmark(
        model=parser.parse_args().model,
        threads=parser.parse_args().threads,
        seed=parser.parse_args().seed,
        gpu=parser.parse_args().gpu,
    )
    results = llm.multiple_runs(parser.parse_args().prompt, parser.parse_args().runs)
    print_results(results)
