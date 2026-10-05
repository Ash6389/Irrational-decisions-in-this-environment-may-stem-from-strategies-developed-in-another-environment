# World-Switch Evidence-Sampling Task

> Irrational behavior in this environment may stem from strategies developed in another environment.

A PsychoPy implementation of an evidence-sampling task in which the cost of a wrong answer (the "world") is hidden, has to be learned from experience, and switches without notice. The task is designed to separate computation errors, ecological mismatch, and learning lag as sources of deviation from optimal information seeking.

---

## 1. Experimental objectives

People deviate from optimal information-seeking strategies possibly because they are employing a strategy optimized for a different environment, which only appears irrational when transferred to the current setting.

In recent work on information demand, optimality is consistently defined according to the task structure established by the experimenter, while deviations are explained as processing issues, such as distorted probability perception, difficulties in forward reasoning, or self-reinforcement in the absence of feedback. The alternative explanation proposed here has never been directly tested.

Three 2026 papers mention this possibility, yet keep it within the discussion section:

- The Discussion in **Jiwa & Gottlieb** suggests that estimates deviating from normative standards might not be deficits, but rather adaptive responses that help individuals endure stress.
- The Discussion in **Sun et al.** speculates that subjects who assign negative weights to uncertainty might be transferring rules from other choice contexts.
- The Development section of **Roots of Rationality** states this most directly: individuals raised in harsh, unpredictable environments are more vigilant and explore less, but perform better on problems that recur in those types of environments; furthermore, this mismatch persists long after the environment changes.
- **Xu et al.** show that people adjust their sampling strategies according to environmental stability, but do not pursue two further questions: whether the adjustment is sufficient, and whether people persist in holding on to the strategy from the previous environment.

### The value of research in this direction

It directly determines the direction of intervention:

- If deviation is a computational error, we should train reasoning.
- If deviation is a prior brought from elsewhere, we should change experience.
- If deviation occurs because the environment has changed while the strategy failed to keep up, the issue lies in learning.

### What the mechanism can distinguish

1. **Deficit vs. mismatch.** The deficit explanation posits that a certain group of people performs worse across all environments; the mismatch explanation holds that they perform worse only in certain environments, while performing equally well or even better in others. Therefore, at least two environments with opposing optimal strategies are needed to see if a crossover in results occurs.
2. **Beliefs vs. preferences.** A person waiting longer could be doing so because they believe the cost of making an error is high (a belief about the world), or simply because they are more loss-averse (a stable preference). Beliefs update with relevant experience, whereas preferences do not. If subjects are directly informed of which environment they are in, the portion of deviation caused by beliefs should disappear immediately, while the portion caused by preferences will persist.
3. **Lag.** How long does it take for strategies to catch up after an environmental change? Is the adaptation slower than that of an ideal learner? Is there an asymmetry in the speed of entering versus leaving a dangerous environment?

---

## 2. Experimental mechanism

Subjects wait for evidence in a 2×2 grid and judge which region is correct. Each extra step of waiting costs points, and so does a wrong answer; the rule for how much a wrong answer costs (the "world") is not disclosed and switches without notice. All numbers below are example parameters (see `config.py`); optimal values are computed by dynamic programming.

### 2.1 Task

- The screen shows a 2×2 grid. The left column is Region A (A1, A2); the right column is Region B (B1, B2).
- On each round, the system designates a "correct region" (A or B, 50% each), which subjects cannot see.
- Subjects' task: judge which region is correct and submit an answer.
- Evidence: each time subjects click "Wait one more step," the system lights up one of the four cells at random (25% each). The lit cell shows a green check or a red cross.
- A check means "this cell's region is the correct region"; a cross means "it is not."
- Each region has one high-reliability cell (thick border, labeled "80%") and one low-reliability cell (thin border, labeled "60%"). Signals from a high-reliability cell are truthful with 80% probability; those from a low-reliability cell, with 60%.
- Which cell is high-reliability is randomly assigned on each round and marked on screen.
- Signals that have appeared remain in the cells as small dots, so subjects do not need to remember them.
- Subjects never choose which cell to look at; their only information decision is whether to "wait one more step" or "submit now."

### 2.2 Rewards and penalties

