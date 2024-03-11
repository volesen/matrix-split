import re

scanner = re.Scanner(
    [
        # Quoted strings
        (r"'[^']*'", lambda _, token: token.strip("'")),
        (r'"[^"]*"', lambda _, token: token.strip('"')),
        # Rest
        (r"\S+", lambda _, token: token),
        # Skip whitespace
        (r"\s+", None),
    ]
)


def tokenize(command: str) -> list[str]:
    tokens, _ = scanner.scan(command)
    return tokens


def parse_split_command(command: str, display_name_to_user_id: dict) -> dict:
    def diambiguate_mention(mention: str) -> str:
        """ """
        if ":" in mention:
            return mention

        return display_name_to_user_id[mention.removeprefix("@")]

    match tokenize(command):
        case [
            "!split",
            buyer,
            "bought",
            description,
            "for",
            amount,
            currency,
            "to",
            "everyone",
            "but",
            *recipients,
        ]:
            return {
                "buyer": diambiguate_mention(buyer),
                "description": description,
                "amount": float(amount),
                "currency": currency,
                "recipients": {
                    "exclude": [
                        diambiguate_mention(recipient) for recipient in recipients
                    ],
                },
            }
        case [
            "!split",
            buyer,
            "bought",
            description,
            "for",
            amount,
            currency,
            "to",
            "everyone",
        ]:
            return {
                "buyer": diambiguate_mention(buyer),
                "description": description,
                "amount": float(amount),
                "currency": currency,
                "recipients": {
                    "exclude": [],
                },
            }
        case [
            "!split",
            buyer,
            "bought",
            description,
            "for",
            amount,
            currency,
            "to",
            *recipients,
        ]:
            return {
                "buyer": diambiguate_mention(buyer),
                "description": description,
                "amount": float(amount),
                "currency": currency,
                "recipients": {
                    "include": [
                        diambiguate_mention(recipient) for recipient in recipients
                    ],
                },
            }
        case _:
            raise ValueError(f"Invalid command: {command}")
