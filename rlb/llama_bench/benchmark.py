"""llama.cpp benchmark."""

import gc
import re
from llama_cpp import Llama
from wurlitzer import pipes
from .prompts import prompts


class Benchmark:
    """llama.cpp benchmark."""

    def __init__(self, model, threads, seed, gpu):
        """Load model.

        Args:
            model (str): Path to model.
        """
        if gpu:
            ngl = 1
        else:
            ngl = 0

        self._llama = Llama(
            model_path=model, n_gpu_layers=ngl, seed=seed, n_threads=threads
        )

        self.run("warmup", verbose=False)

    def __del__(self):
        """Delete model."""
        # This does successfully free the memory. However, llama.cpp does not
        # notice and still reports the memory as used, causing it to complain
        # about memory usage when running benchmarks against multiple models.
        self._llama.__del__()
        gc.collect()

    def run(self, prompt, verbose=True):
        """Run benchmark.

        Returns:
            dict: Benchmark results.
        """
        output = {}
        with pipes() as (_, err):
            self._llama.reset()
            result = self._llama(prompt, max_tokens=1024)

        stats = err.read()

        if verbose:
            print(stats)
            print(f"Prompt: {prompt}")
            print(result["choices"][0]["text"])

        output["result"] = result

        output.update(self.parse_timings(stats))
        return output

    def multiple_runs(self, runs):
        """Run benchmark multiple times.

        Args:
            runs (int): Number of runs.

        Returns:
            list: Benchmark results.
        """
        results = {}
        prompt = prompts()
        for run in range(runs):
            results[run] = self.run(next(prompt))

        return results

    def parse_timings(self, input):
        """Parse timings from benchmark output.

        Args:
            input (str): Benchmark output.

        Returns:
            dict: Timings.
        """
        timings = {}
        lines = input.split("\n")
        for line in lines:
            if "llama_print_timings:" in line:
                label = line.split()[1]
                mod_line = re.sub(r"\((\d+)", r"( \1", line)
                values = mod_line.split("=")[1].strip().split()
                if label in ["load", "total"]:
                    timings[label] = {"time": float(values[0])}
                else:
                    timings[label] = {
                        "ms_per_token": float(values[6]),
                        "runs": int(values[3]),
                        "time": float(values[0]),
                        "tokens_per_sec": float(values[10]),
                    }
        return timings