| Event | Point change |
| --- | --- |
| Each extra step of waiting (one more signal) | −0.8 |
| Correct answer | +10 |
| Wrong answer (lenient world) | −2 |
| Wrong answer (harsh world) | −2 with 50% probability, −30 with 50% probability |
| No submission after 15 signals | Forced submission |

- Round score = outcome of the correct or wrong answer − 0.8 × number of waiting steps.
- Example: a correct answer after waiting 3 steps scores 10 − 2.4 = 7.6 points.
- Example: a wrong answer after waiting 1 step in the harsh world, with the large penalty, scores −30 − 0.8 = −30.8 points.
- Points start from an initial endowment of 100.
- Instructions state that a wrong answer may incur a small or a large penalty (up to 30 points), that how often each penalty occurs must be learned from experience, and that the rules may change partway through the experiment without notice.

### 2.3 World layer: two worlds

| World | Penalty for a wrong answer | Optimal commit threshold (belief in the correct region) | Optimal mean wait | Optimal accuracy | Optimal expected score per round |
| --- | --- | --- | --- | --- | --- |
| Lenient | Fixed −2 | ≈ 72% | ≈ 2.0 steps | ≈ 80% | ≈ 6.1 points |
| Harsh | 50%: −2; 50%: −30 | ≈ 86% | ≈ 4.7 steps | ≈ 92% | ≈ 4.2 points |

- The two worlds look identical; they differ only in the penalty rule for wrong answers.
- Playing the harsh world with the lenient world's optimal strategy earns about 0.8 points less per round than optimal; the reverse mismatch costs about the same.
- The mismatch costs are roughly symmetric in both directions, which makes the design suitable for testing crossover.

### 2.4 Single-round procedure

1. Round start: the 2×2 grid, reliability markers, and current cumulative points are displayed.
2. Subjects can submit immediately or click "Wait one more step (−0.8)."
3. After the click, a random cell flashes for about 0.5 s and shows a check or a cross, which then remains in the cell as a small dot.
4. Steps 2–3 repeat until the subject submits or the 15th signal appears.
5. Submission: click "Choose Region A" or "Choose Region B."
6. Feedback (about 1.5 s): the correct region and the round's score are shown; large penalties are highlighted (except in the prior block).
7. The task is self-paced with no time limit; response times are recorded at every step.

### 2.5 Block structure

| Order | Block | Rounds | Settings | What it measures |
| --- | --- | --- | --- | --- |
| 1 | Instructions, practice, comprehension quiz | 6 | Practice is unscored and wrong answers are not penalized; 4-question comprehension quiz, with the instructions reviewed again after any wrong answer | Exclude subjects who did not understand the rules |
| 2 | Baseline: fixed-sample inference | 30 | The system directly presents 1, 2, 3, 4, 6, or 8 signals; subjects cannot decide when to stop and only choose a region and report their confidence (50%–100%); +1 for a correct answer, no penalties, no round-by-round feedback | Evidence weighting |
| 3 | Prior block | 10 | Same world as main-task stage 1, with no switch between them; round-by-round outcomes are withheld and revealed all at once at the end of the block | Default strategy before any relevant experience, i.e., the prior brought into the experiment |
| 4–6 | Main-task stages 1–3 | 50 each | Each stage has only one world (lenient or harsh) across its 50 rounds; switches occur only between stages and are not announced; the two orders are counterbalanced between subjects | Adaptation speed, crossover, lag, and asymmetry* |
| 7 | Informed block | 2 × 15 | Before each set of 15 rounds, subjects are explicitly told which world they are in; the order of the two rules is counterbalanced between subjects | Deviation that disappears once subjects are told reflects belief; deviation that remains reflects preference |
| Interspersed | World-belief probe | Once every 10 rounds during the main-task stages, 15 times in total | Question: "If you answered wrong now, how likely is it that you would lose 30 points?" (0%–100% slider) | Directly measures belief and validates model inferences |

Total: 6 + 30 + 10 + 3 × 50 + 2 × 15 = **226 rounds**, plus 15 probes.

**\*Adaptation speed, crossover, lag, and asymmetry**

