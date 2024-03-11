import matrix_split.parsing


def test_parsing_to_reciepients():
    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to A2"
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "include": ["@A2"],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to A2 jebi"
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "include": ["@A2", "@jebi"],
        },
    }


def test_parsing_everyone():
    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to everyone"
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }


def test_parsing_everyone_but():
    assert matrix_split.parsing.parse_split_command(
        "!split @volesen bought 'Beer 🍻' for 100 DKK to everyone but @A2"
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": ["@A2"],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to everyone but A2 jebi"
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": ["@A2", "@jebi"],
        },
    }


def test_parsing_description_quotes():
    assert matrix_split.parsing.parse_split_command(
        "!split @volesen bought 'Beer 🍻' for 100 DKK to everyone"
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        '!split @volesen bought "Beer 🍻" for 100 DKK to everyone'
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }


def test_parsing_mention():
    assert matrix_split.parsing.parse_split_command(
        '!split volesen bought "Beer 🍻" for 100 DKK to everyone'
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        '!split @volesen bought "Beer 🍻" for 100 DKK to everyone'
    ) == {
        "buyer": "@volesen",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        '!split @volesen:matrix.org bought "Beer 🍻" for 100 DKK to everyone'
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }
