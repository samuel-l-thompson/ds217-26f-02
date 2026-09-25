"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic blood pressure reading stored in encounter records."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Return the systolic blood pressure reading stored in encounter records."""
    if not readings:
        return None
    return round((sum(readings) / len(readings)), 1)


def count_patients(encounters):
    """Return the number of patient IDs that are unique."""
    unique_patients = {encounter["patient_id"] for encounter in encounters}
    return len(unique_patients)


def patients_at_or_above(encounters, cutoff):
    """Will keep each patient whose systolic reading is at or above the cutoff."""
    above_cutoff = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            above_cutoff.append(encounter["patient_id"])
    return above_cutoff
