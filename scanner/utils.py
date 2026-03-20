from config import SEVERITY_RULES

def get_severity(line):
    for level, keywords in SEVERITY_RULES.items():
        for keyword in keywords:
            if keyword in line.lower():
                return level
    return "safe"


def load_ignore():
    try:
        with open("ignore.txt") as f:
            return [line.strip().lower() for line in f.readlines()]
    except:
        return []