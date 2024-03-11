import matrix_split.settle


def test_no_transactions_needed():
    balances = {
        "@alice:matrix.org": 0.00,
        "@bob:matrix.org": 0.00,
        "@charlie:matrix.org": 0.00,
        "@dave:matrix.org": 0.00,
    }

    transactions = matrix_split.settle.settle_balances(balances)

    assert transactions == []


def test_no_redundant_transactions():
    balances = {
        "@alice:matrix.org": 300.00,
        "@bob:matrix.org": -100.00,
        "@charlie:matrix.org": -100.00,
        "@dave:matrix.org": -100.00,
    }

    transactions = matrix_split.settle.settle_balances(balances)

    assert sorted(transactions, key=lambda t: t[1]) == [
        ("@alice:matrix.org", "@bob:matrix.org", 100.00),
        ("@alice:matrix.org", "@charlie:matrix.org", 100.00),
        ("@alice:matrix.org", "@dave:matrix.org", 100.00),
    ]