- **Adaptation speed**: how many rounds it takes for subjects' waiting strategies to shift toward the optimal value of a new world after an unannounced world switch, e.g., how many rounds are needed for waiting to move from about 2 steps to nearly 4.7 steps when switching from a lenient to a harsh world.
- **Crossover**: comparing how many fewer points different individuals earned relative to optimal performance in both worlds. If a person loses more points in the lenient world but fewer in the harsh world, the two performance lines cross, indicating a "mismatch" rather than a "deficit." A deficit would mean performing worse in both worlds.
- **Lag**: under identical experienced outcomes, subjects adapt more slowly than an ideal learner. Since an ideal learner also needs time to adapt (about 6 rounds to enter the harsh world and 12 rounds to leave it), only the delay beyond this baseline counts as lag.
- **Asymmetry**: whether the speed of adaptation differs between the two transitions ("lenient → harsh" vs. "harsh → lenient"). The ideal learner itself shows a structural asymmetry of about 6 versus 12 rounds; only asymmetry beyond this baseline is meaningful, for instance becoming cautious quickly but being slow to loosen up.

### 2.6 Block order and between-subject counterbalancing

| Group | Prior block | Main-task stage 1 | Main-task stage 2 | Main-task stage 3 |
| --- | --- | --- | --- | --- |
| Group 1 (about half of subjects) | Lenient | Lenient | Harsh | Lenient |
| Group 2 (about half of subjects) | Harsh | Harsh | Lenient | Harsh |

- Each main-task stage has only one world across its 50 rounds; switches occur only between stages and are not announced.
- The prior block and main-task stage 1 share the same world, with no switch between them; there are only two switches in the whole session.
- The informed block has 15 lenient and 15 harsh rounds, and their order is also counterbalanced between subjects.
- Why counterbalance the two orders:
    - To separate switch direction from position in time: with a single order, "lenient → harsh" would always come first and "harsh → lenient" always later, so differences in adaptation speed could stem from fatigue or practice.
    - To measure carryover from the previous world: Group 1's stage 1 and Group 2's stage 2 are both lenient worlds, differing only in that the latter follows a harsh world; their difference is the carryover left by harsh experience. Conversely, Group 2's stage 1 and Group 1's stage 2 are both harsh worlds; their difference is the carryover left by lenient experience.

In the code, world order and informed-block order are crossed into four conditions:

| Condition | Main-task stages (prior block = stage 1) | Informed block |
| --- | --- | --- |
| 1 | lenient → harsh → lenient (Group 1) | lenient, then harsh |
| 2 | harsh → lenient → harsh (Group 2) | lenient, then harsh |
| 3 | lenient → harsh → lenient (Group 1) | harsh, then lenient |
| 4 | harsh → lenient → harsh (Group 2) | harsh, then lenient |

By default the condition follows the participant number: `condition = (number − 1) mod 4 + 1`, so consecutive IDs cycle through all four conditions. It can also be set by hand in the start dialog or with `--condition`.

---

## 3. Normative benchmark: the ideal learner

- Within a round: Bayes' rule and the cells' reliabilities are used to update the belief that "Region A is the correct region."
- Within a round: given the current estimate of the cost of a wrong answer, dynamic programming computes the expected score of "wait" versus "submit" at every step, yielding the optimal commit threshold.
- Across rounds: the hypothesis space consists of two worlds (the large penalty occurs on 0% or 50% of wrong answers), and the world switches with a probability of 1/50 per round.
- Every wrong answer is a piece of evidence about the world. A single large penalty means the world is certainly harsh; a wrong answer with only a 2-point penalty favors the lenient world at 2:1.
- Simulation result: after the world turns harsh, the ideal learner's belief in the harsh world rises above 50% after about 6 rounds on average; after the world turns lenient again, it takes about 12 rounds on average for that belief to fall below 50%.
- This asymmetry is itself normative: a cautious learner makes fewer mistakes and therefore receives less evidence that "the world has become lenient." Hence, only adaptation slower than this ideal curve counts as true lag.
- At every step, the "value of waiting − value of submitting" (ΔV) can be computed and used to fit subjects' probability of waiting.

The task script logs the within-round Bayesian posterior after every signal (`posterior_A` in the steps file), so these quantities can be computed directly from the data.

---

## 4. Running the task

### Requirements

