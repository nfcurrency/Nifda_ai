from data.sources.fred import FREDClient


class SourceRegistry:
    """
    Central registry for NIFDA's external intelligence sources.
    """

    def __init__(self):
        self.sources = {}

    def register(self, name: str, client):
        self.sources[name] = client

    def get(self, name: str):
        return self.sources.get(name)

    def available_sources(self):
        return list(self.sources.keys())