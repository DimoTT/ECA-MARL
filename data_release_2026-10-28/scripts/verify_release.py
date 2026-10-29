"""Verify this supporting-materials collection without third-party packages."""

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_rows(relative_path):
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def verify():
    checksums = {}
    for line in (ROOT / "SHA256SUMS.txt").read_text(encoding="ascii").splitlines():
        expected, name = line.split("  ", 1)
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe manifest path: {name}")
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid checksum: {name}")
        if name in checksums:
            raise ValueError(f"Duplicate manifest path: {name}")
        checksums[name] = expected
        if digest(ROOT / relative) != expected:
            raise ValueError(f"Checksum mismatch: {name}")

    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS.txt"
        and "__pycache__" not in path.parts
    }
    if actual != set(checksums):
        raise ValueError(f"Manifest coverage differs: {actual ^ set(checksums)}")

    figures = csv_rows("metadata/figure_manifest.csv")
    if [row["figure"] for row in figures] != [f"Fig{i}" for i in range(1, 15)]:
        raise ValueError("Expected the current 14 figures in order")
    for row in figures:
        if digest(ROOT / row["primary_file"]) != row["primary_sha256"]:
            raise ValueError(f"Primary figure mismatch: {row['figure']}")
        if digest(ROOT / row["display_file"]) != row["display_sha256"]:
            raise ValueError(f"Display figure mismatch: {row['figure']}")

    parameters = csv_rows("tables/table1_simulation_parameters.csv")
    setup = (ROOT / "documentation/reported_setup.tex").read_text(encoding="utf-8")
    table = setup.split(r"\begin{tabular}", 1)[1].split(r"\end{tabular}", 1)[0]
    expected_rows = []
    for line in table.splitlines():
        if " & " in line and line.rstrip().endswith(r"\\"):
            left, right = line.rstrip()[:-2].split(" & ", 1)
            if left.strip() != "Parameter":
                expected_rows.append((left.strip(), right.strip()))
    transcribed = [(row["parameter"], row["reported_value"]) for row in parameters]
    if len(parameters) != 12 or transcribed != expected_rows:
        raise ValueError("Parameter CSV differs from the included Table 1 excerpt")

    metadata = json.loads((ROOT / "metadata/dataset_metadata.json").read_text(encoding="utf-8"))
    creators = [creator["name"] for creator in metadata["creators"]]
    if len(creators) != 6 or len(set(creators)) != 6 or "Author Name" in creators:
        raise ValueError("Expected six actual authors, with no template placeholder")
    if metadata["coverage"]["raw_simulation_data_included"]:
        raise ValueError("This collection must not claim to contain raw simulation data")
    if metadata["coverage"]["experimental_numerical_results_included"]:
        raise ValueError("This collection must not claim to contain missing numerical results")
    print(f"PASS: {len(checksums)} files, 14 figures, 12 exact parameter rows.")
    print("Scope: partial supporting materials; no raw runs or numerical result tables.")
    return checksums


if __name__ == "__main__":
    verify()
