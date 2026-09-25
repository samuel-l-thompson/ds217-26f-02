#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Useable enocounter are those with the form of patient ID, date, systolic.  Systolic must be an integer between 50 and 300.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    with data_path.open(encoding="utf-8") as data_file:
        rows = data_file.readlines()
    encounters = []
    skipped = 0
    for row in rows[1:]:  # skip the header row
        fields = row.strip().split(",")
        if len(fields) != 3:  # if not three filds, skip the row and count it as skipped
            print(f"skipping  row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, date, systolic_raw = (
            fields  # define our three variables based on the fields
        )

        try:
            systolic = int(
                systolic_raw
            )  # ensure that systolic is an integer, if not, skip the row and count it as skipped
        except ValueError as error:
            print(f"skipping {patient_id} with non-integer systolic: {error}")
            skipped += 1
        else:
            if (
                systolic < 50 or systolic > 300
            ):  # ensure that systolic is within a plausible range, if not, skip the row and count it as skipped
                print(f"skipping {patient_id} with implausible systolic: {systolic}")
                skipped += 1
            else:
                encounters.append(
                    {"patient_id": patient_id, "date": date, "systolic": systolic}
                )
    return encounters, skipped


# follow up cutoff function, takes a user input and ensures it is a valid integer, if not, it will keep asking for a valid input until it gets one. It will return the valid integer.
def follow_up_cutoff():
    while True:  # keeps running until we have a valid return
        typed_cutoff = input(
            "Cut off for systolic BP at or above which will flag patient for follow up, enter in mmHG: "
        )
        if not typed_cutoff or not typed_cutoff.isdigit():
            print("Invalid input. Please enter a valid integer for the cutoff.")
            continue
        cutoff = int(typed_cutoff)
        return cutoff


# follow up reason
def follow_up_reason():  # takes a user input and ensures it is a valid string, if not, it will keep asking for a valid input until it gets one. It will return the valid string.
    while True:
        typed_reason = input("Reason for follow up parameter: ")
        if not typed_reason:
            continue
        if (
            "\n" in typed_reason or "\r" in typed_reason
        ):  # ensures reason is a single line, if not, print error message and return                print("Invalid input. Please enter a single line for the reason.")
            continue
        if not (
            20 <= len(typed_reason) <= 300
        ):  # ensures reason is between 20 and 300 characters, if not, print error message and return
            print("Invalid input. Please enter a reason between 20 and 300 characters.")
            continue
        reason = typed_reason
        return reason


def main():
    """TODO: describe the two artifacts this writes."""
    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)  # prevents error if already created/exists.
    vitals_path = output_dir / "vitals_report.txt"  # defines our output/vital.txt
    encounters, skipped = read_encounters(
        DATA_PATH
    )  # obtain usable encounters and skipped rows from read_encounters function
    with open(vitals_path, "w", encoding="utf-8") as file:
        file.write(f"Usable encounters: {len(encounters)}\n")
        file.write(f"Skipped rows: {skipped}\n")
        file.write(f"Patients seen: {count_patients(encounters)}\n")
        file.write(
            f"Mean systolic: {mean_systolic(systolic_readings(encounters))} mmHG\n"
        )
        file.write(f"Highest systolic: {max(systolic_readings(encounters))} mmHG\n")
        file.write(f"Lowest systolic: {min(systolic_readings(encounters))} mmHG\n")

    # read the file back and print it, so you can see what was saved.
    with vitals_path.open("r", encoding="utf-8") as file:
        print(file.read())

    # choose your follow-up cutoff, then write output/followup_list.txt
    # with the Cutoff line, the Reason line, and one patient ID per line.

    # write the followup_list.txt file
    followup_path = (
        output_dir / "followup_list.txt"
    )  # defines our output/followup_list.txt
    with open(followup_path, "w", encoding="utf-8") as file_fu:
        cut_off = (
            follow_up_cutoff()
        )  # uses the follow_up_cutoff function to get the cutoff value
        file_fu.write(f"Cutoff: {cut_off} mmgHG\n")
        file_fu.write(
            f"Reason: {follow_up_reason()}\n"
        )  # uses the follow_up_reason function to get the reason and write it to the file
        for patient in patients_at_or_above(
            encounters, cut_off
        ):  # uses the patients_at_or_above function to get the patient IDs and write them to the file
            file_fu.write(f"{patient}\n")


# Usable encounters: <how many data rows were usable>
# Skipped rows: <how many data rows were skipped>
# Patients seen: <how many different patient IDs appear among the usable encounters>
# Mean systolic: <mean of every usable reading> mmHg
# Highest systolic: <largest usable reading> mmHg
# Lowest systolic: <smallest usable reading> mmHg

if __name__ == "__main__":
    main()
