class UnifiedState:
    """
    Central shared state (NOT connected yet)
    Holds goal, context, identity
    """

    def __init__(self):
        self.goal = None
        self.context = {}
        self.identity = {
            "name": "Jarvis",
            "mode": "assistant",
            "priority": "user"
        }

    def set_goal(self, goal):
        self.goal = goal

    def get_goal(self):
        return self.goal

    def update_context(self, key, value):
        self.context[key] = value

    def get_context(self):
        return self.context

    def set_identity(self, key, value):
        self.identity[key] = value

    def get_identity(self):
        return self.identity

    def reset(self):
        self.goal = None
        self.context = {}