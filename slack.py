import os
import logging
import requests
from slack_bolt import App
import streamlit as st
   

from dotenv import load_dotenv


load_dotenv()  



logging.basicConfig(level=logging.DEBUG)

app = App(
   token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)


@app.middleware  
def log_request(logger, body, next):
    logger.debug(body)
    next()

@app.command("/lead")
def handle_command(body, ack, client, logger):
    logger.info(body)
    ack()

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "gratitude-modal",
            "title": {"type": "plain_text", "text": "Lead Created Form"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "first_name",
                    "element": {"type": "plain_text_input", "action_id": "first_name"},
                    "label": {"type": "plain_text", "text": "First Name"},
                },
                {
                    "type": "input",
                    "block_id": "last_name",
                    "element": {"type": "plain_text_input", "action_id": "last_name"},
                    "label": {"type": "plain_text", "text": "Last Name"},
                },
                {
                    "type": "input",
                    "block_id": "company",
                    "element": {"type": "plain_text_input", "action_id": "company"},
                    "label": {"type": "plain_text", "text": "Company"},
                },
                {
                    "type": "input",
                    "block_id": "city",
                    "element": {"type": "plain_text_input", "action_id": "city"},
                    "label": {"type": "plain_text", "text": "City"},
                },
                {
                    "type": "input",
                    "block_id": "phone",
                    "element": {"type": "plain_text_input", "action_id": "phone"},
                    "label": {"type": "plain_text", "text": "Phone"},
                },
                {
                    "type": "input",
                    "block_id": "email",
                    "element": {"type": "plain_text_input", "action_id": "email"},
                    "label": {"type": "plain_text", "text": "Email"},
                },
                {
                    "type": "input",
                    "block_id": "status",
                    "element": {"type": "plain_text_input", "action_id": "status"},
                    "label": {"type": "plain_text", "text": "Status"},
                },
            ],
        },
    )
    logger.info(res)

@app.view("gratitude-modal")
def view_submission(ack, body, client, logger):


    
    ack()

    st.write("Submission received!")
    st.write(body["view"]["state"]["values"])
    print('-------------------start-----------------------------')
    print(logger.info(body["view"]["state"]["values"]))
    print('---------------------end---------------------------')
    lead_info = {
        "FirstName": body["view"]["state"]["values"]["first_name"]["first_name"]["value"],
        "LastName": body["view"]["state"]["values"]["last_name"]["last_name"]["value"],
        "Company": body["view"]["state"]["values"]["company"]["company"]["value"],
        "City": body["view"]["state"]["values"]["city"]["city"]["value"],
        "Phone": body["view"]["state"]["values"]["phone"]["phone"]["value"],
        "Email": body["view"]["state"]["values"]["email"]["email"]["value"],
        "Status": body["view"]["state"]["values"]["status"]["status"]["value"],
    }


if __name__ == "__main__":
    app.start(3000)
