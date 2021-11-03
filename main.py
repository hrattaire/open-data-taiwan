import os
from dotenv import load_dotenv



if __name__ == "__main__":
    load_dotenv()
    print(f"ID: {os.environ['APP_ID']}")

