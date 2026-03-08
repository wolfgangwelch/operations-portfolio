from src.reporting_engine import build_reports

def run_pipeline():

    variance, reorder = build_reports()

    print("Inventory reports generated.")
    print("Variance rows:", len(variance))
    print("Reorder recommendations:", len(reorder))

if __name__ == "__main__":
    run_pipeline()
