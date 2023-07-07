"""Output benchmark results."""

import pkg_resources
import rlb.llama_bench as llama_bench
import rlb.sysinfo as sysinfo
import os
from tabulate import tabulate


def header():
    """Print benchmark header."""
    return f"""Racing Llama Benchmark

System Information:
{sysinfo.basic()}"""


def results(results, parser, type="model"):
    """Format benchmark results.

    Args:
        results (dict): Benchmark results.
        parser (argparse.ArgumentParser): Argument parser.
        type (str): Type of benchmark results.

    Returns:
        str: Formatted benchmark results.
    """
    output = header()
    if type == "directory":
        denorm = denormalize(results)
        output += f"""Runs: {parser.parse_args().runs}
llama-cpp-python version: {pkg_resources.get_distribution("llama-cpp-python").version}
CPU Threads: {parser.parse_args().threads}
GPU Acceleration: {parser.parse_args().gpu}
Seed: {parser.parse_args().seed}

Eval Tokens per second:
{create_table(denorm, "eval")}

Prompt Tokens per second:
{create_table(denorm, "prompt")}"""
    else:
        output += f"""Runs: {parser.parse_args().runs}
llama-cpp-python version: {pkg_resources.get_distribution("llama-cpp-python").version}
CPU Threads: {parser.parse_args().threads}
GPU Acceleration: {parser.parse_args().gpu}
Model: {os.path.basename(parser.parse_args().model)}
Seed: {parser.parse_args().seed}
{llama_bench.run_summary(results)}"""
    return output


def denormalize(results):
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

    denorm_sorted = sorted(
        denorm, key=lambda d: (d["name"], d["parameters"], d["quant"])
    )

    for result in denorm_sorted:
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
