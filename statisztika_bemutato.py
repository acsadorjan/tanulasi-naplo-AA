import statistics


def atlag_perc(percek):
    return statistics.mean(percek) if percek else 0.0


def median_perc(percek):
    return statistics.median(percek) if percek else 0.0


def szoras_perc(percek):
    return statistics.pstdev(percek) if percek else 0.0


def bemutato():
    minta = [30, 45, 60]
    print("Bemutatandó modul: statistics")
    print("Mintaadatok:", minta)
    print("statistics.mean:", atlag_perc(minta))
    print("statistics.median:", median_perc(minta))
    print("statistics.pstdev:", round(szoras_perc(minta), 2))


if __name__ == "__main__":
    bemutato()
