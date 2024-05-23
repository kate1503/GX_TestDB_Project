import os
import dotenv

dotenv.load_dotenv('.env')

USERID = os.environ['USERID']
PASSWORD = os.environ['PASSWORD']
SERVER_PORT = os.environ['SERVER_PORT']
