
# Quiz Game

A terminal-based multiple-choice quiz game in Python with timed questions, streak bonuses, difficulty levels, and a persistent high score.

## Features

- 🎯 **Three difficulty levels** — Easy, Medium, Hard
- ⏱️ **Timed questions** — 15 seconds per question, enforced with a background thread
- 🔥 **Streak bonus scoring** — consecutive correct answers earn extra points
- 🏆 **Persistent high score** — saved between sessions in `highscore.json`
- 📊 **Letter grading** — A+ to F based on final percentage
- 📝 **Missed question review** — see the correct answers after each round
- ✅ No external dependencies — built entirely with Python's standard library

## Requirements

- Python 3.7 or higher

## How to Run

```bash
python quiz_game.py
```

You'll see a menu:

```
1. Play
2. High Score
3. Exit
```

- **Play** — enter your name, pick a difficulty level, and answer 10 questions
- **High Score** — view the current top score and who set it
- **Exit** — quit the program

## Sample Output

```
1. Play
2. High Score
3. Exit
Choice: 1
Enter your name: Jaffar
Choose level (Easy/Medium/Hard): Medium

Q1/10 [Medium]: Python keyword used to define a function?
  A) func
  B) def
  C) fun
  D) define
Answer (A/B/C/D): B
✅ Correct!

...

==============================
Player:      Jaffar
Score:       85 / 100
Percentage:  85.0%
Grade:       A
Avg. time:   4.2s per question
==============================
🏆 New high score!
```

## Project Structure

```
.
├── quiz_game.py     # Main game logic
├── highscore.json   # Auto-created on first run to store the high score
├── README.md
├── LICENSE
└── .gitignore
```

## How It Works (Quick Overview)

- Questions are stored as a list of dictionaries, each with text, options, the correct answer index, and a difficulty level.
- On each round, questions are filtered by difficulty and shuffled with `random.shuffle`.
- Each question is timed using a background thread (`threading`) so unanswered questions time out correctly instead of waiting forever.
- Scores are calculated with a streak bonus for consecutive correct answers.
- High scores are stored in JSON so both the score and the player's name persist across runs.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
