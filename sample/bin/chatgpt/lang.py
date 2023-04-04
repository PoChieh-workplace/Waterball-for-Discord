class lang:
    def __init__(self,strs:str) -> None:
        match strs:
            case "zh_tw":
                self.l = "請使用繁體中文"
            case "zh_cn":
                self.l = "请使用简体中文"
            case "en":
                self.l = "Please communicate with english"
            case "ja":
                self.l = "日本語を話します"
            case _:
                raise Exception("語言代號錯誤")

    def __repr__(self) -> str:
        return self.l
