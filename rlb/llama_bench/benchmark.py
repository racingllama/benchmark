"""llama.cpp benchmark."""

from io import StringIO
from llama_cpp import Llama
from wurlitzer import pipes


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

    def run(self, prompt):
        """Run benchmark.

        Returns:
            str: Benchmark results.
        """
        with pipes() as (out, err):
            self._llama.reset()
            self._llama(prompt, max_tokens=1024)

        stats = err.read()

        print(stats)
        return self.parse_timings(stats)

    def multiple_runs(self, prompt, runs):
        """Run benchmark multiple times.

        Args:
            prompt (str): Prompt.
            runs (int): Number of runs.

        Returns:
            list: Benchmark results.
        """
        results = {}
        for run in range(runs):
            results[run] = self.run(prompt)
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
                values = line.split("=")[1].strip().split()
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
