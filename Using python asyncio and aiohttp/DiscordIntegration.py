import aiohttp
import asyncio
import json


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
        self.session = aiohttp.ClientSession()

    async def close_session(self):
        await self.session.close()

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

    async def create_webhook(self, webhook_name):
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

        async with self.session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                webhook_info = await response.json()
                self.webhook_url = webhook_info['url']
                self.webhook_id = webhook_info['id']
                return self.webhook_url
            else:
                return None

    async def get_webhook_info(self, webhook_url=None):
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

        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

    async def get_all_webhooks(self):
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

        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                webhooks = await response.json()
                return [{"name": webhook["name"], "url": webhook["url"]} for webhook in webhooks]
            else:
                return None

    async def update_webhook(self, webhook_name, webhook_url=None):
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
        async with self.session.patch(url, data=json.dumps(payload), headers=headers) as response:
            return response.status

    async def delete_webhook(self, webhook_url=None):
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

        async with self.session.delete(url, headers=headers) as response:
            if webhook_url is None and self.webhook_url is not None:
                self.webhook_url = None
                self.webhook_id = None
            return response.status

    async def send_message(self, message, image_url=None):
        """
        Sends a message through the webhook.

        Parameters:
            - message: The message to be sent.

        Returns:
            - message_id: The ID of the sent message.
            - response.status: If failed.
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
        async with self.session.post(self.webhook_url + '?wait=true', json=data) as response:
            if response.status == 200:
                return (await response.json()).get('id')
            return response.status

    async def edit_message(self, message_id, new_message):
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
        async with self.session.patch(edit_url, json=data) as response:
            return response.status

    async def delete_message(self, message_id):
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
        async with self.session.delete(delete_url) as response:
            return response.status

    async def get_message(self, message_id):
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

        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

    async def get_pinned_messages(self):
        """
        Retrieves all pinned messages in a channel.

        Returns:
            - pinned_messages: A list of pinned message IDs.
            - response.status: If failed.
        """
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/pins"

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                pinned_messages = []
                for i in await response.json():
                    pinned_messages.append(i["id"])
                return pinned_messages
            return [response.status]

    async def pin_message(self, message_id):
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

        async with self.session.put(url, headers=headers) as response:
            return response.status

    async def unpin_message(self, message_id):
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

        async with self.session.delete(url, headers=headers) as response:
            return response.status


async def main():
    # Create DiscordIntegration object
    discord_int = DiscordIntegration({"token": "MTIxOTU1NTUyNTc3NjI0ODgzMg.GNUJxw.P3qoic93MyvUeEsQ2l4oqOHnNT3t-4XAUoJWKs", "channel_id": "1220124696809308324"})

    webhooks = await discord_int.get_all_webhooks()
    if webhooks is not None:
        print("All Webhooks:")
        for webhook in webhooks:
            print(f"Name: {webhook['name']}, URL: {webhook['url']}")
            discord_int.use_webhook(webhook['url'])
    else:
        print("Failed to retrieve webhooks.")

    # Get Webhook Info
    response = await discord_int.get_webhook_info()
    print("Webhook info: ", response)

    # Send a message and get message ID
    message = "Hello, this is a test message!"
    message_id = await discord_int.send_message(message)
    print("Sent Message ID:", message_id)

    # Pin the message
    pin_status = await discord_int.pin_message(message_id)
    print("Pin Message Status Code:", pin_status)

    # Get all pinned messages
    pinned_messages = await discord_int.get_pinned_messages()
    print("Pinned Messages:", pinned_messages)

    # Unpin the message
    unpin_status = await discord_int.unpin_message(message_id)
    print("Unpin Message Status Code:", unpin_status)

    # Edit the message
    edited_message = "This message has been edited!"
    edit_status = await discord_int.edit_message(message_id, edited_message)
    print("Edit Message Status Code:", edit_status)

    # Get the edited message
    edited_message_data = await discord_int.get_message(message_id)
    print("Edited Message Data:", edited_message_data)

    # Delete the message
    delete_status = await discord_int.delete_message(message_id)
    print("Delete Message Status Code:", delete_status)

    # Send a message and get message ID
    message = "Hello, this is a test message!"
    message_id = await discord_int.send_message(message, "https://images.ctfassets.net/hrltx12pl8hq/28ECAQiPJZ78hxatLTa7Ts/2f695d869736ae3b0de3e56ceaca3958/free-nature-images.jpg?fit=fill&w=1200&h=630")
    print("Sent Message ID:", message_id)

    # Close the session
    await discord_int.close_session()

if __name__ == "__main__":
    asyncio.run(main())

