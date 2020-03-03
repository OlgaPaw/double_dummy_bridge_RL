# Double Dummy Bridge Reinforcement Learning Solver

This repo contains a PoC of using Reinforcement Learning to solve Double Dummy Bridge Problem.

## Dependencies

- python 3.7+
- poetry

## Run Learning

```
mkdir -p results

# If want to learn on clean network. Leave untached if you want tu update network.
mv src/q_models_data/deep_q_learn.h5 src/q_models_data/deep_q_learn.h5.old

poetry shell
PYTHONPATH=. python src/train.py
```

## Run validation

```
mkdir -p results/validate
PYTHONPATH=. python src/validate.py
```

## Chart drawing

This is developer purpose script, so if sth does not meet your expectations - feel free to modify in code. Currently it takes a list of validation directories as an input and draws 3 charts:

- progress on learning invalid moves (from directory 1)
- comparison of invalid rules from all directories
- comparison of tricks won from all directories

Use example:

```
python chart_draw.py results_dry_run/validate results_rules/validate/ results_both_q_and_rules/validate
```
