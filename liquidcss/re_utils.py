from re import Match


class Replacement(object):

    def __init__(self, replacement: str, manager):
        self.replacement = replacement
        self.manager = manager
        self.occurrences = []

    def __call__(self, match: Match):
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