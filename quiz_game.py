"""
Terminal Quiz Game
------------------
An expanded, more robust version of a simple multiple-choice quiz.
Features: real countdown timer (thread-based), difficulty levels,
scoring with streak bonus, letter grading, persistent high score,
and a post-game review of missed questions.
"""

import random
import time
import os
import json
import threading

HIGHSCORE_FILE = "highscore.json"
TIME_LIMIT = 15  # seconds allowed per question

QUESTIONS = [
    {"q": "Capital of Pakistan?", "o": ["Karachi", "Lahore", "Islamabad", "Peshawar"], "a": 2, "level": "Easy"},
    {"q": "2 + 5 = ?", "o": ["6", "7", "8", "9"], "a": 1, "level": "Easy"},
    {"q": "Which planet is known as the Red Planet?", "o": ["Venus", "Mars", "Jupiter", "Saturn"], "a": 1, "level": "Easy"},
    {"q": "How many continents are there?", "o": ["5", "6", "7", "8"], "a": 2, "level": "Easy"},
    {"q": "Water freezes at what temperature (Celsius)?", "o": ["0", "10", "-1", "100"], "a": 0, "level": "Easy"},
    {"q": "Python keyword used to define a function?", "o": ["func", "def", "fun", "define"], "a": 1, "level": "Medium"},
    {"q": "Which data type is immutable in Python?", "o": ["list", "dict", "tuple", "set"], "a": 2, "level": "Medium"},
    {"q": "What does 'open()' primarily do in Python?", "o": ["Loop", "Open a file", "Print output", "Import a module"], "a": 1, "level": "Medium"},
    {"q": "Which HTTP method is typically used to fetch data?", "o": ["POST", "GET", "DELETE", "PUT"], "a": 1, "level": "Medium"},
    {"q": "What symbol starts a comment in Python?", "o": ["//", "#", "--", "/*"], "a": 1, "level": "Medium"},
    {"q": "Big-O of binary search on a sorted array?", "o": ["O(n)", "O(n^2)", "O(log n)", "O(1)"], "a": 2, "level": "Hard"},
    {"q": "Which sorting algorithm has worst-case O(n log n)?", "o": ["Bubble sort", "Merge sort", "Insertion sort", "Selection sort"], "a": 1, "level": "Hard"},
    {"q": "What does CPU stand for?", "o": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Core Processing Utility"], "a": 1, "level": "Hard"},
    {"q": "In Python, what does GIL stand for?", "o": ["Global Interpreter Lock", "General Import Library", "Global Index List", "Generic Interface Layer"], "a": 0, "level": "Hard"},
    {"q": "Which of these is NOT a Python built-in type?", "o": ["int", "float", "char", "bool"], "a": 2, "level": "Hard"},
]


def load_high_score():
    """Read the saved high score, creating the file if missing."""
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": 0, "name": "-"}, f)
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)


def save_high_score(name, score):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump({"high_score": score, "name": name}, f)


def timed_input(prompt, timeout):
    """
    Get input from the user but stop waiting after `timeout` seconds.
    Uses a background thread so we can enforce a real deadline,
    unlike a plain input() call which blocks indefinitely.
    """
    answer = [None]

    def get_input():
        answer[0] = input(prompt)

    thread = threading.Thread(target=get_input, daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("\n⏰ Time's up!")
        return None
    return answer[0]


def ask_question(question, number, total):
    print(f"\nQ{number}/{total} [{question['level']}]: {question['q']}")
    for i, option in enumerate(question["o"]):
        print(f"  {chr(65 + i)}) {option}")

    start = time.time()
    raw_answer = timed_input("Answer (A/B/C/D): ", TIME_LIMIT)
    elapsed = time.time() - start

    correct_letter = "ABCD"[question["a"]]
    if raw_answer is None:
        return False, elapsed

    user_answer = raw_answer.strip().upper()
    is_correct = user_answer == correct_letter

    if is_correct:
        print("✅ Correct!")
    else:
        print(f"❌ Wrong. Correct answer: {correct_letter}) {question['o'][question['a']]}")

    return is_correct, elapsed


def letter_grade(percent):
    if percent >= 90:
        return "A+"
    if percent >= 80:
        return "A"
    if percent >= 70:
        return "B"
    if percent >= 60:
        return "C"
    if percent >= 50:
        return "D"
    return "F"


def play_round():
    name = input("Enter your name: ").strip() or "Player"
    level = input("Choose level (Easy/Medium/Hard): ").strip().title()

    pool = [q for q in QUESTIONS if q["level"] == level]
    if not pool:
        print("No questions found for that level. Defaulting to Easy.")
        pool = [q for q in QUESTIONS if q["level"] == "Easy"]

    random.shuffle(pool)
    selected = pool[:10] if len(pool) >= 10 else pool

    score = 0
    streak = 0
    missed = []
    total_time = 0.0

    for i, question in enumerate(selected, start=1):
        correct, elapsed = ask_question(question, i, len(selected))
        total_time += elapsed

        if correct:
            streak += 1
            bonus = min(streak - 1, 5)  # up to +5 bonus for consecutive correct answers
            points = 10 + bonus
            score += points
            if bonus:
                print(f"🔥 Streak x{streak}! +{points} points")
        else:
            streak = 0
            missed.append(question)

    max_possible = len(selected) * 10
    percent = (score / max_possible) * 100 if max_possible else 0
    grade = letter_grade(percent)
    avg_time = total_time / len(selected) if selected else 0

    print("\n" + "=" * 30)
    print(f"Player:      {name}")
    print(f"Score:       {score} / {max_possible}")
    print(f"Percentage:  {percent:.1f}%")
    print(f"Grade:       {grade}")
    print(f"Avg. time:   {avg_time:.1f}s per question")
    print("=" * 30)

    data = load_high_score()
    if score > data["high_score"]:
        save_high_score(name, score)
        print("🏆 New high score!")
    else:
        print(f"High score is still {data['high_score']} by {data['name']}")

    if missed:
        show = input("\nReview missed questions? (y/n): ").strip().lower()
        if show == "y":
            print("\n--- Review ---")
            for q in missed:
                correct_letter = "ABCD"[q["a"]]
                print(f"- {q['q']}  (Correct: {correct_letter}) {q['o'][q['a']]})")


def main():
    while True:
        print("\n1. Play")
        print("2. High Score")
        print("3. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            play_round()
        elif choice == "2":
            data = load_high_score()
            print(f"High Score: {data['high_score']} (by {data['name']})")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
