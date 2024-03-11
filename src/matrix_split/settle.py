import pulp


def settle_balances(balances):
    """
    Settle the balances

    Returns a list of transactions
    """
    prob = pulp.LpProblem("settle", pulp.LpMinimize)

    # Decision variables
    # x[i, j] is the amount of money that i owes to j
    x = pulp.LpVariable.dicts(
        "x", [(i, j) for i in balances for j in balances if i != j], lowBound=0
    )

    # Objective function
    # We want to minimize the amount of money that is transferred
    prob += pulp.lpSum([x[i, j] for i in balances for j in balances if i != j])

    # Constraints
    # We want to settle the balances
    # For each member, the sum of money going in and out should be equal to the balance
    for i in balances:
        prob += (
            pulp.lpSum([x[i, j] for j in balances if i != j])
            - pulp.lpSum([x[j, i] for j in balances if i != j])
            == balances[i]
        )

    # Solve the problem
    prob.solve()

    # Return the transactions
    return [
        (i, j, x[i, j].varValue)
        for i in balances
        for j in balances
        if i != j and x[i, j].varValue > 0
    ]
