"""
Main entry point for the application."""
import pathlib
from loguru import logger
import fire
from security import save_env_var, load_env_var
from tqdm import tqdm
from nvd_api import fetch_data_with_CVE_number
from time import sleep


class App(object):
    """
    Main entry of the application."""

    def __init__(self):
        logger.info("Initializing the application")

    def fetch(self, csv_path: pathlib.Path):
        """ Main function to fetch the data from the remote API and save it to ./data."""
        logger.info(f"Fetching data from {csv_path}")
        with open(csv_path, "r") as f:
            cve_numbers = f.readlines()
        with tqdm(total=len(cve_numbers), desc="Processing CVEs") as pbar:
            for cve in cve_numbers:
                fetch_data_with_CVE_number(cve.strip())
                pbar.update(1)
                # NOTE: follow the best practice of API rate limiting here: https://nvd.nist.gov/developers/start-here
                sleep(3)
        logger.info(f"Successfully fetched all data from {csv_path}")

    def export(self, output_path: pathlib.Path):
        """ Main function to export the data to the remote API."""
        logger.info(f"Exporting data to {output_path}")
        logger.exception("Export function not implemented yet")
        raise NotImplementedError("Export function not implemented yet")

    def hello(self):
        logger.info("Hello, World!")


class Register(object):
    """
    Register credentials for the remote APIs."""

    def opencve(self, username: str, password: str):
        """ To save credentials for OpenCVE."""
        logger.info(f"Registering a new user {username} for OpenCVE")
        save_env_var("OPENCVE_USERNAME", username)
        save_env_var("OPENCVE_PASSWORD", password)
        logger.info(f"Successfully registered a new user {
                    username} for OpenCVE")
        return

    def github(self, token: str):
        """ To save credentials for Github."""
        logger.info(f"Registering a new user for Github")
        save_env_var("GITHUB_TOKEN", token)
        logger.info(f"Successfully registered a new user for Github")
        return

    def nvd(self, token: str):
        logger.info(f"Registering a new user for NVD")
        save_env_var("NVD_TOKEN", token)
        logger.info(f"Successfully registered a new user for NVD")
        return


if __name__ == "__main__":
    fire.Fire({'run': App, 'register': Register})
