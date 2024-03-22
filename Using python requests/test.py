import unittest
from DiscordIntegration import DiscordIntegration


class TestDiscordIntegration(unittest.TestCase):

    def setUp(self):
        # Initialize the DiscordIntegration object for testing
        self.discord_int = DiscordIntegration({"token": "YOUR BOT TOKEN", "channel_id": "YOUR CHANNEL ID"})
        webhooks = self.discord_int.get_all_webhooks()
        if webhooks is not None:
            for webhook in webhooks:
                self.discord_int.use_webhook(webhook['url'])
        else:
            print("Failed to retrieve webhooks.")

    def tearDown(self):
        # Clean up after each test
        self.discord_int.close_executor()

    def test_create_webhook(self):
        # webhook_name = "Test Webhook"
        # webhook_url = self.discord_int.create_webhook(webhook_name)
        self.assertIsNotNone(self.discord_int.webhook_url)

    def test_use_webhook(self):
        self.discord_int.use_webhook(self.discord_int.webhook_url)
        self.assertIsNotNone(self.discord_int.webhook_url)

    def test_get_webhook_info(self):
        self.discord_int.use_webhook(self.discord_int.webhook_url)
        response = self.discord_int.get_webhook_info()
        self.assertIsNotNone(response)

    def test_get_all_webhooks(self):
        webhooks = self.discord_int.get_all_webhooks()
        self.assertIsNotNone(webhooks)
        for webhook in webhooks:
            self.assertIsNotNone(webhook.get("name"))
            self.assertIsNotNone(webhook.get("url"))

    def test_update_webhook(self):
        new_webhook_name = "Updated Webhook Name"
        status_code = self.discord_int.update_webhook(new_webhook_name)
        self.assertEqual(status_code, 200)

    # def test_delete_webhook(self):
    #     status_code = self.discord_int.delete_webhook()
    #     self.assertEqual(status_code, 204)

    def test_send_message(self):
        message = "Hello, this is a test message!"
        message_id = self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)

    def test_edit_message(self):
        message = "Hello, this is a test message!"
        message_id = self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)

        new_message = "This is an edited message!"
        status_code = self.discord_int.edit_message(message_id, new_message)
        self.assertEqual(status_code, 200)

    def test_delete_message(self):
        message = "Hello, this is a test message!"
        message_id = self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)

        status_code = self.discord_int.delete_message(message_id)
        self.assertEqual(status_code, 204)

    def test_pin_and_unpin_message(self):
        message = "Hello, this is a test pin unpin and with image url message!"
        message_id = self.discord_int.send_message(message, image_url="https://media1.tenor.com/m/x8v1oNUOmg4AAAAd/rickroll-roll.gif")
        self.assertIsNotNone(message_id)

        pin_status = self.discord_int.pin_message(message_id)
        self.assertEqual(pin_status, 204)

        unpin_status = self.discord_int.unpin_message(message_id)
        self.assertEqual(unpin_status, 204)

    def test_get_message(self):
        message = "Hello, this is a test message!"
        message_id = self.discord_int.send_message(message)
        self.assertIsNotNone(message_id)

        message_data = self.discord_int.get_message(message_id)
        self.assertIsNotNone(message_data)
        self.assertEqual(message_data["content"], message)

    def test_get_pinned_messages(self):
        pinned_messages = self.discord_int.get_pinned_messages()
        self.assertIsNotNone(pinned_messages)


if __name__ == '__main__':
    unittest.main()
