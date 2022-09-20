"""This is an example basic script which can be used to wrap an existing
Python script. In this example, the script being wrapped is in the
``./script`` directory and imported and called from main.
"""
import logging
import os
from pathlib import Path
import sys
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Robocorp.Vault import Vault, Secret
from RPA.Email.ImapSmtp import ImapSmtp
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP

from script.MockScript import mock_python_logic

# Define paths
OUTPUT = Path("./output")
OUTPUT.mkdir(exist_ok=True)
LOG_PATH = OUTPUT / "out.log"
LOG_PATH.touch(exist_ok=True)

# Configure logging
LOG = logging.getLogger()
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

# Initialize RPA libraries
VAULT = Vault()
WI = WorkItems()
REQUEST = HTTP()
EXCEL = Files()


def main() -> None:
    """Main script"""
    LOG.info("START")
    set_credentials("domain_one")
    set_credentials("domain_two")
    input_file, requesting_user = get_work_item_file()
    new_file, status_code = mock_python_logic(input_file)
    send_completion_email(requesting_user, status_code, new_file)
    LOG.info("END")


def set_credentials(secret_name: str) -> None:
    """Retrieves credentials from the Control Room and then
    sets those as environment variables for the script we are
    wrapping.

    You could also modify your existing script to use the
    vault directly.
    """
    secret = VAULT.get_secret(secret_name)
    LOG.debug("Setting environment variables using Vault secret '%s'", secret_name)
    os.environ[f"{secret_name.upper()}_USER"] = secret["user"]
    os.environ[f"{secret_name.upper()}_PASSWORD"] = secret["password"]
    os.environ[f"{secret_name.upper()}_URL"] = secret["url"]


def get_work_item_file() -> tuple[Path, str]:
    """Retrieves the first attached file from the work item and
    the user that emailed it into the system."""
    LOG.info("Retreiving file from work item.")
    item = WI.get_input_work_item()
    LOG.debug("Obtained work item %s.\nWork item files: \n%r", item.id, item.files)
    requesting_user = item.payload.get("email", {}).get("from", {}).get("address")
    LOG.debug("Requesting user is: %s", requesting_user)
    return Path(item.get_file(item.files[0])), requesting_user


def send_completion_email(recipient: str, status_code: int, output_file: Path) -> None:
    """Sends a completion email with the output excel file."""
    email_cred = VAULT.get_secret("email_app_password")
    client = ImapSmtp(
        smtp_server="smtp.gmail.com",
        account=email_cred["user"],
        password=email_cred["password"],
    )
    LOG.info("Authenticating to email for user '%s'", email_cred["user"])
    client.authorize_smtp()
    LOG.info("Sending email message...")
    client.send_message(
        sender=email_cred["user"],
        recipients=recipient,
        subject="Mock Python Script Output",
        body=(
            f"Python script executed with exit code {status_code}. "
            f"Please find the output report attached."
        ),
        attachments=str(output_file),
    )
    LOG.info("Email sent successfully.")


if __name__ == "__main__":
    main()
