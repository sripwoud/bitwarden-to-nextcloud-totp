import json
import argparse
from urllib.parse import urlparse, parse_qs

DEFAULT_BITWARDEN_FILE_PATH = "bitwarden.json"
DEFAULT_NEXTCLOUD_OTP_FILE_PATH = "accounts.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Bitwarden TOTP to FreeOTP accounts"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=DEFAULT_BITWARDEN_FILE_PATH,
        help="Bitwarden export file path",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=DEFAULT_NEXTCLOUD_OTP_FILE_PATH,
        help="Nextcloud OTP Manager import file path",
    )
    return parser.parse_args()


def read_bitwarden(file_path: str = DEFAULT_BITWARDEN_FILE_PATH):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON file: {file_path}")
        exit(1)


def parse_totp(login_item: dict):
    secret_or_url = login_item.get("login", {}).get("totp").replace(" ", "")
    return parse_qs(urlparse(secret_or_url).query).get("secret", [secret_or_url])[0]


def parse_bitwarden(file_path: str = DEFAULT_BITWARDEN_FILE_PATH):
    return [
        {
            "issuer": item.get("login", {}).get("username") or "",
            "name": item["name"],
            "secret": parse_totp(item),
        }
        for item in read_bitwarden(file_path)["items"]
        if "login" in item and item.get("login", {}).get("totp")
    ]


def create_account(issuer: str, name: str, secret: str):
    return {
        "algorithm": 0,
        "counter": None,
        "digits": 6,
        "icon": "default",
        "issuer": issuer,
        "name": name,
        "period": 30,
        "secret": secret,
        "type": "totp",
    }


def create_accounts(input_file_path: str = DEFAULT_BITWARDEN_FILE_PATH):
    accounts = parse_bitwarden(input_file_path)
    return [
        create_account(account["issuer"], account["name"], account["secret"])
        for account in accounts
    ]


def write_accounts(
    input_file_path: str = DEFAULT_BITWARDEN_FILE_PATH,
    output_file_path: str = DEFAULT_NEXTCLOUD_OTP_FILE_PATH,
):
    accounts = create_accounts(input_file_path)
    count = len(accounts)
    with open(output_file_path, "w") as f:
        json.dump({"accounts": accounts}, f, indent=4)

    print(f"Successfully wrote {count} TOTP accounts to {output_file_path}")


if __name__ == "__main__":
    args = parse_args()
    bitwarden_file_path = args.input
    nextcloud_otp_file_path = args.output
    write_accounts(bitwarden_file_path, nextcloud_otp_file_path)
