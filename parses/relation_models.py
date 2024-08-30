#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-08-30 15:30
# describe：使用dify构建的关系提取应用（底座为llama3.1:8b）对文本进行关系提取

import json
import requests

from parses import configs

class ChatMessageAPI:
    def __init__(self, base_url, api_key):
        """
        Initialize the API client with the base URL and API key.

        :param base_url: The base URL of the API endpoint.
        :param api_key: The API key for authorization.
        """
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def send_chat_message(self, query, user, files=None, response_mode='blocking', conversation_id=""):
        """
        Send a chat message to the API.

        :param query: The query to be sent.
        :param user: The user identifier.
        :param files: A list of files to be included in the request (default: None).
        :param response_mode: The mode of the response (default: 'blocking'). blocking or streaming
        :param conversation_id: The conversation ID (default: empty string).
        :return: The response from the API.
        """
        data = {
            "inputs": {},
            "query": query,
            "response_mode": response_mode,
            "conversation_id": conversation_id,
            "user": user,
            "files": files if files else []
        }

        # Make the POST request
        response = requests.post(self.base_url, headers=self.headers, json=data)
        # Handle the response
        if response.status_code == 200:
            return json.loads(response.json().get('answer'))
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None


api_client = None

def get_api_client():
    global api_client
    if not api_client:
        api_client = ChatMessageAPI(
            base_url=f'{configs.API_URL}/chat-messages',
            api_key=configs.AUTHORIZATION
        )
    return api_client


if __name__ == "__main__":

    # Define the files to be sent
    # files = [
    #     {
    #         "type": "image",
    #         "transfer_method": "remote_url",
    #         "url": "https://cloud.dify.ai/logo/logo-site.png"
    #     }
    # ]
    files = []

    # Send a chat message
    result = get_api_client().send_chat_message(
        query="高捷，祖籍江苏，本科毕业于东南大学。",
        user=configs.USER_NAME,
        files=files
    )
    print(result)
    