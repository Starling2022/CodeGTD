from os import system

libs = ["pycryptodome", "base64", "requests", "json"]

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    import base64
    import requests
    import json
except:
    for el in libs:
        system("pip install %s" % el)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
import json

import random

BASE_URL = "http://211.253.26.47:8093/TOWERDEFENCE_AMO/"

SERVER = "AMO"

USER_AGENT = random.choice(
    [
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    ]
)

# AES secret key and iv
key = b"gksekf1djrqjfwk!"
iv = b"towerdefence_amo"


def encrypt(string_to_encrypt: str) -> str:
    padded_data = pad(string_to_encrypt.encode("utf-8"), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt(encrypted_string: str) -> str:
    encrypted_data = base64.b64decode(encrypted_string)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode("utf-8")


def postWithEncryptedData(url: str, data: dict):
    return requests.post(
        BASE_URL + url,
        params={"DATA": encrypt(json.dumps(data))} if url.endswith("AES.php") else data,
        headers={
            "User-Agent": USER_AGENT,
            "X-Requested-With": "busidol.mobile.tower",
        },
    ).text


class GTDHack:
    def __init__(self, id: str) -> None:
        self.id = id
        print(">> Counter server ++")
        postWithEncryptedData(
            "Counter/daily_run_count.php", {"UNIQ_ID": self.id}
        )  # Cái này để runcount lên server. Đại loại là để check in cho mỗi lần đăng nhập
        self.runCount = int(
            postWithEncryptedData(
                "../TOWERDEFENCE_COMMON/MOBILE_CONNECT/get_run_count_AES.php",
                {"PLATFORM": SERVER, "UNIQ_ID": self.id},
            )
        )  # Cái này để lấy số run count hiện tại rồi lưu vào self.runCount
        print(">> Get run count:", self.runCount)

    def getUserData(self):
        return postWithEncryptedData("get_user_data_all_AES.php", {"UNIQ_ID": self.id})

    def addRuby(self, amount: int):
        currentUser = json.loads(
            self.getUserData()
        )  # Lấy số ruby, dia, gold, mileage hiện tại từ server

        currentUserRubyDiaGold = currentUser["VALUE"]["rubydiagold"]["value"]

        print(">> Current user ruby dia gold value: ", currentUserRubyDiaGold)

        return postWithEncryptedData(
            "put_userinfo_rubydiagold_AES.php",
            {
                "UNIQ_ID": self.id,
                "CUR_RUBY": currentUserRubyDiaGold["RUBY"],
                "CUR_DIA": currentUserRubyDiaGold["DIA"],
                "CUR_GOLD": currentUserRubyDiaGold["GOLD"],
                "CUR_MILEAGE": currentUserRubyDiaGold["MILEAGE"],
                "RUBY_ADD": amount,
                "RUBY_WHY": "우편함 모두받기",  # Lấy tạm lí do là nhận hộp thư
                "DIA_ADD": 0,
                "DIA_WHY": "",
                "GOLD_ADD": 0,
                "GOLD_WHY": "",
                "MILEAGE_ADD": 0,
                "MILEAGE_WHY": "",
                "RUN_COUNT": self.runCount,
            },
        )  # Không sửa code vì có thể lỗi không hack dc


def main() -> None:
    user = GTDHack("TDM56446")

    result = user.addRuby(100)
    # Hack với số lượng ít để tránh bị band
    print(
        ">> Add result: %s %s"
        % (
            result,
            "\n IP blocked"
            if json.loads(result)["VALUE"] == "(I)You are blocked!!"
            else "",
        ),
    )

    # Nếu acc không bị khoá nhưng lại trả về như này {"RESULT":"ERROR","VALUE":"(I)You are blocked!!","COMMENT":"empty"} thì là bị block ip


main()