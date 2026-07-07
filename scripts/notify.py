"""
Notification adapter for test report delivery.

Usage:
    export NOTIFY_ADAPTER=slack
    export SLACK_WEBHOOK_URL=https://hooks.slack.com/...

    poetry run python scripts/notify.py "Message" "path/to/report.png"
"""

from abc import ABC, abstractmethod
import os
from pathlib import Path
import sys


class NotificationAdapter(ABC):
    @abstractmethod
    def send(self, message: str, image_path: str | None = None) -> None: ...


class SlackAdapter(NotificationAdapter):
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send(self, message: str, image_path: str | None = None) -> None:
        import requests

        payload = {
            "text": message,
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message},
                }
            ],
        }

        if image_path and Path(image_path).exists():
            with open(image_path, "rb") as f:
                files = {"file": f}
                requests.post(self.webhook_url, files=files, data=payload, timeout=10)  # nosec B113
        else:
            requests.post(self.webhook_url, json=payload, timeout=10)  # type: ignore[arg-type]


class TelegramAdapter(NotificationAdapter):
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send(self, message: str, image_path: str | None = None) -> None:
        import requests

        if image_path and Path(image_path).exists():
            with open(image_path, "rb") as f:
                files = {"photo": f}
                data = {"chat_id": self.chat_id, "caption": message}
                requests.post(f"{self.api_url}/sendPhoto", files=files, data=data, timeout=10)  # nosec B113
        else:
            requests.post(
                f"{self.api_url}/sendMessage",
                json={"chat_id": self.chat_id, "text": message},
                timeout=10,  # nosec B113
            )


def get_adapter() -> NotificationAdapter:
    adapter_name = os.environ.get("NOTIFY_ADAPTER", "").lower()

    if adapter_name == "slack":
        webhook = os.environ.get("SLACK_WEBHOOK_URL")
        if not webhook:
            raise ValueError("SLACK_WEBHOOK_URL not set")
        return SlackAdapter(webhook)

    if adapter_name == "telegram":
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        return TelegramAdapter(bot_token, chat_id)

    raise ValueError(f"Unknown NOTIFY_ADAPTER: {adapter_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: poetry run python scripts/notify.py <message> [image_path]")
        sys.exit(1)

    message = sys.argv[1]
    image_path = sys.argv[2] if len(sys.argv) > 2 else None

    adapter = get_adapter()
    adapter.send(message, image_path)
    print("Notification sent.")
