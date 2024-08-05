import requests
import json


class ABCMART:
    def __init__(self):
        self.url = "https://abcmart.a-rt.com/product/info?prdtNo="

    def url_setting(self, url):
        return url.split("&")[0].split("prdtNo=")[-1]

    def login(self, input):
        url = "https://grandstage.a-rt.com/"
        req = requests.get(url)
        JSESSIONID = str(req.cookies).split("JSESSIONID=")[-1].split(" for")[0]
        WMONID = str(req.cookies).split("WMONID=")[-1].split(" for")[0]
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) ApplewebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148APP_IOS_F",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={JSESSIONID}; " f"WMONID={WMONID}",
        }
        url = "https://grandstage.a-rt.com/login/login-processing"
        data = f'loginType=member&username={input["id"]}&password={input["pw"]}'
        req = requests.post(url, data=data, headers=header)
        UID = str(req.cookies).split("UID=")[-1].split(" for")[0]
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) ApplewebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148APP_IOS_F",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={JSESSIONID}; " f"WMONID={WMONID}; " f"UID={UID}",
        }
        return header

    def run(self, input):
        product_code = input['url']
        if "abcmart" in product_code:
            product_code = self.url_setting(product_code)
            header = self.login(input)
            req = requests.get(self.url + product_code, headers=header)
            output = {
                "Name": req.json()["prdtName"],
                "Model": req.json()["styleInfo"],
                "Image": req.json()["productImage"][0]["imageUrl"],
                "Price": str(req.json()["displayProductPrice"]),
                "Url": "https://abcmart.a-rt.com/product/new?prdtNo="
                + str(product_code),
                "Stock": {},
            }
            for i in req.json()["productOption"]:
                data = {str(i["optnName"]): str(i["orderPsbltQty"])}
                output["Stock"].update(data)
            return output
        elif "grandstage.a-rt." in product_code:
            product_code = self.url_setting(product_code)
            header = self.login(input)
            req = requests.get(self.url + product_code, headers=header)
            output = {
                "Name": req.json()["prdtName"],
                "Model": req.json()["styleInfo"],
                "Image": req.json()["productImage"][0]["imageUrl"],
                "Price": str(req.json()["displayProductPrice"]),
                "Url": "https://grandstage.a-rt.com/product/new?prdtNo="
                + str(product_code),
                "Stock": {},
            }

            for i in req.json()["productOption"]:
                data = {str(i["optnName"]): str(i["orderPsbltQty"])}
                output["Stock"].update(data)
            return output
# data = {
#     'url':'https://grandstage.a-rt.com/product/new?prdtNo=1020102173',
#     'id':'ABC계정',
#     'pw': 'ABC암호'
# }
#
# print(json.dumps(ABCMART().run(data), ensure_ascii=False, indent=4))
