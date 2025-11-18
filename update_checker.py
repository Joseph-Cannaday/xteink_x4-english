#!/usr/bin/env python3
"""
Queries the api for updates
"""
import requests
import argparse
import json

def craft_query(cur_version="V3.0.2", device_type="ESP32C3", device_id="1111"):
    req_string = f"http://gotaserver.xteink.com/api/check-update?current_version={cur_version}&device_type={device_type}&device_id={device_id}"
    return req_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog="python3 update_checker.py",
                        description="Queries the official API for firmware updates")

    parser.add_argument('-i', '--id', help='device_id', default="1111")
    parser.add_argument('-t', '--device_type', help='device type i.e. ESP32C3', default="ESP32C3")
    parser.add_argument('-v', '--version', help='Current version of firmware loaded on your device', default="V3.0.2")
    args = parser.parse_args()

    req_string = craft_query(args.version, args.device_type, args.id)
    json_dict = json.loads(requests.get(req_string).text)
    if json_dict["message"] == "Update available":
        print(json_dict["message"])
        version = json_dict["data"]["version"]
        print(f"The latest version is: {version}")
        print(f"It can be downloaded here: {json_dict["data"]["download_url"]}")
        print("WARNING: This is only the app0 partition, do not overwrite other sectors of the firmware")
    else:
        print("You are already on the current firmware version")
