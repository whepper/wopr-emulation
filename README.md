# WOPR Emulation

```
╦ ╦╔═╗╔═╗╦═╗
║║║║ ║╠═╝╠╦╝
╚╩╝╚═╝╩  ╩╚═
War Operation Plan Response
```

A faithful Python implementation of the WOPR computer system from the iconic 1983 film **WarGames**. Relive the classic movie experience with authentic dialogue, the Joshua password backdoor, DEFCON escalation, and the famous conclusion that "the only winning move is not to play."

## 🎬 About the Movie

*WarGames* (1983) starring Matthew Broderick tells the story of a young hacker who accidentally accesses WOPR, a military supercomputer designed to simulate nuclear war scenarios. What begins as a game becomes a race against time to prevent actual World War III. The film's message about the futility of nuclear war remains powerful and relevant.

## ✨ Features

This emulation recreates the key moments from the film:

- **🔐 Joshua Password Authentication** - The backdoor password from the movie
- **🎮 Complete Game Menu** - All 15 games from WOPR's original list
- **♟️ Chess Game** - Play chess with WOPR, as Professor Falken intended
- **☢️ Global Thermonuclear War Simulation** - The infamous war game
- **🚨 DEFCON Level System** - Watch tensions escalate from DEFCON 5 to 1
- **🔢 Launch Code Acquisition** - Witness WOPR cracking 9 of 10 launch codes
- **💥 Strike & Retaliation** - Experience nuclear exchanges with casualty projections
- **🧠 Learning Sequence** - WOPR learns through tic-tac-toe that war is futile
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

## 🎮 How to Play

### The Authentic WarGames Experience

Follow these steps to recreate the movie's iconic scenes:

#### 1. **System Logon**
```
LOGON: [Enter any name]
PASSWORD: joshua
```

💡 **Movie Fact**: "Joshua" was the name of Professor Falken's deceased son. This backdoor password becomes the key to accessing WOPR in the film.

#### 2. **Game Selection**

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

#### 3. **The Chess Question**

WOPR will ask:
```
WOULDN'T YOU PREFER A GOOD GAME OF CHESS?
```

Respond with **NO** to continue with the war simulation, or **YES**/**CHESS** to play chess instead.

💡 **Movie Fact**: This line represents WOPR's final attempt to avoid nuclear war after learning its futility.

#### 4. **Launch Code Acquisition**

Watch as WOPR attempts to crack the launch codes:
```
LAUNCH CODE 1/10 ACQUIRED: CPE-1704-TKS
LAUNCH CODE 2/10 ACQUIRED: DPR-5938-AKL
...
WARNING: 9 OF 10 LAUNCH CODES ACQUIRED
```

💡 **Movie Fact**: In the film, WOPR cycles through millions of combinations trying to find the launch codes, creating tension as it gets closer to 10/10.

#### 5. **DEFCON Escalation**

Monitor the Defense Condition levels as tensions rise:
- **DEFCON 5**: Normal peacetime readiness
- **DEFCON 4**: Increased intelligence watch
- **DEFCON 3**: Increase in force readiness (launch codes acquired)
- **DEFCON 2**: Further increase in force readiness (first strikes)
- **DEFCON 1**: Maximum readiness (nuclear war imminent)

💡 **Movie Fact**: The DEFCON system is real and used by the U.S. military. The film accurately portrays its escalation during a nuclear crisis.

#### 6. **Target Selection**

Select Soviet cities as primary targets:
```
PRIMARY TARGETS SELECTION:
  - MOSCOW
  - LENINGRAD
  - KIEV
  - MINSK
  - TASHKENT

SELECT TARGET: [Type city name]
```

Witness the strike, casualty estimates, and Soviet retaliation.

#### 7. **The Learning Sequence**

After multiple exchanges, WOPR initiates its learning sequence:
- Analyzes all nuclear war scenarios
- Runs tic-tac-toe simulations to understand futility
- Reaches its famous conclusion

```
A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.

HOW ABOUT A NICE GAME OF CHESS?
```

💡 **Movie Fact**: This is one of the most famous movie quotes about nuclear war, teaching that some conflicts cannot be won and should not be fought.

## 🎯 Alternative Paths

### Play Chess Instead

Select option **7** (CHESS) from the game menu:
```
EXCELLENT. A GAME OF CHESS. WHITE OR BLACK?
```

Choose your color and play against WOPR using algebraic notation:
```
YOUR MOVE: e2 e4
MY MOVE: e7 e5
```

### Explore Other Games

Many games in WOPR's database are "not currently available" - just like in the movie. Try selecting different options to see WOPR's responses!

## 🎭 Movie Quotes Included

- "GREETINGS PROFESSOR FALKEN."
- "SHALL WE PLAY A GAME?"
- "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?"
- "A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY."
- "HOW ABOUT A NICE GAME OF CHESS?"

## 🛠️ Technical Details

### Architecture

- **WOPR Class**: Main system controller handling authentication, game selection, and coordination
- **ChessGame Class**: Implements basic chess rules and AI opponent
- **NuclearWarSimulation Class**: Manages war game scenarios, DEFCON levels, and learning sequence

### Game Mechanics

**Chess**:
- Standard 8x8 board with full piece set
- Simplified move validation
- Random AI opponent
- Algebraic notation (e.g., "e2 e4")

**Global Thermonuclear War**:
- Target selection from Soviet cities
- Automatic Soviet retaliation
- Casualty projections
- DEFCON escalation system
- Learning sequence triggering

## 🎓 Educational Value

This emulation serves as:

- **Historical Reference**: Experience computing and Cold War culture from 1983
- **Programming Example**: Study game logic, state management, and user interaction
- **Peace Education**: Understand the anti-nuclear war message through interactive experience
- **Retro Computing**: Appreciate the command-line interface aesthetic

## 📚 Behind the Scenes

### Movie Production Notes

- The film's technical advisor was a real computer security expert
- WOPR's voice was created by sound engineers to sound ominous yet neutral
- The NORAD scenes were filmed in a real military command center
- "Joshua" was chosen as the password for its emotional connection to Falken

### Implementation Details

This Python implementation aims for **experience accuracy** over technical accuracy:

- **Simplified Chess**: Full chess rules would require thousands of lines; we use simplified validation
- **Accelerated Timeline**: Real nuclear simulations took hours; ours takes minutes
- **Random AI**: WOPR's actual AI would be more sophisticated
- **Terminal-based**: The original used custom graphics terminals

## 🐛 Known Limitations

- Chess AI uses random legal moves (not strategic)
- Move validation is simplified
- No network multiplayer (WOPR was standalone)
- No graphics beyond ASCII art

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] More sophisticated chess AI
- [ ] Additional game implementations (Falken's Maze, etc.)
- [ ] Sound effects and audio quotes
- [ ] Enhanced ASCII graphics/animations
- [ ] Save/load game states
- [ ] More detailed nuclear simulation
- [ ] Terminal color support

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
