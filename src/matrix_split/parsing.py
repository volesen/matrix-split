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


def tokenize(command: str):
    tokens, _ = scanner.scan(command)
    return tokens


def diambiguate_user(user: str):
    # TODO: Should normalize the display name or user_id to the user_id
    return "@" + user if not user.startswith("@") else user


def parse_split_command(command: str):
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
                "buyer": diambiguate_user(buyer),
                "description": description,
                "amount": int(amount),
                "currency": currency,
                "recipients": {
                    "exclude": [
                        diambiguate_user(recipient) for recipient in recipients
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
                "buyer": diambiguate_user(buyer),
                "description": description,
                "amount": int(amount),
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
                "buyer": diambiguate_user(buyer),
                "description": description,
                "amount": int(amount),
                "currency": currency,
                "recipients": {
                    "include": [
                        diambiguate_user(recipient) for recipient in recipients
                    ],
                },
            }
        case _:
            raise ValueError(f"Invalid command: {command}")
