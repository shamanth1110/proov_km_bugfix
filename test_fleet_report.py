# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_does_not_crash_without_last_service_km():
    # A car with no "last_service_km" key must not cause a KeyError.
    # VOS-7788 has never had a reading recorded; the report must still run.
    fleet = [{"id": "VOS-7788", "odometer": 92000}]
    result = fleet_summary(fleet)
    assert result["count"] == 1
    # No last_service_km means 0 km since service → not due.
    assert result["due"] == 0
