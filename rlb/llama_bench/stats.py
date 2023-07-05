"""Provides stats from the benchmark results."""

import statistics


def run_summary(results):
    """Parse the results from the benchmark and returns a summary of the results.

    Args:
        results (dict): The results from the benchmark.

    Returns:
        str: A summary of the results.
    """
    stats = calculate_stats(results)

    return f"""\
Prompt Tokens Per Second:
Fastest: {stats["prompt"]["fastest"]:.2f}
Slowest: {stats["prompt"]["slowest"]:.2f}
Mean:    {stats["prompt"]["mean"]:.2f}
Median:  {stats["prompt"]["median"]:.2f}

Eval Tokens Per Second:
Fastest: {stats["eval"]["fastest"]:.2f}
Slowest: {stats["eval"]["slowest"]:.2f}
Mean:    {stats["eval"]["mean"]:.2f}
Median:  {stats["eval"]["median"]:.2f}
    """


def calculate_stats(results):
    """Calculate the stats from the benchmark results.

    Args:
        results (dict): The results from the benchmark.

    Returns:
        dict: The stats from the benchmark.
    """
    prompt_tokens = ()
    eval_tokens = ()
    output = {}

    for run in results:
        eval_tokens += (results[run]["eval"]["tokens_per_sec"],)
        prompt_tokens += (results[run]["prompt"]["tokens_per_sec"],)

    output["prompt"] = {}
    output["prompt"]["fastest"] = max(prompt_tokens)
    output["prompt"]["slowest"] = min(prompt_tokens)
    output["prompt"]["mean"] = statistics.mean(prompt_tokens)
    output["prompt"]["median"] = statistics.median(prompt_tokens)
    output["eval"] = {}
    output["eval"]["fastest"] = max(eval_tokens)
    output["eval"]["slowest"] = min(eval_tokens)
    output["eval"]["mean"] = statistics.mean(eval_tokens)
    output["eval"]["median"] = statistics.median(eval_tokens)

    return output
