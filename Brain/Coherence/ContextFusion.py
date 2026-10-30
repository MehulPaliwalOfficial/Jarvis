class ContextFusion:
    """
    Combines multiple context sources into one
    """

    def fuse(self, *contexts):
        fused = {}

        for ctx in contexts:
            if isinstance(ctx, dict):
                fused.update(ctx)

        return fused

    def priority_fuse(self, high_priority: dict, low_priority: dict):
        """
        High priority overrides low priority
        """
        result = dict(low_priority)
        result.update(high_priority)
        return result