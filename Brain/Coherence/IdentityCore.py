class IdentityCore:
    """
    Defines personality + behavior style
    """

    def __init__(self):
        self.personality = {
            "tone": "calm",
            "style": "precise",
            "behavior": "proactive",
            "verbosity": "medium"
        }

    def set_trait(self, key, value):
        self.personality[key] = value

    def get_trait(self, key):
        return self.personality.get(key)

    def get_full_identity(self):
        return self.personality

    def reset_identity(self):
        self.__init__()