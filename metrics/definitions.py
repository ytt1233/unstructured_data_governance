METRIC_DEFINITIONS = {
    "removed_ratio": {
        "formula": "removed_chars / raw_length * 100",
        "description": (
            "Percentage of characters removed during cleaning."
        ),
        "interpretation": (
            "Higher values indicate more content was removed."
        ),
    },

    "avg_chunk_size": {
        "formula": (
            "sum(chunk_sizes) / chunk_count"
        ),
        "description": (
            "Average number of characters per chunk."
        ),
        "interpretation": (
            "Used to evaluate chunk granularity."
        ),
    },
}