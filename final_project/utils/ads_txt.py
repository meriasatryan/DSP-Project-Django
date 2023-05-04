import os

import requests


def get_ads_txt(publisher_domain):
    """
    Retrieves the ads.txt content for the given publisher domain.

    Args:
        publisher_domain (str): The publisher domain to retrieve the ads.txt for.

    Returns:
        str: The ads.txt content as a string, or None if the request fails.
    """
    ip_address = os.environ.get("ADS_TXT")
    response = requests.get(f"http://108.61.176.250:14592/ads.txt?publisher={publisher_domain}")

    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        return None


def is_authorized(publisher_domain, ssp_id):
    """
    Determines whether the given SSP ID is authorized to sell ads for the given publisher domain.

    Args:
        publisher_domain (str): The publisher domain to check authorization for.
        ssp_id (str): The SSP ID to check authorization for.

    Returns:
        bool: True if the SSP ID is authorized to sell ads for the publisher domain, False otherwise.
    """
    ads_txt = get_ads_txt(publisher_domain)
    if ads_txt:
        lines = ads_txt.split('\n')
        for line in lines:
            parts = line.split(', ')
            if parts[1] == ssp_id:
                return True
        return False
