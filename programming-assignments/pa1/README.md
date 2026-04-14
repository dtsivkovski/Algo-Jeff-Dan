# Programming Assignment 1: Horn formulas and unit propagation

This assignment asks you to determine whether a propositional Horn formula is satisfiable.
Horn formulas are a special SAT case that can be solved efficiently with forward chaining
(also called unit propagation in this context).

## Background

A clause is **Horn** if it has at most one positive literal. In this assignment, literals are:

- `-x` for a negative literal ("not `x`")
- `x` for a positive literal

Because each clause has at most one positive literal, each clause can be interpreted as an implication:

- `[-a,-b,c]` means `(a AND b) -> c`
- `[a]` means `true -> a` (a fact)
- `[-x,-y]` means `(x AND y) -> false` (a contradiction rule)

A **Horn formula** is a conjunction of Horn clauses.

The key idea:

- start with known facts,
- repeatedly apply rules whose body is already true,
- if you derive `false`, the formula is unsatisfiable,
- if propagation reaches a fixed point with no contradiction, it is satisfiable.

## Input format

Your script is called with one argument containing the full formula, for example:

```bash
python3 pa1.py "[[-a,-b,c],[-c,-d,e],[a]]"
```

That string is parsed as a list of clauses, where each inner list is one clause.

## Output format

Your program should print:

```text
satisfiable: true|false
true_vars: <space-separated variables>  # only when satisfiable: true
```

Important for grading:

- only `satisfiable:` is used for scoring,
- `true_vars:` is ignored by the checker and should only be printed for satisfiable cases.

## What you implement

In [`pa1.py`](pa1.py), implement:

```python
def solve_horn(formula: dict) -> dict:
    ...
```

Expected return structure:

- `{"satisfiable": bool, "true_vars": list[str]}`

## Suggested algorithm (forward chaining)

1. Initialize a set/queue with facts.
2. For each rule, track how many body literals are still unmet.
3. When a variable becomes true, update all rules depending on it.
4. When a rule body is fully satisfied:
   - derive its head variable, or
   - if head is `None`, report unsatisfiable.
5. If no contradiction is derived, report satisfiable.

### Example run (forward chaining)

Consider this formula (as one argument string). It includes a **longer Horn body** in `[-a,-b,c]`, meaning `(a AND b) -> c`:

```text
[[a],[b],[-a,-b,c],[-c,d],[-d]]
```

Read each clause as a rule:

| Clause      | Meaning                         |
|-------------|---------------------------------|
| `[a]`       | fact: `a` is true               |
| `[b]`       | fact: `b` is true               |
| `[-a,-b,c]` | if `a` **and** `b` then `c`     |
| `[-c,d]`    | if `c` then `d`                 |
| `[-d]`      | if `d` then `false`             |

Trace:

1. **Start** — From `[a]` and `[b]`, mark `a` and `b` as true. Known true: `{a, b}`.
2. **Fire** `(a AND b) -> c` — The rule `[-a,-b,c]` has body `{a, b}`; both are already true, so derive `c`. Known true: `{a, b, c}`.
3. **Fire** `c -> d` — Body `{c}` is satisfied, so derive `d`. Known true: `{a, b, c, d}`.
4. **Fire** `d -> false` — Body `{d}` is satisfied, so you derived a contradiction.

So the formula is **unsatisfiable**. Your program would print `satisfiable: false` (and no `true_vars` line).

For contrast, if the last clause were omitted, `[[a],[b],[-a,-b,c],[-c,d]]` would stop at step 3 with no contradiction rule firing. Then the formula is **satisfiable** and you would print `satisfiable: true` plus a `true_vars:` line listing the variables you derived as true (here `a b c d`).

## Grading (15 points total)

Grading breakdown:

- **9 points**: tests pass
- **1 points**: output contract and CLI usage
  - correctly prints `satisfiable: true|false`
  - prints `true_vars` only when satisfiable
- **1 point**: maintaining directory and file structure. In particular, your file `pa1.py` must be in a subdirectory `pa1`.
- **1 point**: code quality (readable implementation, clear variable naming, no hard-coding)

You are encouraged to add your own test cases. I maintain the right to use additional test cases for grading.

Scoring is based on satisfiability correctness; `true_vars` is not used for correctness grading.

## Collaboration and Repository Requirements

- Work in groups of **2-4** students.
- Create a **new private repository** for your group.
- Add your full PA1 work in that private repository.
- Invite [me](https://github.com/jonweinb) to the private repository so I can grade it.
- Do **not** modify the directory, file, and template structure from Programming Assignment 1.

## Testing

Run public tests:

```bash
python3 tests/check.py --solution pa1.py
```

If you run `check.py` from inside `tests/`, use a path relative to that directory (for example `--solution ../../reference_pa1.py` for the instructor reference next to `student/`). Relative `--solution` paths are resolved from your **current working directory** first.

Run full grader:

```bash
python3 ../tests/grade_pa1.py --solution "$PWD/pa1.py"
```
