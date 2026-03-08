from src.performance_engine import summarize_performance

def run_pipeline():

    summary = summarize_performance()

    summary.to_csv(
        "outputs/performance_summary.csv",
        index=False
    )

    print("Performance summary generated.")

if __name__ == "__main__":
    run_pipeline()
