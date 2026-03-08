from src.variance_engine import calculate_variance
from src.reorder_engine import generate_reorder_recommendations

def build_reports():

    variance_report = calculate_variance()
    reorder_report = generate_reorder_recommendations()

    variance_report.to_csv(
        "outputs/asset_variance_report.csv",
        index=False
    )

    reorder_report.to_csv(
        "outputs/reorder_recommendations.csv",
        index=False
    )

    return variance_report, reorder_report
