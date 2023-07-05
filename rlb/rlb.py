#!/usr/bin/env python3
"""Racing Llama Benchmark Alpha - a benchmarking application for llama.cpp."""

import argparse
import llama_bench
import sysinfo
import output

parser = argparse.ArgumentParser()
parser.add_argument(
    "-g", "--gpu", action="store_true", default=False, help="Enable GPU acceleration."
)
parser.add_argument(
    "-r", "--runs", type=int, default=5, help="Number of runs to perform."
)
parser.add_argument(
    "-s", "--seed", type=int, default=-1, help="Seed to use for benchmarking."
)
parser.add_argument(
    "-t",
    "--threads",
    type=int,
    default=sysinfo.threads(),
    help="Number of threads to use for benchmarking.",
)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-m", "--model", type=str, help="Model to use for benchmarking.")
group.add_argument("-d", "--directory", type=str, help="Directory of models to use.")


if __name__ == "__main__":
    if parser.parse_args().model:
        llm = llama_bench.Benchmark(
            model=parser.parse_args().model,
            threads=parser.parse_args().threads,
            seed=parser.parse_args().seed,
            gpu=parser.parse_args().gpu,
        )
        results = llm.multiple_runs(parser.parse_args().runs)
        output.print_results(results, parser, type="model")

    elif parser.parse_args().directory:
        results = []
        models = llama_bench.parse_directory(parser.parse_args().directory)
        for model in models:
            print(
                f"Running benchmark for {model['name']} ({model['quant']} {model['parameters']})"
            )
            try:
                llm = llama_bench.Benchmark(
                    model=model["path"],
                    threads=parser.parse_args().threads,
                    seed=parser.parse_args().seed,
                    gpu=parser.parse_args().gpu,
                )
            except AssertionError:
                print(f"Could not load model {model['path']}")
                continue

            result = llm.multiple_runs(
                parser.parse_args().prompt, parser.parse_args().runs
            )

            del llm

            data = llama_bench.calculate_stats(result)

            results.append(
                {
                    "name": model["name"],
                    "quant": model["quant"],
                    "parameters": model["parameters"],
                    "data": data,
                }
            )
        output.print_results(results, parser, type="directory")
