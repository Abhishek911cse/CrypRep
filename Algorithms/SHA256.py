import hashlib

# initializing string
def get_sha256_hash(msg):
    result = hashlib.sha256(msg.encode())
    return result.hexdigest()


if __name__ == "__main__":
    # str = "random string"

    # encoding GeeksforGeeks using encode()
    # then sending to SHA256()

    # printing the equivalent hexadecimal value.
    # print("The hexadecimal equivalent of SHA256 is : ")
    # print(result.hexdigest())
    pass