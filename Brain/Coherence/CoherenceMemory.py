class CoherenceMemory:
    """
    Tracks past decisions for consistency
    """

    def __init__(self):
        self.history = []

    def store(self, event: dict):
        self.history.append(event)

    def get_recent(self, n=5):
        return self.history[-n:]

    def clear(self):
        self.history = []