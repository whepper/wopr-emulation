# Changelog

All notable changes to this project are documented here. The format is
loosely based on [Keep a Changelog](https://keepachangelog.com/), and the
project does not yet use [Semantic Versioning](https://semver.org/).

## [2.0.0] — 2026-06-20

### Added

- **Falken's Maze** — fully playable 5x5 grid where player (`P`) and WOPR
  (`W`) race to the center (`*`). Player starts at the bottom-left,
  WOPR at the top-right, and uses Manhattan-distance heuristic.
  Movement via `N` / `S` / `E` / `W`. Selectable as game #1, or via
  `play 1` / `falken's maze` at any time.
- **NORAD interjections** during the war simulation. Seven lines of
  flavor from the "NORAD" war room, e.g. `"[NORAD] GENERAL, WE HAVE
  MULTIPLE LAUNCH DETECTIONS."`, interspersed between strikes.
- **"I'M FINE. HOW ARE YOU?"** — the famous non-sequitur reply to
  whatever the user types after "HOW ARE YOU FEELING TODAY?". Taken
  directly from the film's script.
- **"5…4…3…2…1…"** cinematic countdown in the learning sequence,
  one tick per second, immediately before the punchline.
- **"IS THIS A GAME OR IS IT REAL?"** — the film's most chilling line,
  printed in slow teletype after the war scenarios.
- **"*** CHANGES LOCKED OUT ***"** lockout screen polish, replacing the
  bare "ACCESS DENIED. SYSTEM LOCKED." message.
- **"UNABLE TO COMPUTE. PLEASE LIST ANOTHER."** for invalid game
  selections, replacing the original "INVALID SELECTION. PLEASE CHOOSE
  AGAIN."
- **`who is falken`** global command. Reveals Professor Falken's
  biography and the revelation that he is dead. One-shot — the reveal
  is shown only once and subsequent queries are declined.
- **Boot timestamp** at startup, e.g.
  `WOPR (War Operation Plan Response)  ::  2026-06-20  21:38:14`.
- **"THIS TIME WE PLAY FOR REAL."** pressure line, printed if the user
  hesitates more than 3 seconds on the "WOULDN'T YOU PREFER A GOOD GAME
  OF CHESS?" prompt.
- **Chess flavor line** "A GAME OF CHESS IS A BATTLE OF LOGIC AND
  PATIENCE. NEITHER SIDE CAN AFFORD A MISCALCULATION." printed before
  the WHITE OR BLACK prompt.
- **Teletype effect on iconic quotes** — `"GREETINGS PROFESSOR FALKEN."`,
  `"SHALL WE PLAY A GAME?"`, `"EXCELLENT. A GAME OF CHESS. WHITE OR
  BLACK?"`, and the `"A STRANGE GAME..."` punchline are now printed
  one character at a time using the slow teletype delay.
- **Test suite** — 133 unit tests in `tests/`, no external dependencies,
  using only `unittest` from the standard library. Includes regression
  tests for the previously-broken `"YESTERDAY"`-treated-as-yes bug and
  the DEFCON banner alignment.

### Changed

- **Package layout** — refactored from a single 1100-line `wopr.py` into
  a 12-module `wopr/` package. See README for the new module map.
- **All duration constants** extracted into `wopr/timing.py::Timing`.
  Replaces the scattered `time.sleep(0.5)` / `time.sleep(2)` literals
  throughout the code.
- **`TicTacToe.play_turn` decomposed** — the original 122-line method
  is now a ~15-line dispatch over 7 focused step handlers
  (`_ask_player_count`, `_receive_player_count`, `_apply_human_move`,
  `_wopr_responds`, etc.).
- **`WOPR._process_input` uses a dispatch table** of `(predicate,
  handler)` pairs, replacing the 86-line if/elif chain.
- **`CurrentGame` enum** — `current_game` is now a `str` enum
  (`NONE` / `TICTACTOE` / `CHESS` / `NUCLEAR` / `FALKEN_MAZE`) instead
  of a bare string.
- **Game registry** — `select_game`'s three linear passes through
  `AVAILABLE_GAMES` replaced by a single `registry.resolve_selection`
  helper.
- **Tic-tac-toe `play_turn` accepts an optional `writer` callable**,
  so tests can capture output without monkey-patching `print`.

### Fixed

- **DEFCON banner alignment** — content rows previously overflowed the
  border by up to 5 characters. All rows are now exactly 54 chars wide
  via a single `BANNER_WIDTH` constant in `wopr/defcon.py`.
- **`"YESTERDAY"`-treated-as-yes bug** — the war confirmation used
  `startswith("YES")`, so any word starting with "yes" (e.g. "YESTERDAY")
  launched a chess game. Now uses tokenized matching via
  `shlex.split`.
- **Case-sensitivity in war confirmation** — the `_WAR_AFFIRM` /
  `_WAR_DECLINE` sets contained uppercase tokens but were intersected
  against lowercased user input, so `"no"` was never matched. Sets are
  now lowercase.
- **Bare `except Exception`** in chess move parser replaced with
  `(ValueError, IndexError)`.
- **DEFCON reset ownership** — `NuclearWarSimulation.play_turn` was
  mutating `self.wopr.defcon_level = 5` directly. Now goes through
  `WOPR.reset_post_war()`.
- **Empty `pass` guards** in `TicTacToe.play_turn` step-4 removed.
- **Stale step-4 comment block** in `TicTacToe.play_turn` removed.
- **`movie_quotes_terminal()` wrapper** function was redundant; inlined
  the lookup at the call site.
- **9 unused `WOPR` attributes** removed (`conversation_history`,
  `learning_data`, `system_id`, `operating_system`, `processor`,
  `security_level`, `system_time` property, `system_status` branch, and
  others).
- **3 unused chess/nuclear attributes** removed (`move_count`,
  `move_history`, `target_history`).

### Removed

- `wopr_legacy.py` (the original 1100-line single file) — replaced by
  the `wopr/` package.
- Dead comment blocks (`# Step 4: ...` and similar) in `TicTacToe.play_turn`.
- `WOPR.system_time` property — was defined but never read.

## [1.0.0] — 2023-XX-XX

Initial public release. Single-file `wopr.py` (~1100 lines) implementing
the WOPR conversation, the 15-game list, chess, tic-tac-toe (3 modes),
the global thermonuclear war simulation, DEFCON escalation, launch
code acquisition, and the learning sequence culminating in
"THE ONLY WINNING MOVE IS NOT TO PLAY."
