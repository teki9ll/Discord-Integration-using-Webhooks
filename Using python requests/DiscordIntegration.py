import requests
import json
from concurrent.futures import ThreadPoolExecutor


class DiscordIntegration:
    def __init__(self, secrets):
        """
        Initializes the DiscordIntegration object.

        Parameters:
            - secrets: A dictionary containing the required keys (token, channel_id).
        """
        self.token = secrets["token"]
        self.channel_id = secrets["channel_id"]
        self.webhook_url = None
        self.webhook_id = None
        self.executor = ThreadPoolExecutor(max_workers=10)

    def close_executor(self):
        self.executor.shutdown()

    def use_webhook(self, webhook_url):
        """
        Sets the webhook URL and id to use for subsequent requests.

        Parameters:
            - webhook_url: The URL of the webhook to use.

        Returns:
            - None
        """
        self.webhook_url = webhook_url
        url = webhook_url.split('/')
        self.webhook_id = url[-2]

    def create_webhook(self, webhook_name):
        """
        Creates a webhook in the specified Discord channel.

        Parameters:
            - webhook_name: The name of the webhook to be created.

        Returns:
            - webhook_url: The URL of the created webhook.
            - None: If creation fails
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks"

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "name": webhook_name
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            webhook_info = response.json()
            self.webhook_url = webhook_info['url']
            self.webhook_id = webhook_info['id']
            return self.webhook_url
        else:
            return None

    def get_webhook_info(self, webhook_url=None):
        """
        Retrieves information about the current webhook or provided webhook_url.

        Parameters:
            - webhook_url: The URL of the webhook to retrieve information.

        Returns:
            - response: The response object containing webhook information.
            - None: If retrieval fails
        """
        if self.webhook_url is None or self.webhook_id is None:
            print("Webhook URL or ID is not set. Use 'use_webhook' or 'create_webhook' first.")
            return None

        webhook_id = self.webhook_id
        if webhook_url is not None:
            url = webhook_url.split('/')
            webhook_id = url[-2]

        url = f"https://discord.com/api/v9/webhooks/{webhook_id}"

        headers = {
            "Authorization": f"Bot {self.token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_all_webhooks(self):
        """
        Retrieves all webhooks in the specified Discord channel.

        Returns:
            - webhooks: A list of dictionaries containing webhook name and URL.
            - None: If retrieval fails
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks"

        headers = {
            "Authorization": f"Bot {self.token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            webhooks = response.json()
            return [{"name": webhook["name"], "url": webhook["url"]} for webhook in webhooks]
        else:
            return None

    def update_webhook(self, webhook_name, webhook_url=None):
        """
        Updates the webhook with a new name.

        Parameters:
            - webhook_name: The new name for the webhook.
            - webhook_url: The URL of the webhook to update.

        Returns:
            - status_code: HTTP status code of the update request.
        """
        if self.webhook_url is None or self.webhook_id is None and webhook_url is None:
            print("Webhook URL or ID is not set. Use 'use_webhook' or 'create_webhook' first.")
            return None

        webhook_id = self.webhook_id
        if webhook_url is not None:
            url = webhook_url.split('/')
            webhook_id = url[-2]

        url = f"https://discord.com/api/v9/webhooks/{webhook_id}"

        payload = {
            "name": webhook_name
        }
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.patch(url, data=json.dumps(payload), headers=headers)
        return response.status_code

    def delete_webhook(self, webhook_url=None):
        """
        Deletes the webhook.

        Parameters:
            - webhook_url: The URL of the webhook to delete.

        Returns:
            - status_code: HTTP status code of the delete request.
        """
        if self.webhook_url is None or self.webhook_id is None and webhook_url is None:
            print("Webhook URL or ID is not set. Use 'use_webhook' or 'create_webhook' first.")
            return None

        webhook_id = self.webhook_id
        if webhook_url is not None:
            url = webhook_url.split('/')
            webhook_id = url[-2]

        url = f"https://discord.com/api/v9/webhooks/{webhook_id}"

        headers = {
            "Authorization": f"Bot {self.token}"
        }

        response = requests.delete(url, headers=headers)
        if webhook_url is None and self.webhook_url is not None:
            self.webhook_url = None
            self.webhook_id = None
        return response.status_code

    def send_message(self, message, image_url=None):
        """
        Sends a message through the webhook.

        Parameters:
            - message: The message to be sent.

        Returns:
            - message_id: The ID of the sent message.
            - response.status_code: If failed.
        """
        if self.webhook_url is None or self.webhook_id is None:
            print("Webhook URL or ID is not set. Use 'use_webhook' or 'create_webhook' first.")
            return None

        data = {
            'content': message
        }
        if image_url is not None:
            data = {
                'content': message,
                'embeds': [
                    {
                        'image': {
                            'url': image_url
                        }
                    }
                ]
            }
        response = requests.post(self.webhook_url + '?wait=true', json=data)
        if response.status_code == 200:
            return response.json().get('id')
        return response.status_code

    def edit_message(self, message_id, new_message):
        """
        Edits a message sent through the webhook.

        Parameters:
            - message_id: The ID of the message to be edited.
            - new_message: The new content of the message.

        Returns:
            - status_code: HTTP status code of the edit request.
        """
        if self.webhook_url is None or self.webhook_id is None:
            print("Webhook URL or ID is not set. Use 'use_webhook' or 'create_webhook' first.")
            return None

        edit_url = f"{self.webhook_url}/messages/{message_id}"
        data = {
            'content': new_message
        }
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.patch(edit_url, json=data, headers=headers)
        return response.status_code

    def delete_message(self, message_id):
        """
        Deletes a message sent through the webhook.

        Parameters:
            - message_id: The ID of the message to be deleted.

        Returns:
            - status_code: HTTP status code of the delete request.
        """
        if self.webhook_url is None or self.webhook_id is None:
            print("Webhook URL or ID is not set. Use 'use_webhook' or 'create_webhook' first.")
            return None

        delete_url = f"{self.webhook_url}/messages/{message_id}"
        headers = {
            "Authorization": f"Bot {self.token}"
        }
        response = requests.delete(delete_url, headers=headers)
        return response.status_code

    def get_message(self, message_id):
        """
        Retrieves a message by its ID.

        Parameters:
            - message_id: The ID of the message to retrieve.

        Returns:
            - message_data: A dictionary containing the message data.
            - None: If message is not found
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages/{message_id}"

        headers = {
            "Authorization": f"Bot {self.token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_pinned_messages(self):
        """
        Retrieves all pinned messages in a channel.

        Returns:
            - pinned_messages: A list of pinned message IDs.
            - response.status_code: If failed.
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/pins"

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pinned_messages = []
            for i in response.json():
                pinned_messages.append(i["id"])
            return pinned_messages
        return [response.status_code]

    def pin_message(self, message_id):
        """
        Pins a message in a channel.

        Parameters:
            - message_id: The ID of the message to be pinned.

        Returns:
            - status_code: HTTP status code of the pinning action.
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/pins/{message_id}"

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers)
        return response.status_code

    def unpin_message(self, message_id):
        """
        Unpins a message in a channel.

        Parameters:
            - message_id: The ID of the message to be unpinned.

        Returns:
            - status_code: HTTP status code of the unpinning action.
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/pins/{message_id}"

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.delete(url, headers=headers)
        return response.status_code