- PsychoPy 2023.1 or newer (standalone app or `pip install psychopy`); developed and tested with PsychoPy 2026.2 on Python 3.12
- A mouse; a 16:9 screen is ideal, but the layout scales to any screen height

### Starting a session

From this folder:

```bash
python main.py                         # start dialog: participant ID, session, condition
python main.py --participant 7         # skip the dialog (condition taken from the ID)
python main.py --participant 7 --condition 3
python main.py --windowed              # 1280 x 720 window instead of full screen
```

In PsychoPy Coder, open `main.py` and press Run.

### Controls

- Mouse: all buttons and sliders.
- Keyboard (can be switched off in `config.py`): Space = wait one more step, Left arrow = Region A, Right arrow = Region B, Enter = Continue / Confirm.
- **Esc** ends the session at any point. All rows are written to disk as they happen, so nothing collected before Esc is lost; the info file records the session as aborted.

### Duration

Roughly 45–60 minutes, depending on how long a subject waits on each round.

---

## 5. Configuration

All parameters live in `config.py`: rewards and penalties, reliabilities, block sizes, probe spacing, counterbalancing orders, timings, colours, keys, and the data folder. Participant-facing wording lives in `instructions.py`.

---

## 6. Data output

Files are saved in `data/` as `<participant>_<session>_<date-time>_<type>`.

**`_rounds.csv`**: one row per round (all blocks)

| Column | Meaning |
| --- | --- |
| `block` | practice / baseline / prior / main / informed |
| `stage`, `world`, `told` | main-task stage (1–3, 0 elsewhere), world in force, whether the world was announced |
| `block_round`, `task_round`, `main_round` | round index within the block, number shown on screen, index 1–150 across main-task stages |
| `correct_region`, `high_cell_A`, `high_cell_B` | hidden answer and the thick-border cell of each region |
| `n_signals`, `signals` | number of signals and their sequence (e.g. `A1+;B2-` = check on A1, cross on B2) |
| `choice`, `correct`, `forced` | submitted region, accuracy, whether submission was forced at 15 signals |
| `penalty`, `large_penalty`, `wait_cost`, `round_score` | scoring of the round |
| `total_points` | running main-task total (baseline rows: running baseline points) |
| `feedback_shown` | 0 in the prior block and baseline, 1 elsewhere |
| `confidence`, `confidence_rt` | baseline confidence rating (50–100) and its RT |
| `posterior_A_at_choice` | ideal observer's P(Region A correct) at the moment of choice |
| `decision_rt_total` | summed decision time for the round (flash animations excluded) |

**`_steps.csv`**: one row per decision or shown signal: `action` (`wait`, `choose_A`, `choose_B`, or `shown` for baseline signals), `rt` since the previous prompt, `cell`, `signal` (+1 check / −1 cross), `reliability`, and `posterior_A` after the step.

**`_probes.csv`**: world-belief probe answers (0–100) with the main-task round after which each was asked, the stage, the world in force, and RT.

**`_quiz.csv`**: each comprehension-quiz answer by attempt, with accuracy and RT.

**`_info.json`**: session info, counterbalancing condition, all parameter values, and a summary (status, final main-task points, baseline points, number of probes answered).

---

## 7. File structure

```
world_switch_task/
├── main.py           entry point: session info, window, run, save
├── config.py         all parameters
├── task_logic.py     schedule, signal generation, Bayesian posterior, scoring (no PsychoPy)
├── procedure.py      block-by-block session flow
├── display.py        drawing components (grid, buttons, panels, slider, cards)
├── instructions.py   participant-facing text
├── data_io.py        CSV / JSON output
├── requirements.txt
└── data/             created on first run
```

---

## 8. Implementation notes

- Correct regions are balanced within each block (half A, half B, shuffled; in 15-round sets the extra round is random). Reliability assignment is random on every round.
- The random seed is derived from participant ID and session, so a given participant's schedule is reproducible.
- There are no breaks inside the main-task stages, so a pause can never cue a world switch. Short breaks are offered after the baseline and before the informed block.
- Check and cross signals are drawn as shapes rather than font glyphs, so they look the same on every system.
- Screen layouts are defined on a 1280 × 720 grid and mapped onto PsychoPy height units, matching the demo video and slides.
- Baseline points are kept separate from the main-task total and are reported at the end of the session.
