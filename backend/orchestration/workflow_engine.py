from __future__ import annotations

from datetime import datetime

def analyze_incident(raw_logs: str, incident_type: str, service_name: str, severity: str) -> dict:
    normalized_logs = (raw_logs or "").lower()
    normalized_type = (incident_type or "").lower()

    probable_cause = "Unknown"
    confidence = 0.5
    analysis_severity = severity or "MEDIUM"

    keyword_map = [
        ("redis", "Redis timeout or connectivity issue", 0.82),
        ("timeout", "Upstream timeout", 0.74),
        ("database", "Database connection issue", 0.78),
        ("auth", "Authentication failure", 0.7),
        ("payment", "Payment processing failure", 0.7),
        ("memory", "Memory pressure or leak", 0.68),
        ("cpu", "High CPU or resource saturation", 0.66),
    ]

    for keyword, cause, score in keyword_map:
        if keyword in normalized_logs or keyword in normalized_type:
            probable_cause = cause
            confidence = score
            break

    if "fatal" in normalized_logs or "critical" in normalized_logs:
        analysis_severity = "HIGH"
    elif "warn" in normalized_logs and analysis_severity == "HIGH":
        analysis_severity = "MEDIUM"

    analysis_summary = (
        f"Heuristic analysis for {service_name}. "
        f"Detected keywords in logs/type: {incident_type}."
    )

    return {
        "probable_cause": probable_cause,
        "confidence": confidence,
        "analysis_severity": analysis_severity,
        "analysis_summary": analysis_summary,
        "analyzed_at": datetime.utcnow(),
    }
