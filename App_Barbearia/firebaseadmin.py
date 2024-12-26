import firebase_admin
from firebase_admin import credentials, db


class FirebaseAdmin:
    def __init__(self) :

        self.cred = credentials.Certificate("service_account_key\\users-arbearia-firebase-adminsdk-b4ajg-0d9ef628c3.json")
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': "https://users-arbearia-default-rtdb.firebaseio.com/"
        })
    