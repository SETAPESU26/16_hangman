import random
from words import WORDS, HINTS


class HangmanGame:
    DIFFICULTIES = {
        "easy": {
            "lives": 8,
            "multiplier": 1,
            "hint_penalty": 1
        },
        "medium": {
            "lives": 6,
            "multiplier": 2,
            "hint_penalty": 2
        },
        "hard": {
            "lives": 4,
            "multiplier": 3,
            "hint_penalty": 3
        }
    }

    def __init__(self):
        self.score = 0
        self.streak = 0
        self.category = "technology"
        self.difficulty = "medium"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 6
        self.hint_used = False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()

        settings = self.DIFFICULTIES[self.difficulty]
        self.lives = settings["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(
            ch if ch in self.guessed else "_"
            for ch in self.secret
        )

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        if len(letter) != 1 or not letter.isalpha():
            return "Invalid input. Enter one letter."

        if letter in self.guessed:
            return "You already guessed that letter."

        if letter in self.wrong:
            return "You already guessed that letter."

        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."

        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."
  

    def use_hint(self):
        if self.hint_used:
            return None

        self.hint_used = True

        penalty = self.DIFFICULTIES[self.difficulty]["hint_penalty"]
        self.score = max(0, self.score - penalty)

        return HINTS.get(
            self.secret,
            "No hint available."
        )

    def calculate_round_score(self):
        settings = self.DIFFICULTIES[self.difficulty]
        base_score = 5 + self.streak
        return base_score * settings["multiplier"]

    def play_round(self):
        self.start_round()

        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print(
                "Difficulty:", self.difficulty,
                "Lives:", self.lives,
                "Score:", self.score,
                "Streak:", self.streak
            )

            raw = input(
                "Letter, /hint, or /quit: "
            ).strip().lower()

            if raw == "/quit":
                return False

            if raw == "/hint":
                hint = self.use_hint()
                print(
                    hint if hint
                    else "Hint already used."
                )
                continue

            print(self.guess(raw))

        if self.won():
            self.streak += 1

            round_score = self.calculate_round_score()
            self.score += round_score

            print("Solved:", self.secret)
            print("Round score:", round_score)

            return True

        self.streak = 0
        print(
            "Out of lives. The word was:",
            self.secret
        )

        return True

    def choose_difficulty(self):
        while True:
            print("\nDifficulty:")
            print("1. Easy   - 8 lives, 1x score")
            print("2. Medium - 6 lives, 2x score")
            print("3. Hard   - 4 lives, 3x score")

            raw = input(
                "Choose difficulty (1/2/3): "
            ).strip().lower()

            choices = {
                "1": "easy",
                "2": "medium",
                "3": "hard",
                "easy": "easy",
                "medium": "medium",
                "hard": "hard"
            }

            if raw in choices:
                self.difficulty = choices[raw]
                return

            print("Invalid difficulty.")

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")

        while True:
            self.choose_difficulty()

            print(
                "\nCategories:",
                ", ".join(WORDS)
            )

            raw = input(
                "Choose category or q: "
            ).strip().lower()

            if raw == "q":
                return

            if raw not in WORDS:
                print("Unknown category.")
                continue

            self.category = raw

            if not self.play_round():
                return

            again = input(
                "Another round? [y/n]: "
            ).strip().lower()

            if again != "y":
                print(
                    "Final score:",
                    self.score,
                    " Streak:",
                    self.streak
                )
                return
if __name__ == "__main__":
    HangmanGame().run()
