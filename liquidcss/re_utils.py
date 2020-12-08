class Replacement(object):

    def __init__(self, replacement, manager):
        self.replacement = replacement
        self.manager = manager
        self.occurrences = []

    def __call__(self, match):
        matched = match.group(0)
        replaced = match.expand(
            self.replacement
        ).format(
            self.manager._generate_id(
                matched
            )
        )
        self.occurrences.append((matched, replaced))
        return replaced