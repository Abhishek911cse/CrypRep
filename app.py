from flask import Flask, render_template, request
import random
from CrypRep.DES import run_des
from CrypRep.AES import AES
from CrypRep.RSA import RSA
from CrypRep.MD5 import MD5

app = Flask(__name__, template_folder="templates", static_folder="static")


def is_hex(string):
    """Check if entered value is hex:"""
    try:
        int(string, 16)
        return True
    except ValueError:
        return False


def get_hex(text):
    """Get hex value from entered string"""
    text_byte_array = list(map(bin, bytearray(text, encoding="utf-8")))
    text_byte_array_string = "".join([foo[2:] for foo in text_byte_array])
    return str(hex(int(text_byte_array_string, 2))[2:].upper())


def get_hex_array(string):
    return [int(string[i : i + 2], 16) for i in range(0, len(string), 2)]


def fixed_len_hex(string):
    return "{0:#034x}".format(int(string, 16))[2:]


@app.route("/")
def load_home_page():
    """Display Home page:"""
    return render_template("index.html")


@app.route("/des/", methods=["POST", "GET"])
def des_page():
    """Display data from DES calculations:"""
    if request.method == "POST":
        message = request.form["message"]
        key = request.form["key"]
        # Errors:
        # 1 - empty message or key field
        # 2- key is not hex value
        if message or key is not None:
            if not is_hex(key):
                return render_template("page_des.html", error_no="2")
            else:
                errors = list()
                if not is_hex(message):
                    message = get_hex(message)
                    errors.append(
                        "Message was not hex so it was converted to hex value which is: {}".format(
                            message
                        )
                    )
                if len(key) > 16:
                    key = key[:16]
                    errors.append(
                        "Key was longer than 16 symbols, it was shortened to: {}".format(
                            key
                        )
                    )
                # Check if   there are errors:
                errors = None if len(errors) == 0 else errors
                action = request.form["action_options"]
                print(action)
                if action == "encrypt":
                    encryption_values = run_des(message, key, action)
                    return render_template(
                        "page_des.html",
                        print_action=action,
                        message=message,
                        key=key,
                        encryption_values=encryption_values,
                        errors=errors,
                    )
                elif action == "decrypt":
                    decryption_values = run_des(message, key, action)
                    return render_template(
                        "page_des.html",
                        print_action=action,
                        message=message,
                        key=key,
                        decryption_values=decryption_values,
                        errors=errors,
                    )
                else:
                    encryption_values = run_des(message, key, "encrypt")
                    decryption_values = run_des(
                        encryption_values["Cipher"], key, "decrypt"
                    )
                    return render_template(
                        "page_des.html",
                        print_action="both",
                        message=message,
                        key=key,
                        encryption_values=encryption_values,
                        decryption_values=decryption_values,
                        errors=errors,
                    )
        else:
            return render_template("page_des.html", error_no="1")
    else:
        return render_template("page_des.html")


@app.route("/aes/", methods=["POST", "GET"])
def aes_page():
    """Display data from AES calculations:"""
    if request.method == "POST":
        message = request.form["message"]
        key = request.form["key"]
        # Errors:
        # 1 - empty message or key field
        # 2 - key is not hex value
        # 3 - message is not hex value
        if message or key is not None:
            if not is_hex(key):
                return render_template("page_aes.html", error_no="2")
            elif not is_hex(message):
                return render_template("page_aes.html", error_no="3")
            else:
                message = fixed_len_hex(message)
                key = fixed_len_hex(key)
                aes = AES()
                aes_data = aes.do_rounds(
                    message=get_hex_array(message), key=get_hex_array(key)
                )
                return render_template(
                    "page_aes.html", message=message, key=key, data=aes_data
                )
        else:
            return render_template("page_aes.html", error_no="1")
    else:
        return render_template("page_aes.html")


@app.route("/rsa/", methods=["POST", "GET"])
def rsa_page():
    """Display data from DES calculations:"""
    if request.method == "POST":
        message = int(request.form["message"])
        e = int(request.form["e"])
        p = int(request.form["p"])
        q = int(request.form["q"])
        # Errors:
        # 1 - empty value
        # 2 - numbers are not prime
        # 3 - e is not relatively prime to (p-1)*(q-1)
        if message and e and p and q is not None:
            rsa = RSA()
            # Check for primeness and relative primeness:
            if not rsa.is_prime(p):  # is_hex(e):
                return render_template("page_rsa.html", error_no="2", number=p)
            elif not rsa.is_prime(q):
                return render_template("page_rsa.html", error_no="2", number=q)
            else:
                if not rsa.is_relatively_prime(e, (p - 1) * (q - 1)):
                    return render_template("page_rsa.html", error_no="3", number=e)
                else:
                    action = request.form["action_options"]
                    print(action)
                    return render_template(
                        "page_rsa.html",
                        message=message,
                        p=p,
                        q=q,
                        e=e,
                        rsa=rsa.do_rsa(message, p, q, e, action),
                    )
        else:
            return render_template("page_rsa.html", error_no="1")
    else:
        return render_template("page_rsa.html")


@app.route("/md5/", methods=["POST", "GET"])
def md5_page():
    if request.method == "POST":
        message = request.form["message"]
        action = request.form["action_options"]
        # Errors:
        # 1 - empty value
        # if message is not None:
        hash = MD5().get_md5_hash(message)
        if action == "all_steps":
            return render_template(
                "page_md5.html",
                message=message,
                hash=hash["hash"],
                show_all=True,
                operations_data=hash,
            )
        else:
            return render_template("page_md5.html", message=message, hash=hash["hash"])
        # else:
        # return render_template('page_md5.html', error_no='1')
    else:
        return render_template("page_md5.html")


if __name__ == "__main__":
    app.run(debug=True)