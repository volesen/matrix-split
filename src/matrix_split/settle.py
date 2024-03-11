import pulp


def settle_balances(balances):
    """
    Settle the balances

    Returns a list of transactions
    """
    prob = pulp.LpProblem("settle", pulp.LpMinimize)

    # Decision variables: t[i, j] is the amount of money that member i pays to member j
    t = pulp.LpVariable.dicts(
        "transaction",
        [(i, j) for i in balances for j in balances if i != j],
        lowBound=0,
        cat="Continuous",
    )

    # Objective function: minimize the amount of money that is transferred
    prob += pulp.lpSum([t[i, j] for i in balances for j in balances if i != j])

    # Constraints: each member's total outgoing and incoming amounts equal their balance
    for i in balances:
        prob += (
            pulp.lpSum([t[i, j] for j in balances if i != j])
            - pulp.lpSum([t[j, i] for j in balances if i != j])
            == balances[i]
        )

    prob.solve()

    # Extract and return transactions where money is transferred
    return [
        (i, j, t[i, j].varValue)
        for i in balances
        for j in balances
        if i != j and t[i, j].varValue > 0
    ]
