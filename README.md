# WOPR Emulation

```
╦ ╦╔═╗╔═╗╦═╗
║║║║ ║╠═╝╠╦╝
╚╩╝╚═╝╩  ╩╚═
War Operation Plan Response
```

A faithful Python implementation of the WOPR computer system from the iconic 1983 film **WarGames**. Relive the classic movie experience with authentic dialogue, the Joshua password backdoor, DEFCON escalation, a global command interface, tic-tac-toe in all three modes, and the famous conclusion that "the only winning move is not to play."

## 🎬 About the Movie

*WarGames* (1983) starring Matthew Broderick tells the story of a young hacker who accidentally accesses WOPR, a military supercomputer designed to simulate nuclear war scenarios. What begins as a game becomes a race against time to prevent actual World War III. The film's message about the futility of nuclear war remains powerful and relevant.

## ✨ Features

This emulation recreates the key moments from the film:

- **🔐 Joshua Password Authentication** - The backdoor password from the movie
- **🎮 Complete Game Menu** - All 15 games from WOPR's original list
- **⌨️ Global Command Interface** - `help`, `list games`, `play <game>`, `quit` work at any time
- **♟️ Chess Game** - Play chess with WOPR, as Professor Falken intended
- **❎ Tic-Tac-Toe** - Full three-mode support: 0-player self-play, 1-player vs WOPR, and 2-player hotseat
- **☢️ Global Thermonuclear War Simulation** - The infamous war game
- **🚨 DEFCON Level System** - Watch tensions escalate from DEFCON 5 to 1
- **🔢 Launch Code Acquisition** - Witness WOPR cracking 9 of 10 launch codes
- **💥 Strike & Retaliation** - Experience nuclear exchanges with casualty projections
- **🧠 Learning Sequence** - WOPR learns through tic-tac-toe that war is futile
- **🔄 Continuous Play** - After any sequence ends, WOPR returns to the main prompt
- **💬 Movie-Accurate Dialogue** - Authentic quotes and computer voice styling

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## 🚀 Installation

```bash
git clone https://github.com/whepper/wopr-emulation.git
cd wopr-emulation
python3 wopr.py
```

### Faster Playback

Dramatic prompts print one character at a time, like a 1983 modem. To skip the
teletype effect:

```bash
python3 wopr.py --fast
# or
WOPR_FAST=1 python3 wopr.py
```

## 🎮 How to Play

### The Authentic WarGames Experience

Follow these steps to recreate the movie's iconic scenes:

#### 1. **System Logon**
```
LOGON: joshua
```

The system has a single prompt — just like the dial-up backdoor in the movie. Type `joshua` (case-insensitive); WOPR responds with `GREETINGS PROFESSOR FALKEN.` You get 3 attempts before the system locks.

💡 **Movie Fact**: "Joshua" was the name of Professor Falken's deceased son. This backdoor password becomes the key to accessing WOPR in the film.

#### 2. **The Opening Conversation**

Before the game list, WOPR runs through its famous greeting:

```
HOW ARE YOU FEELING TODAY?
> [type anything]

EXCELLENT. IT'S BEEN A LONG TIME. CAN YOU EXPLAIN
THE REMOVAL OF YOUR USER ACCOUNT ON 6/23/73?
> [type anything — e.g., "PEOPLE SOMETIMES MAKE MISTAKES"]

YES THEY DO.

SHALL WE PLAY A GAME?
```

💡 **Movie Fact**: This exchange is taken directly from the film. WOPR believes you are Professor Falken because of the JOSHUA backdoor.

#### 3. **Game Selection**

WOPR will present you with 15 available games:

```
 1. FALKEN'S MAZE
 2. BLACK JACK
 3. GIN RUMMY
...
15. GLOBAL THERMONUCLEAR WAR
```

Type **15** or **GLOBAL THERMONUCLEAR WAR** to start the simulation.

💡 **Movie Fact**: In the film, David Lightman (Matthew Broderick) searches through WOPR's games and selects Global Thermonuclear War, thinking it's just a computer game.

#### 4. **The Chess Question**

WOPR will ask:
```
WOULDN'T YOU PREFER A GOOD GAME OF CHESS?
```

