"""This represents a pre-existing script which a user wants to
automate through the Control Room.

Note: the Excel functionality is mocked with RPA framework's Excel
library, but other excel libraries might be used.
"""
import logging
import os
import sys
import requests
from pathlib import Path
from RPA.Excel.Files import Files

# Define paths
OUTPUT = Path("./output")
OUTPUT.mkdir(exist_ok=True)
LOG_PATH = OUTPUT / "out.log"
LOG_PATH.touch(exist_ok=True)

# Configure logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
term_handler = logging.StreamHandler(sys.stdout)
term_handler.setLevel(logging.INFO)
term_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
term_handler.setFormatter(term_format)
LOG.addHandler(term_handler)
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_format)
LOG.addHandler(file_handler)

# Initialize RPA library for use.
EXCEL = Files()


def mock_execution_against_domain(domain: str, credentials: dict) -> None:
    """Mocks executing against a domain."""

    LOG.info("Executing against '%s'", domain)
    LOG.info(
        "Using username '%s' and password '%s' at '%s'",
        credentials["user"],
        credentials["password"],
        credentials["url"],
    )
    response = requests.get(credentials["url"])
    LOG.info("Received response: <%s>", response.status_code)


def mock_execution_with_excel(file: Path) -> Path:
    """Reads the file, echoing each row into the log,
    then modifies column 2 and saves it as a new file
    to output. Returns the path to the new file.
    """
    LOG.info("Reading Excel file at '%s'", file)
    EXCEL.open_workbook(file)
    rows = EXCEL.read_worksheet(header=True)
    output_file = OUTPUT / "output.xlsx"
    EXCEL.create_workbook(str(output_file))
    EXCEL.set_cell_value(1, 1, list(rows[0].keys())[0])
    EXCEL.set_cell_value(1, 2, list(rows[0].keys())[1])
    for row in rows:
        LOG.info("Row contents are: %r", row)
        row["Value"] += 10
        LOG.info("Row updated")
    EXCEL.append_rows_to_worksheet(rows)
    EXCEL.save_workbook()
    return output_file


def mock_python_logic(path: Path) -> tuple[Path, int]:
    """Represents the Python logic, returns the path to a
    report and an exit code.
    """
    LOG.info("Executing SQL script using input file at %s", path)
    new_file = mock_execution_with_excel(path)
    domain_one_creds = {
        "user": os.getenv("DOMAIN_ONE_USER", "user1"),
        "password": os.getenv("DOMAIN_ONE_PASSWORD", "pass1"),
        "url": os.getenv("DOMAIN_ONE_URL", "https://www.example.com"),
    }
    mock_execution_against_domain("domain_one", domain_one_creds)
    domain_two_creds = {
        "user": os.getenv("DOMAIN_TWO_USER", "user2"),
        "password": os.getenv("DOMAIN_TWO_PASSWORD", "pass2"),
        "url": os.getenv(
            "DOMAIN_TWO_URL",
            (
                "https://file-examples.com/storage/fe783a5cbb6323602a28c66/"
                "2017/10/file_example_PNG_500kB.png"
            ),
        ),
    }
    mock_execution_against_domain("domain_two", domain_two_creds)

    LOG.info("Execution of Python script complete.")
    return new_file, 0


if __name__ == "__main__":
    # This would be the original script entrance.
    mock_python_logic(Path("./input"))
