import datetime


class HighScore:

    FILE = "scores.txt"

    @staticmethod
    def load():

        scores = []

        try:
            with open(HighScore.FILE, "r") as file:
                for line in file:
                    name, score, date = line.strip().split(",")
                    scores.append((name, int(score), date))
        except:
            pass

        return scores

    @staticmethod
    def save(name, score):

        scores = HighScore.load()

        today = datetime.datetime.now().strftime("%d/%m/%y")

        scores.append((name, score, today))

        # ordenar maior score primeiro
        scores.sort(key=lambda x: x[1], reverse=True)

        # manter apenas top 10
        scores = scores[:10]

        with open(HighScore.FILE, "w") as file:
            for s in scores:
                file.write(f"{s[0]},{s[1]},{s[2]}\n")