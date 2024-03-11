import pytest
import matrix_split.transactions


@pytest.fixture
def members():
    return [
        "@alice:matrix.org",
        "@bob:matrix.org",
        "@charlie:matrix.org",
        "@david:matrix.org",
    ]


def test_split_everyone(members):
    purchase = {
        "buyer": "@alice:matrix.org",
        "description": "pizza",
        "amount": 20.0,
        "currency": "EUR",
        "recipients": {
            "exclude": [],
        },
    }

    transactions = list(matrix_split.transactions.split_purchase(purchase, members))

    assert sorted(
        transactions,
        key=lambda t: t["to"],
    ) == [
        {
            "from": "@alice:matrix.org",
            "to": "@alice:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
        {
            "from": "@alice:matrix.org",
            "to": "@bob:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
        {
            "from": "@alice:matrix.org",
            "to": "@charlie:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
        {
            "from": "@alice:matrix.org",
            "to": "@david:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
    ]


def test_split_everyone_but(members):
    purchase = {
        "buyer": "@alice:matrix.org",
        "description": "pizza",
        "amount": 15.0,
        "currency": "EUR",
        "recipients": {
            "exclude": ["@bob:matrix.org", "@charlie:matrix.org"],
        },
    }

    transactions = list(matrix_split.transactions.split_purchase(purchase, members))

    assert sorted(
        transactions,
        key=lambda t: t["to"],
    ) == [
        {
            "from": "@alice:matrix.org",
            "to": "@alice:matrix.org",
            "amount": 7.5,
            "currency": "EUR",
        },
        {
            "from": "@alice:matrix.org",
            "to": "@david:matrix.org",
            "amount": 7.5,
            "currency": "EUR",
        },
    ]



def test_balances():
    transactions = [
        {
            "from": "@alice:matrix.org",
            "to": "@bob:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
        {
            "from": "@alice:matrix.org",
            "to": "@charlie:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
        {
            "from": "@alice:matrix.org",
            "to": "@david:matrix.org",
            "amount": 5.0,
            "currency": "EUR",
        },
    ]

    balances = matrix_split.transactions.calculate_balances(transactions)

    assert balances == {
        "@alice:matrix.org": 15.0,
        "@bob:matrix.org": -5.0,
        "@charlie:matrix.org": -5.0,
        "@david:matrix.org": -5.0,
    }