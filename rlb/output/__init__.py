"""Output benchmark results."""

import llama_bench
import os
import sysinfo


def print_results(results, parser):
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
    print(llama_bench.run_summary(results))
