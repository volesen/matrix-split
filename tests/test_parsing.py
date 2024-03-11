import pytest
import matrix_split.parsing


@pytest.fixture
def display_name_to_user_id():
    return {
        "volesen": "@volesen:matrix.org",
        "A2": "@asbjorn:olli.ng",
        "jebi": "@jebi:matrix.org",
    }


def test_parsing_to_reciepients(display_name_to_user_id: dict):
    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to A2",
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "include": ["@asbjorn:olli.ng"],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to A2 jebi",
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "include": ["@asbjorn:olli.ng", "@jebi:matrix.org"],
        },
    }


def test_parsing_everyone(display_name_to_user_id: dict):
    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to everyone",
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }


def test_parsing_everyone_but(display_name_to_user_id):
    assert matrix_split.parsing.parse_split_command(
        "!split @volesen bought 'Beer 🍻' for 100 DKK to everyone but @A2",
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": ["@asbjorn:olli.ng"],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to everyone but A2 jebi",
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": ["@asbjorn:olli.ng", "@jebi:matrix.org"],
        },
    }


def test_parsing_description_quotes(display_name_to_user_id: dict):
    assert matrix_split.parsing.parse_split_command(
        "!split volesen bought 'Beer 🍻' for 100 DKK to everyone",
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        '!split @volesen bought "Beer 🍻" for 100 DKK to everyone',
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }


def test_parsing_mention(display_name_to_user_id):
    assert matrix_split.parsing.parse_split_command(
        '!split volesen bought "Beer 🍻" for 100 DKK to everyone',
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        '!split @volesen bought "Beer 🍻" for 100 DKK to everyone',
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }

    assert matrix_split.parsing.parse_split_command(
        '!split @volesen:matrix.org bought "Beer 🍻" for 100 DKK to everyone',
        display_name_to_user_id
    ) == {
        "buyer": "@volesen:matrix.org",
        "description": "Beer 🍻",
        "amount": 100.00,
        "currency": "DKK",
        "recipients": {
            "exclude": [],
        },
    }
