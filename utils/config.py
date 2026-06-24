from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str = "https://www.saucedemo.com"
    browser: Literal["chromium", "firefox", "webkit"] = "chromium"
    headless: bool = False
    slow_mo: int = 300
    screenshot_on_failure: bool = True
    video_on_failure: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
