"""Git operations require a separately authorized, scoped executor."""


class GitGear:
    def chronicle(self, message):
        """Refuse legacy automatic staging and commits.

        This compatibility entry point intentionally fails closed.
        """
        raise PermissionError(
            "Automatic Git chronicles are disabled. "
            "Require human approval, an explicit file allowlist, "
            "and an independently validated execution contract."
        )
