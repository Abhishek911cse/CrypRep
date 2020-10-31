def remove_backspace(S):
    q = []
    for i in range(0, len(S)):
        if S[i] != '¶':
            q.append(S[i])
        elif len(q) != 0:
            q.pop()
    # Build final string
    ans = ""
    while len(q) != 0:
        ans += q[0]
        q.pop(0)
    # return final string
    return ans


def get_final_file(fileName):
    log = open(fileName, 'r', encoding="utf-8")
    lines = log.readlines()
    with open("final.txt", 'w') as f:
        for line in lines:
            f.write(remove_backspace(line))
