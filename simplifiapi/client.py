import logging
import requests
import uuid

logger = logging.getLogger("simplifiapi")


class Client():

    def __init__(self):
        self.session = requests.Session()

    def get_token(self, email, password):
        # Step 1: Oauth authorize
        body = {
            "clientId": "acme_web",
            "mfaChannel": None,
            "mfaCode": None,
            "password": password,
            "redirectUri": "https://app.simplifimoney.com/login",
            "responseType": "code",
            "threatMetrixRequestId": None,
            "threatMetrixSessionId": str(uuid.uuid4()),
            "username": email,
        }
        r = self.session.post(
            url="https://services.quicken.com/oauth/authorize", json=body)
        data = r.json()
        status = data.get("status")
        if (status == "MFA code sent"):
            mfaChannel = data.get("mfaChannel")
            logger.warning("MFA Channel: {}".format(mfaChannel))
            mfaCode = input("MFA Code: ")
            body["mfaChannel"] = mfaChannel
            body["mfaCode"] = mfaCode
            r = requests.post(
                url="https://services.quicken.com/oauth/authorize", json=body)
            r.raise_for_status()
            data = r.json()
            status = data.get("status")
            if (status != "User passed MFA"):
                logger.error("Login failed.")
                logger.error(r.json())
                return
        code = r.json().get("code")

        # Step 2: Get token
        r = self.session.post(url="https://services.quicken.com/oauth/token",
                              json={
                                  "clientId": "acme_web",
                                  "clientSecret": "BCDCxXwdWYcj@bK6",
                                  "grantType": "authorization_code",
                                  "code": code,
                                  "redirectUri": "https://app.simplifimoney.com/login"
                              })
        r.raise_for_status()
        token = r.json().get("accessToken")

        logger.warn("Retrieved token {}".format(token))

        return token

    def verify_token(self, token) -> bool:
        headers = {"Authorization": "Bearer {}".format(token)}

        r = self.session.get(url="https://services.quicken.com/userprofiles/me",
                             headers=headers)
        if (r.status_code != 200):
            logger.error("Error code: {}".format(r.status_code))
            logger.error(r.json())
            return False
        data = r.json()
        userId = data.get("id")
        logger.warn("User {} logged in.".format(userId))

        # Update session
        self.session.headers.update(headers)

        return True

    def get_datasets(self, limit: int = 1000):
        r = self.session.get(url="https://services.quicken.com/datasets",
                             params={
                                 limit: limit,
                             })
        r.raise_for_status()
        data = r.json().get("resources")
        return data

    def get_transactions(self, datasetId: str, limit: int = 1000):
        r = self.session.get(url="https://services.quicken.com/transactions",
                             headers={
                                 "Qcs-Dataset-Id": datasetId,
                             },
                             params={
                                 limit: limit,
                             })
        r.raise_for_status()
        data = r.json().get("resources")
        return data