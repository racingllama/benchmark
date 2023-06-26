"""Output benchmark results."""

import llama_bench
import os
import sysinfo
from tabulate import tabulate


def print_header():
    """Print benchmark header."""
    print(
        f"""
Racing Llama Benchmark

System Information:
{sysinfo.basic()}"""
    )


def print_results(results, parser, type="model"):
    """Print benchmark results.

    Args:
        results (dict): Benchmark results.
    """
    print_header()
    if type == "directory":
        denorm = denormalize_results(results)
        print(
            f"""Runs: {parser.parse_args().runs}
CPU Threads: {parser.parse_args().threads}
GPU Acceleration: {parser.parse_args().gpu}
Seed: {parser.parse_args().seed}
Prompt: {parser.parse_args().prompt}

Eval Tokens per second:
{create_table(denorm, "eval")}

Prompt Tokens per second:
{create_table(denorm, "prompt")}
            """
        )
    else:
        print(
            f"""Runs: {parser.parse_args().runs}
CPU Threads: {parser.parse_args().threads}
GPU Acceleration: {parser.parse_args().gpu}
Model: {os.path.basename(parser.parse_args().model)}
Seed: {parser.parse_args().seed}
Prompt: {parser.parse_args().prompt}
{llama_bench.run_summary(results)}
            """
        )


def denormalize_results(results):
    """Denormalize benchmark results.

    Args:
        results (dict): Benchmark results.

    Returns:
        list: Denormalized benchmark results.
    """
    table = []

    for result in results:
        table.append(
            {
                "name": result["name"],
                "parameters": result["parameters"],
                "quant": result["quant"],
                "eval_fastest": result["data"]["eval"]["fastest"],
                "eval_slowest": result["data"]["eval"]["slowest"],
                "eval_mean": result["data"]["eval"]["mean"],
                "eval_median": result["data"]["eval"]["median"],
                "prompt_fastest": result["data"]["prompt"]["fastest"],
                "prompt_slowest": result["data"]["prompt"]["slowest"],
                "prompt_mean": result["data"]["prompt"]["mean"],
                "prompt_median": result["data"]["prompt"]["median"],
            }
        )
    return table


def create_table(denorm, type):
    """Create table of benchmark results.

    Args:
        denorm (list): Denormalized benchmark results.
        type (str): Type of benchmark results.

    Returns:
        str: Table of benchmark results.
    """
    table = [["Model", "Params", "Quant", "Fastest", "Slowest", "Mean", "Median"]]

    for result in denorm:
        table.append(
            [
                result["name"],
                result["parameters"],
                result["quant"],
                result[f"{type}_fastest"],
                result[f"{type}_slowest"],
                result[f"{type}_mean"],
                result[f"{type}_median"],
            ]
        )

    return tabulate(table, headers="firstrow", tablefmt="github")
