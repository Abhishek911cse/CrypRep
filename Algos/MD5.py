import math


class MD5:
    # Per round shift amounts:
    __rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,  # Rounds 1 to 16
                        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,  # Rounds 17 to 32
                        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,  # Rounds 33 to 48
                        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]  # Rounds 49 to 64

    # Use binary integer part of the sines of integers (Radians) as constants
    # this is performed by performing logical AND operation with largest 32 bit integer - 0xFFFFFFFF
    __constants = [int(abs(math.sin(i + 1)) * 2 ** 32)
                   & 0xFFFFFFFF for i in range(64)]
    # Define initial values in little-endian format (bytes go in reverse order)
    # So if words are written like this in typical (big-endian) format, the would look like this:
    # word A: 01 23 45 67
    # word B: 89 ab cd ef
    # word C: fe dc ba 98
    # word D: 76 54 32 10
    # In our case they will look like this:
    __init_values = [0x67452301, 0xEFCDAB89,
                     0x98BADCFE, 0x10325476]  # A  # B  # C  # D
    # Non linear functions used in MD5 rounds in description they are referred in this order:
    # F(b,c,d) = (b AND c) OR (NOT b and d)
    # G(b,c,d) = (b AND d) OR (c AND NOT d)
    # H(b,c,d) = b XOR c XOR d
    # I(b,c,d) = c XOR (b OR NOT d)
    # Each of the functions are performed 16 times,
    # so there are 16 instances of each of them in the function list
    __functions = (
        16 * [lambda b, c, d: (b & c) | (~b & d)]
        + 16 * [lambda b, c, d: (d & b) | (~d & c)]
        + 16 * [lambda b, c, d: b ^ c ^ d]
        + 16 * [lambda b, c, d: c ^ (b | ~d)]
    )
    # Function determines index of which 32bit word should be used
    # Rounds 01-16: g(i) = i
    # Rounds 17-32: g(i) = (5 * i + 1)mod16
    # Rounds 33-48: g(i) = (3 * i + 5)mod16
    # Rounds 49-64: g(i) = (7 * i)mod16
    # Each of the functions are performed 16 times,
    # so there are 16 instances of each of them in the function list
    __index_functions = (
        16 * [lambda i: i]
        + 16 * [lambda i: (5 * i + 1) % 16]
        + 16 * [lambda i: (3 * i + 5) % 16]
        + 16 * [lambda i: (7 * i) % 16]
    )

    @staticmethod
    def __left_rotate(x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def get_md5_hash(self, text):
        # Convert message to ascii encoded bytes:
        message = bytearray(text.encode("ascii"))
        # Calculate and append message length in bytes:
        message_length = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
        # Add padding
        message.append(0x80)
        while len(message) % 64 != 56:
            message.append(0)
        message += message_length.to_bytes(8, byteorder="little")
        # Dictionary for all values:
        values = {
            "length": message_length,
            "length_after_padding": len(message),
            "s_table": [
                "s[{0:2d}] = {1}".format(i, self.__rotate_amounts[i])
                for i in range(len(self.__rotate_amounts))
            ],
            "t_table": [
                "T[{0:2d}] = {1}".format(i, self.__constants[i])
                for i in range(len(self.__constants))
            ],
            "message_blocks_int": [
                [
                    int.from_bytes(
                        message[foo + i: foo + i + 4], byteorder="little")
                    for i in range(0, len(message[foo: foo + 64]), 4)
                ]
                for foo in range(0, len(message), 64)
            ],
            "message_blocks_hex": [
                [
                    "{:08x}".format(
                        int.from_bytes(
                            message[foo + i: foo + i + 4], byteorder="little"
                        )
                    )
                    for i in range(0, len(message[foo: foo + 64]), 4)
                ]
                for foo in range(0, len(message), 64)
            ],
            "operations": [],
            "hash": None,
        }

        hash_pieces = self.__init_values[:]
        # Perform MD5 operations for message chunks of 64 bits
        # This is done by iterating through the list with step of 64
        for chunk_offset in range(0, len(message), 64):
            # Assign initial values:
            a, b, c, d = hash_pieces
            # Select 64bit chunk of a message
            chunk = message[chunk_offset: chunk_offset + 64]
            # Append new block array to operations entry:
            values["operations"].append([])
            # Perform 64 MD5 operations (4 different operations 16 times each)
            for i in range(64):
                # Apply correct non-linear function:
                f = self.__functions[i](b, c, d)
                # Apply correct index function:
                g = self.__index_functions[i](i)
                # Variable used to calculate value before rotation, which consists of variable a, correct f function value,
                # correct constant (marked as K in the diagram) and 32bit word which is found by selecting 4 bytes
                # from a chunk:
                to_rotate = (
                    a
                    + f
                    + self.__constants[i]
                    + int.from_bytes(chunk[4 * g: 4 * g + 4],
                                     byteorder="little")
                )
                # Calculate new b value by adding current b value and left rotated previous value by correct amount of
                # rotations from array
                new_b = (
                    b + self.__left_rotate(to_rotate, self.__rotate_amounts[i])
                ) & 0xFFFFFFFF
                # Assigning new values in such order:
                # a -> d,
                # b -> new_b(A according to diagram)
                # c -> b
                # d -> c
                a, b, c, d = d, new_b, b, c
                values["operations"][-1].append(
                    ["{:08x}".format(i) for i in [a, b, c, d]]
                )
            hash_pieces = [
                (hash_pieces[foo] + val) & 0xFFFFFFFF
                for foo, val in enumerate([a, b, c, d])
            ]
            values["operations"][-1].append(["{:08x}".format(i)
                                             for i in hash_pieces])
        raw = sum(x << (32 * i) for i, x in enumerate(hash_pieces)).to_bytes(
            16, byteorder="little"
        )
        values["hash"] = "{:032x}".format(int.from_bytes(raw, byteorder="big"))
        return values


if __name__ == "__main__":
    demo = [  # '',
        # 'a',
        # 'abc',
        # 'message digest',
        # 'abcdefghijklmnopqrstuvwxyz',
        # 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
        #
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890",
        # 'The quick brown fox jumps over the lazy dog',
        # 'The quick brown fox jumps over the lazy dog.',
        "The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.",
    ]
    for msg in demo:
        hash = MD5().get_md5_hash(msg)
        # print('{0} - {1}'.format(MD5().get_md5_hash(msg), msg))
        print(*hash["message_blocks"], sep="\n")
        print(*hash["operations"], sep="\n")
