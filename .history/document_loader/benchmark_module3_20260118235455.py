from semantic_search import semantic_search

TEST_QUERIES = [
    "salary processing",
    "employee leave policy",
    "marketing campaign performance",
    "software deployment pipeline",
    "company financial report"
]

def run_benchmark():
    latencies = []

    for query in TEST_QUERIES:
        print("\n" + "=" * 60)
        latency, _ = semantic_search(query)
        latencies.append(latency)

    avg_latency = sum(latencies) / len(latencies)
    print("\n📊 BENCHMARK SUMMARY")
    print("Total Queries:", len(TEST_QUERIES))
    print("Average Latency (ms):", round(avg_latency, 2))


if __name__ == "__main__":
    run_benchmark()
