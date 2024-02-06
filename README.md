# Transfer [Bitwarden](https://bitwarden.com/) TOTP to [NextCloud OTP Manager](https://apps.nextcloud.com/apps/otpmanager)

1. Export your Bitwarden vault to a JSON file
2. Run the script with the path to the JSON file as an argument
    ```commandline
    python main.py -i /path/to/bitwarden.json [-o /path/to/output.json]
   ```

3. Import the output JSON file into NextCloud OTP Manager