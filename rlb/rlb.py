#!/usr/bin/env python3
"""Racing Llama Benchmark - a benchmarking application for llama.cpp."""

import sysinfo

if __name__ == "__main__":
    print(
        f"""
Racing Llama Benchmark

System Information:
{sysinfo.basic()}"""
    )
