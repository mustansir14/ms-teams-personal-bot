import jwt
import pandas as pd

from internal.env import Env
from internal.teams_client import TeamsClient
from internal.exceptions import ResourceNotFoundException

from colorama import Fore
from datetime import datetime



def send_message(user_email: str, message_to_send: str):    

    teams_client = TeamsClient(Env.SEARCH_TOKEN, Env.MESSAGE_TOKEN, Env.SKYPE_TOKEN)

    # Get user by email
    user = teams_client.get_user_by_email(user_email)
        
    user_id = user["mri"]

    decoded_token = jwt.decode(Env.SKYPE_TOKEN, options={"verify_signature": False})
    skype_id = decoded_token.get("skypeid")

    # get chat
    chat_id = teams_client.create_chat(skype_id, user_id)

    # send_message in chat
    teams_client.send_message(chat_id, skype_id, message_to_send)


if __name__ == "__main__":

    filename = input("Enter file path: ")
    column_index = int(input("Enter Email column number: ")) - 1
    while True:
        header_exists = input("Does the file have a header row?: (y/n)")
        if header_exists.lower() == "y":
            header_exists_bool = True
            break
        elif header_exists.lower() == "n":
            header_exists_bool = False
            break
        else:
            continue
    message_to_send = input("Enter message to send: ")

    if header_exists_bool:
        df = pd.read_excel(filename)
        column_name = df.columns[column_index]
    else:
        df = pd.read_excel(filename, header=None)
        column_name = column_index

    df.rename({column_name: "email"}, axis=1, inplace=True)
    new_df = pd.DataFrame()

    current_time = str(datetime.now().isoformat())[:23]

    for index, row in df.iterrows():

        new_df.loc[index, "Email"] = row["email"]
        try:
            send_message(row["email"], message_to_send)
            new_df.loc[index, "status"] = "Success"
            print(Fore.GREEN + "Sent message to " + row["email"])
        except ResourceNotFoundException:
            new_df.loc[index, "status"] = "Not Found"
            print(Fore.YELLOW + f"Email {row['email']} not found")
        except Exception as e:
            new_df.loc[index, "status"] = "Error"
            new_df.loc[index, "reason"] = str(e)
            print(Fore.RED + f"Error sending message to {row['email']} Error: {str(e)}")

        new_df.to_excel(filename.replace(".xlsx", f"_Results_{current_time}.xlsx"), index=False)


    