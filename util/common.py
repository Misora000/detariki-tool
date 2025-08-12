import os


def dfs(path: str) -> list[str]:
    ls = []
    for v in os.listdir(path):
        child = os.path.join(path, v)
        if os.path.isdir(child):
            ls += dfs(child)
        else:
            ls.append(child)
    return ls


def sort_and_remove_duplicate(input: list) -> list:
    output = []
    input.sort()
    for i, v in enumerate(input):
        if i > 0 and input[i] == input[i-1]:
            continue
        if type(v) == str and len(v) == 0:
            continue
        output.append(v)
    return output

