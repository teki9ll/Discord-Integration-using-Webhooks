import unittest
import asyncio
import warnings
from DiscordIntegration import DiscordIntegration


class TestDiscordIntegration(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.discord_int = DiscordIntegration({"token": "YOUR BOT TOKEN", "channel_id": "YOUR CHANNEL ID"})

        webhooks = await self.discord_int.get_all_webhooks()
        if webhooks is not None:
            print("All Webhooks:")
            for webhook in webhooks:
                print(f"Name: {webhook['name']}, URL: {webhook['url']}")
                self.discord_int.use_webhook(webhook['url'])
        else:
            print("Failed to retrieve webhooks.")

        # Don't use this function to test, because we have limit for only 50 integrations per sever
        # self.discord_int.webhook_url = await self.discord_int.create_webhook("Test_Webhook")

        self.assertIsNotNone(self.discord_int.webhook_id)
        self.assertIsNotNone(self.discord_int.webhook_url)
        print(f"Using Webhook: {self.discord_int.webhook_url}")

    async def asyncTearDown(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        await self.discord_int.close_session()

    async def test_use_webhook(self):
        self.assertIsNotNone(self.discord_int.webhook_id)
        self.assertIsNotNone(self.discord_int.webhook_url)

    async def test_create_webhook(self):
        self.assertIsNotNone(self.discord_int.webhook_id)
        self.assertIsNotNone(self.discord_int.webhook_url)

    async def test_update_webhook(self):
        status_code = await self.discord_int.update_webhook("Updated_Test_Webhook", self.discord_int.webhook_url)
        self.assertEqual(status_code, 200)

    # Don't use this function to test, because we have limit for only 50 integrations per sever
    # async def test_delete_webhook(self):
    #     await self.discord_int.delete_webhook()
    #     self.assertIsNone(self.discord_int.webhook_id)
    #     self.assertIsNone(self.discord_int.webhook_url)

    async def test_send_message(self):
        message = "Hello, this is a test message with embed image url!"
        message_id = await self.discord_int.send_message(message, image_url="https://images.ctfassets.net/hrltx12pl8hq/28ECAQiPJZ78hxatLTa7Ts/2f695d869736ae3b0de3e56ceaca3958/free-nature-images.jpg?fit=fill&w=1200&h=630")
        self.assertIsNotNone(message_id)
        print("Test Send Message Success")

    async def test_get_webhook_info(self):
        response = await self.discord_int.get_webhook_info()
        self.assertIsNotNone(response)
        self.assertIn('name', response)
        self.assertIn('url', response)
        self.assertEqual(response['url'], self.discord_int.webhook_url)
        print(f"Got Webhook: {response['url']}")

    async def test_pin_and_unpin_message(self):
        message = "Test message to pin and unpin"
        message_id = await self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)
        print("Test Send Message to Pin Started...")

        pin_status = await self.discord_int.pin_message(message_id)
        self.assertEqual(pin_status, 204)
        print("Message Pinned...")

        unpin_status = await self.discord_int.unpin_message(message_id)
        self.assertEqual(unpin_status, 204)
        print("Message Unpinned...")

    async def test_edit_message(self):
        message = "Original message to edit"
        message_id = await self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)

        new_message = "Edited message"
        edit_status = await self.discord_int.edit_message(message_id, new_message)
        self.assertEqual(edit_status, 200)

        edited_message_data = await self.discord_int.get_message(message_id)
        self.assertEqual(edited_message_data['content'], new_message)

    async def test_delete_message(self):
        message = "Message to delete"
        message_id = await self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)

        delete_status = await self.discord_int.delete_message(message_id)
        self.assertEqual(delete_status, 204)


if __name__ == "__main__":
    try:
        asyncio.run(unittest.main())
    except Exception as e:
        print(e)
