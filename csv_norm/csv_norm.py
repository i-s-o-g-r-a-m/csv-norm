import logging
import re
import sys
from collections import OrderedDict
from csv import DictReader as CsvDictReader
from csv import DictWriter as CsvDictWriter
from typing import Any, Dict, Generator

import pendulum


# TODO add more tests
# TODO add docstrings


DEFAULT_ENCODING = "UTF-8"
ZIPCODE_LENGTH = 5
TIMESTAMP_FORMAT = "M/D/YY HH:mm:ss A"
DURATION_REGEX = re.compile(
    r"(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+?)\.(?P<milliseconds>\d+)"
)
INPUT_TZ = "US/Pacific"
OUTPUT_TZ = "US/Eastern"


logging.basicConfig(
    stream=sys.stderr, level=logging.WARNING, format="%(levelname)s %(message)s"
)


def norm_timestamp(timestamp: str) -> str:
    ts = pendulum.from_format(timestamp, TIMESTAMP_FORMAT, tz=INPUT_TZ)
    return ts.in_timezone(OUTPUT_TZ).to_iso8601_string()


def norm_zipcode(zipcode: str) -> str:
    return zipcode.zfill(ZIPCODE_LENGTH)


def norm_name(name: str) -> str:
    return name.upper()


def norm_duration(duration: str) -> float:
    parsed = DURATION_REGEX.match(duration)
    if not parsed:
        raise ValueError(f"Could not parse duration: {duration}")
    total_seconds = pendulum.duration(
        **{k: int(v) for (k, v) in parsed.groupdict().items()}
    ).total_seconds()
    return total_seconds


transforms = {
    "Timestamp": norm_timestamp,
    "ZIP": norm_zipcode,
    "FullName": norm_name,
    "FooDuration": norm_duration,
    "BarDuration": norm_duration,
}


def normalize(csv_reader: CsvDictReader) -> Generator[Dict, None, None]:
    for row_index, row in enumerate(csv_reader):
        norm_row = OrderedDict()  # type: Dict[str, Any]
        bad_cols = []

        for col, val in row.items():
            transform = transforms.get(col)
            try:
                if col == "TotalDuration":
                    norm_row[col] = norm_row["FooDuration"] * norm_row["BarDuration"]
                else:
                    norm_row[col] = transform(val) if transform else val
            except:
                bad_cols.append(col)

        if bad_cols:
            logging.warning(
                "Dropping row %d, could not normalize values in columns: %s",
                row_index + 1,
                ", ".join(bad_cols),
            )
        else:
            yield norm_row


def main(input_file, output_file) -> None:
    csv_reader = CsvDictReader(input_file)
    if not csv_reader.fieldnames:
        raise ValueError("Could not parse input CSV data")
    csv_writer = CsvDictWriter(
        output_file, fieldnames=csv_reader.fieldnames, lineterminator="\n"
    )
    csv_writer.writeheader()
    for row in normalize(csv_reader):
        csv_writer.writerow(row)


if __name__ == "__main__":
    sys.stdin.reconfigure(encoding=DEFAULT_ENCODING, errors="replace")
    sys.stdout.reconfigure(encoding=DEFAULT_ENCODING)
    main(input_file=sys.stdin, output_file=sys.stdout)