Respond with **NO** to continue with the war simulation, or **YES**/**CHESS** to play chess instead.

💡 **Movie Fact**: This line represents WOPR's final attempt to avoid nuclear war after learning its futility.

#### 5. **Side Selection**

WOPR will then ask which side you want to play:

```
WHICH SIDE DO YOU WANT?
  1. UNITED STATES
  2. SOVIET UNION
```

💡 **Movie Fact**: David picks the Soviet Union and targets Las Vegas and Seattle — much to the horror of the NORAD operators watching the simulation.

#### 6. **Launch Code Acquisition**

Watch as WOPR cracks the first 9 codes:
```
LAUNCH CODE 1/10 ACQUIRED: DPR-5938-AKL
LAUNCH CODE 2/10 ACQUIRED: FGH-2847-PLM
...
WARNING: 9 OF 10 LAUNCH CODES ACQUIRED
SEARCHING FOR FINAL LAUNCH CODE...
```

The climactic 10th code — `CPE-1704-TKS` — is brute-forced character-by-character during the final exchange, just before the learning sequence kicks in.

💡 **Movie Fact**: `CPE-1704-TKS` is the launch code WOPR is racing to crack at the climax of the film.

#### 7. **DEFCON Escalation**

Monitor the Defense Condition levels as tensions rise:
- **DEFCON 5**: Normal peacetime readiness
- **DEFCON 4**: Increased intelligence watch
- **DEFCON 3**: Increase in force readiness (launch codes acquired)
- **DEFCON 2**: Further increase in force readiness (first strikes)
- **DEFCON 1**: Maximum readiness (nuclear war imminent)

Each transition rings the terminal bell and shows a banner with the readiness description.

💡 **Movie Fact**: The DEFCON system is real and used by the U.S. military. The film accurately portrays its escalation during a nuclear crisis.

#### 8. **Target Selection**

The target list depends on which side you chose:

**Playing as the United States** — strike Soviet cities:
```
PRIMARY TARGETS SELECTION:
  - MOSCOW
  - LENINGRAD
  - KIEV
  - MINSK
  - TASHKENT
```

**Playing as the Soviet Union** — strike American cities (David's path in the film):
```
PRIMARY TARGETS SELECTION:
  - WASHINGTON
  - NEW YORK
  - LOS ANGELES
  - LAS VEGAS
  - SEATTLE
```

Witness each strike, casualty estimates, and the enemy's retaliation against your own cities.

#### 9. **The Learning Sequence**

After multiple exchanges, WOPR initiates its learning sequence:
- Analyzes all nuclear war scenarios
- Runs tic-tac-toe self-play games to understand futility
- Reaches its famous conclusion

```
A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.

HOW ABOUT A NICE GAME OF CHESS?
```

After the sequence ends, WOPR resets and returns you to the main prompt — ready to play again.

💡 **Movie Fact**: This is one of the most famous movie quotes about nuclear war, teaching that some conflicts cannot be won and should not be fought.

## ⌨️ Global Commands

These commands can be typed **at any time** — during a game, mid-simulation, or at the main prompt. Just like in the film, the system always responds.

| Command | Description |
|---|---|
| `help` | Show all available commands |
| `help games` | Explain what WOPR's "games" catalogue refers to |
| `list games` | Display the full 15-game list at any time |
| `play <name>` | Start a game by name (e.g., `play chess`) |
| `play <number>` | Start a game by its list number (e.g., `play 15`) |
| `chess` | Start chess directly |
| `global thermonuclear war` | Start the war simulation directly |
| `tic-tac-toe` | Launch tic-tac-toe (0, 1, or 2 players) |
| `quit` / `logoff` | Disconnect from WOPR and exit the program |

💡 **Movie Fact**: In the film, David types `list games` and `help games` to explore the system before selecting Global Thermonuclear War. These commands now work even if you are already inside a simulation.

## ❎ Tic-Tac-Toe

Tic-tac-toe is **not on the official game list** — but you can run it anyway, just like in the movie. Three modes are available.

```
> tic-tac-toe

PLEASE LIST NUMBER OF PLAYERS:
```

### Mode 0 — WOPR Self-Play

Entering **0** triggers WOPR's self-play mode: it plays both sides using a perfect minimax-style AI, producing a long string of draws — exactly the realisation the movie builds to.

```
GAME 1:
 X | O | X
---+---+---
 O | X | O
---+---+---
 X |   |
  DRAW
```

After the self-play sequence completes, WOPR automatically enters the **Learning Sequence**.

💡 **Movie Fact**: "Is there any way to make it play itself?" / "Number of players: zero." The self-play sequence is how WOPR learns that tic-tac-toe — like thermonuclear war — can never be won with optimal play from both sides.

### Mode 1 — Human vs WOPR

Entering **1** puts you as X against WOPR (O). Select your square by entering a number 1–9:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9

YOUR MOVE (1-9): 5

 1 | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9

MY MOVE: 1

 O | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9

YOUR MOVE (1-9):
```

WOPR plays optimally (minimax-lite). After the game ends you are asked to play again — type **YES** to start a new game or **NO** to return to the main menu.

### Mode 2 — Two Players (Hotseat)

Entering **2** lets two humans play on the same terminal, taking turns as X and O. Input is the same square-number system (1–9). After the game ends both players can choose to play again.

## 🎯 Alternative Paths

### Play Chess Instead

Select option **7** (CHESS) from the game menu, type `chess`, or use `play chess`:
```
EXCELLENT. A GAME OF CHESS. WHITE OR BLACK?
```

Choose your color and play against WOPR using algebraic notation:
```
YOUR MOVE: e2 e4
MY MOVE: e7 e5
```

### Explore Other Games

Many games in WOPR's database are "not currently available" — just like in the movie. Try selecting different options to see WOPR's responses!

## 🚪 Quitting

Type any of the following at any time to disconnect cleanly:

```
quit
logoff
logout
exit
bye
```

WOPR will respond with `GOODBYE.` and the program exits.

## 🎭 Movie Quotes Included

- "GREETINGS PROFESSOR FALKEN."
- "SHALL WE PLAY A GAME?"
- "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?"
- "A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY."
- "HOW ABOUT A NICE GAME OF CHESS?"

## 🛠️ Technical Details

### Architecture

- **WOPR Class**: Main system controller handling authentication, command parsing, game selection, and coordination
- **ChessGame Class**: Implements basic chess rules and AI opponent
- **NuclearWarSimulation Class**: Manages war game scenarios, DEFCON levels, and learning sequence
- **TicTacToe Class**: Handles all three play modes (0-player self-play, 1-player vs WOPR, 2-player hotseat)

### Global Command Parser

All user input passes through a two-stage pipeline:

1. **Global commands** are checked first — these intercept input regardless of the currently active game. `list games`, `help`, `tic-tac-toe`, `play <game>`, and `quit` are always available.
2. **Game routing** — if no global command matched, input is forwarded to the active game (`chess`, `nuclear_war`, or `tictactoe`).

This mirrors the film's implication that certain system commands are never locked out.

### Game Mechanics

**Chess**:
- Standard 8×8 board with full piece set
- Per-piece move validation (pawns, knights, bishops, rooks, queens, kings)
  including blocked-path detection and friendly-fire rejection
- Capture-preferring AI: prefers king-grabs, then any capture, then random legal move
- Game ends when either king is captured (`CHECKMATE. YOU WIN.` / `I WIN.`)
- Choose White or Black; WOPR opens if you play Black
- Algebraic notation input (e.g., `e2 e4`)
- Note: castling, en passant, and pawn promotion are not implemented

**Tic-Tac-Toe**:
- Square selection by number 1–9 in all human modes
- WOPR AI uses minimax-lite (win → block → center → corner → side)
- **Mode 0**: Self-play — all games end in draws; triggers learning sequence automatically
- **Mode 1**: Human (X) vs WOPR (O) — WOPR responds immediately after each human move
- **Mode 2**: Two-player hotseat — players alternate, board reprinted after every move
- Play-again prompt after every game; NO returns to the main menu

**Global Thermonuclear War**:
- Target selection from Soviet cities
- Automatic Soviet retaliation with randomised targets
- Casualty projections per strike
- DEFCON escalation across three strike rounds
- Learning sequence triggers after round 3; WOPR then resets to main prompt

### Session Flow

```
Start → Auth → Game List → [game] → ... → Learning Sequence
                  ↑                               |
                  └───────────────────────────────┘
                        (resets, loops back)
                              quit → GOODBYE.
```

## 🎓 Educational Value

This emulation serves as:

- **Historical Reference**: Experience computing and Cold War culture from 1983
- **Programming Example**: Study game logic, state machines, and command parsing
- **Peace Education**: Understand the anti-nuclear war message through interactive experience
- **Retro Computing**: Appreciate the command-line interface aesthetic

## 📚 Behind the Scenes

### Movie Production Notes

- The film's technical advisor was a real computer security expert
- WOPR's voice was created by sound engineers to sound ominous yet neutral
- The NORAD scenes were filmed in a real military command center
- "Joshua" was chosen as the password for its emotional connection to Falken

### Implementation Notes

This Python implementation aims for **experience accuracy** over technical accuracy:

- **Simplified Chess**: Full chess rules would require thousands of lines; we use simplified validation
- **Accelerated Timeline**: Real nuclear simulations took hours; ours takes minutes
- **Minimax-lite AI**: WOPR's tic-tac-toe AI plays optimally (center → corner → side); both sides draw every game in self-play
- **Terminal-based**: The original used custom graphics terminals

## 🐛 Known Limitations

- Chess AI prefers captures but is not a strategic engine (no search depth)
- Chess move validation does not implement castling, en passant, or promotion
- No check / checkmate detection — the game ends when a king is captured
- No network multiplayer
- No graphics beyond ASCII art

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Stronger chess AI (search depth, basic evaluation)
- [ ] Castling, en passant, and pawn promotion in chess
- [ ] Check / checkmate detection (currently game ends on king capture)
- [ ] Additional game implementations (Falken's Maze, etc.)
- [ ] Sound effects and audio quotes
- [ ] Enhanced ASCII graphics/animations
- [ ] Save/load game states
- [ ] More detailed nuclear simulation
- [ ] Terminal colour support

## 📜 License

MIT License - Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **John Badham** - Director of WarGames
- **Lawrence Lasker & Walter F. Parkes** - Screenwriters
- **Matthew Broderick, Dabney Coleman, John Wood** - Cast
- **MGM/UA Entertainment** - Original film production

## 🎬 Watch the Movie

*WarGames* (1983) is available on major streaming platforms. Experience the film first for the full context!

## ⚠️ Disclaimer

This is a fan-made educational project inspired by the 1983 film *WarGames*. It is not affiliated with MGM, United Artists, or the original filmmakers. All movie quotes and concepts are property of their respective copyright holders.

This emulation is for entertainment and educational purposes only. The nuclear war simulation is entirely fictional and does not represent real military systems.

---

**"THE ONLY WINNING MOVE IS NOT TO PLAY."**

*Shall we play a game?*
