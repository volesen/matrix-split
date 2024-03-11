from collections import defaultdict


def split_purchase(purchase, members):
    """
    Split the purchase into a list of transactions
    """

    buyer = purchase["buyer"]
    amount = purchase["amount"]
    currency = purchase["currency"]

    # Elaborate `exclude` into a list of recipients
    if "exclude" in purchase["recipients"]:
        recipients = set(members) - set(purchase["recipients"]["exclude"])
    else:
        recipients = purchase["recipients"]["include"]

    amount_per_recipient = amount / len(recipients)

    for recipient in recipients:
        # TODO: `from` and `to` are probably not the best names for the concepts
        yield {
            "from": buyer,
            "to": recipient,
            "amount": amount_per_recipient,
            "currency": currency,
        }


def calculate_balances(transactions):
    """
    Calculate the balances for each user
    """
    balances = defaultdict(int)

    for transaction in transactions:
        balances[transaction["from"]] += transaction["amount"]
        balances[transaction["to"]] -= transaction["amount"]

    return balances

