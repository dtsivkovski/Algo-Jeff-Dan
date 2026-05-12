"""PA3 SAT solver starter.

Copy your PA2 implementation into this file. The Sudoku solver should call
sat_solve(clauses, assignment).
"""

from __future__ import annotations

def literal_variable(literal):
    """Return the variable number appearing in a literal."""
    return abs(literal)


def literal_required_value(literal):
    """Return the value that makes a literal true."""
    return literal > 0


def evaluate_literal(literal, assignment):
    """Evaluate one literal under a partial assignment.

    Return:
      True if the literal is already true,
      False if the literal is already false,
      None if its variable is not assigned yet.
    """
    variable = literal_variable(literal)
    if variable not in assignment:
        return None
    return assignment[variable] == literal_required_value(literal)


def simplify(clauses, assignment):
    """Simplify clauses under a partial assignment.

    Clauses that are already true disappear. Literals that are already false are
    removed from their clauses. If a clause becomes empty, the current partial
    assignment cannot lead to a solution.
    """
    simplified = []
    for clause in clauses:
        new_clause = []
        clause_satisfied = False

        for literal in clause:
            value = evaluate_literal(literal, assignment)
            if value is True:
                clause_satisfied = True
                break
            if value is None:
                new_clause.append(literal)

        if clause_satisfied:
            continue
        if len(new_clause) == 0:
            return None
        simplified.append(new_clause)

    return simplified


def unit_propagate(clauses, assignment):
    """Repeatedly apply unit clauses.

    This is one of the key algorithmic parts of the assignment.
    """

    # check for simplified clause
    simplified = simplify(clauses, assignment)
    if simplified is None:
        return None

    # check for unit clauses
    for clause in simplified:
        # check for unit clause
        if len(clause) == 1:
            literal = clause[0]
            variable = literal_variable(literal)
            value = literal_required_value(literal)
            # add variable assignment and propagate again
            assignment[variable] = value
            return unit_propagate(simplified, assignment)

    return simplified

def choose_variable(clauses, assignment):
    """Choose an unassigned variable to branch on.

    This simple helper returns the first unassigned variable it sees. You may
    replace it by a smarter heuristic.
    """
    for clause in clauses:
        for literal in clause:
            variable = literal_variable(literal)
            if variable not in assignment:
                return variable
    return None


def sat_solve(clauses, assignment):
    """Solve SAT for a CNF formula by extending the given partial assignment.

    Return a satisfying assignment if one exists. Return None otherwise.
    """

    # propagate clauses and check contradiction or solution
    propagated = unit_propagate(clauses, assignment)
    if propagated is None:
        return None
    if len(propagated) == 0:
        return assignment

    # choose a variable to try values on
    variable = choose_variable(propagated, assignment)
    if variable is None:
        return None

    # try true val
    assignment[variable] = True
    result = sat_solve(propagated, assignment.copy())
    if result is not None:
        return result

    # try false val
    assignment[variable] = False
    result = sat_solve(propagated, assignment.copy())
    if result is not None:
        return result

    # no solution found
    return None
