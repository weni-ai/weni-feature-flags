import requests


from weni_feature_flags.integrations.settings import (
    GROWTHBOOK_CLIENT_KEY,
    GROWTHBOOK_REQUESTS_TIMEOUT,
    GROWTHBOOK_HOST,
)


class GrowthBookClient:
    """
    Client to interact with the GrowthBook API.
    """

    def __init__(self):
        self.client_key = GROWTHBOOK_CLIENT_KEY
        self.host = GROWTHBOOK_HOST
        self.timeout = GROWTHBOOK_REQUESTS_TIMEOUT

    def get_features(self):
        """
        Get feature flags definitions from GrowthBook API.
        """

        url = f"{self.host}/api/features/{self.client_key}"

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                "Error getting feature flags definitions from GrowthBook API: %s", e
            )

        response = response.json()
        features = response.get("features", {})

        return features
