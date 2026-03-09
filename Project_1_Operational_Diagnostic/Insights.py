from __future__ import annotations

import os
from typing import Dict, Any

try:
    import ollama
except ImportError:
    ollama = None


def _fallback_report(summary_data: Dict[str, Any]) -> str:
    metrics = summary_data["metrics"]
    signals = summary_data["signals"]
    top_category = summary_data.get("top_category")

    findings = []
    findings.append(
        f"Total revenue for the selected period is ${metrics['total_revenue']:,.0f} "
        f"across {metrics['total_transactions']:,} transactions."
    )

    findings.append(
        f"Average revenue per transaction is "
        f"${metrics['avg_revenue_per_transaction']:,.2f}."
    )

    if top_category:
        findings.append(
            f"The top category is {top_category['name']}, contributing "
            f"{top_category['revenue_share']:.1%} of total revenue."
        )

    if signals.get("trend_signal"):
        findings.append(signals["trend_signal"])

    if signals.get("anomaly_signal"):
        findings.append(signals["anomaly_signal"])

    if signals.get("concentration_signal"):
        findings.append(signals["concentration_signal"])

    return (
        "Executive Summary\n"
        "The business shows a structured operational revenue profile for the selected period.\n\n"
        "Key Findings\n- " + "\n- ".join(findings) + "\n\n"
        "Operational Risks\n- Review concentration and anomaly signals if present.\n\n"
        "Strategic Opportunities\n- Focus on categories and periods with the strongest growth and stability.\n\n"
        "Recommended Focus Areas\n- Monitor rolling revenue trends and category contribution closely."
    )


def generate_consultant_report(summary_data: Dict[str, Any]) -> str:
    if ollama is None:
        return _fallback_report(summary_data)

    model_name = os.getenv("OLLAMA_MODEL", "llama3")

    prompt = f"""
You are an operational consultant.

Write a concise operational diagnostic report using this exact structure:

Executive Summary
Key Findings
Operational Risks
Strategic Opportunities
Recommended Focus Areas

Use the following metrics and signals:
{summary_data}

Be concrete, concise, and professional.
Do not invent data.
"""

    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception:
        return _fallback_report(summary_data)
