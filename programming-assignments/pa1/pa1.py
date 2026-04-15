#!/usr/bin/env python3
"""Student starter for PA1."""

from __future__ import annotations

from typing import Any, Dict, List
import re
import sys


def solve_horn(formula: Dict[str, Any]) -> Dict[str, Any]:
    """Implement Horn resolution with unit propagation."""
    # LAYOUT
    # make a copy of formula
    is_contradiction = False
    formula_copy = formula.copy()
    print(formula_copy)
    # loop through all rules
    while (not is_contradiction) and (not len(formula_copy['rules']) is 0):
        # check if facts derive result of any rule fully
        for i in range(0, len(formula_copy['rules'])): # loop through all rules
            rule = formula_copy['rules'][i]
            num_confirmed_vars = 0



            # check to see if all variables in a rule exists in facts
            for var in rule.body:
                if var in facts:
                    num_confirmed_vars += 1
                else:
                    break

            if num_confirmed_vars == len(rules.body): # if the rule is solved from facts, add that rule to facts
                # contradiction check
                if rule.head is None:
                    is_contradiction = true
                    return { 'satisfiable' : False }

                formula_copy.facts.append(rule.head)
                formula_copy.rules.remove(rule)
                i -= 1

    return { 'satisfiable' : True , 'true_vars' : formula_copy.facts }


def parse_horn_clause_string(text: str) -> Dict[str, Any]:
    """
    Parse text like: [[-a,-b,c], [-c,-d,e], [a]]
    Each clause must be Horn (at most one positive literal).
    """
    src = ''.join(text.strip().split())
    clause_texts = re.findall(r'\[([^\[\]]*)\]', src)

    clauses: List[List[str]] = []
    for raw in clause_texts:
        if raw == '':
            clauses.append([])
            continue
        tokens = [tok for tok in raw.split(',') if tok]
        clauses.append(tokens)

    variables = set()
    facts: List[str] = []
    rules: List[Dict[str, Any]] = []

    for clause in clauses:
        neg_body: List[str] = []
        positives: List[str] = []

        for lit in clause:
            if lit.startswith('-'):
                v = lit[1:]
                if v:
                    neg_body.append(v)
                    variables.add(v)
            else:
                positives.append(lit)
                if lit:
                    variables.add(lit)

        if len(positives) > 1:
            head = positives[0]
        elif len(positives) == 1:
            head = positives[0]
        else:
            head = None

        if not neg_body and head is not None:
            facts.append(head)
        else:
            rules.append({'body': neg_body, 'head': head})

    return {
        'variables': sorted(variables),
        'facts': sorted(set(facts)),
        'rules': rules,
    }


def format_result(result: Dict[str, Any]) -> str:
    sat = 'true' if result['satisfiable'] else 'false'
    if result['satisfiable']:
        tv = ' '.join(sorted(set(result['true_vars'])))
        return f'satisfiable: {sat}\ntrue_vars: {tv}'.rstrip()
    return f'satisfiable: {sat}'


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    formula = parse_horn_clause_string(raw)
    result = solve_horn(formula)
    print(format_result(result))


if __name__ == '__main__':
    main()
