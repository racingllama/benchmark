"""Provides stats from the benchmark results."""

import statistics


def summary(results):
    """Parse the results from the benchmark and returns a summary of the results.

    Args:
        results (dict): The results from the benchmark.

    Returns:
        str: A summary of the results.
    """
    prompt_tokens = ()
    eval_tokens = ()

    for run in results:
        eval_tokens += (results[run]["eval"]["tokens_per_sec"],)
        prompt_tokens += (results[run]["prompt"]["tokens_per_sec"],)

    max_eval_tokens = max(eval_tokens)
    max_prompt_tokens = max(prompt_tokens)
    min_eval_tokens = min(eval_tokens)
    min_prompt_tokens = min(prompt_tokens)
    mean_eval_tokens = statistics.mean(eval_tokens)
    mean_prompt_tokens = statistics.mean(prompt_tokens)
    median_eval_tokens = statistics.median(eval_tokens)
    median_prompt_tokens = statistics.median(prompt_tokens)

    return f"""\
Prompt Tokens Per Second:
Fastest: {min_prompt_tokens:.2f}
Slowest: {max_prompt_tokens:.2f}
Mean:    {mean_prompt_tokens:.2f}
Median:  {median_prompt_tokens:.2f}

Eval Tokens Per Second:
Fastest: {min_eval_tokens:.2f}
Slowest: {max_eval_tokens:.2f}
Mean:    {mean_eval_tokens:.2f}
Median:  {median_eval_tokens:.2f}
    """
