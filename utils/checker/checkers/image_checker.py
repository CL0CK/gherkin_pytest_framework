import os
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import Locator, Page

from utils.allure.step import CheckStep
from utils.config import Settings
from utils.element import Element, resolve_locator


class ImageChecker:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._settings = Settings()

    def _locator(self, element: Element | Locator) -> Locator:
        return resolve_locator(self._page, element)

    def _get_baseline_path(self, baseline_name: str) -> Path:
        return Path(self._settings.visual_baseline_path) / f"{baseline_name}.png"

    def _compare_images(self, img1: Image.Image, img2: Image.Image) -> float:
        diff = ImageChops.difference(img1, img2)
        stat = ImageStat.Stat(diff)
        # Calculate percentage of difference based on mean pixel values
        return sum(stat.mean) / (255 * 3) * 100

    @CheckStep
    def check_screenshot(
        self,
        element: Element | Locator,
        baseline_name: str,
        threshold: float = 1.0,
        ignore_regions: list[dict] | None = None
    ) -> None:
        locator = self._locator(element)
        actual_path = Path("temp_actual.png")
        baseline_path = self._get_baseline_path(baseline_name)

        # Capture actual state
        locator.screenshot(path=str(actual_path))

        if self._settings.image_mode == "update":
            actual_img = Image.open(actual_path)
            actual_img.save(baseline_path)
            os.remove(actual_path)
            print(f"Baseline updated: {baseline_path}")
            return

        if not baseline_path.exists():
            os.remove(actual_path)
            raise FileNotFoundError(
                f"Baseline image not found at {baseline_path}. "
                f"Run with IMAGE_MODE=update to create it."
            )

        # Comparison logic
        img_actual = Image.open(actual_path).convert("RGB")
        img_baseline = Image.open(baseline_path).convert("RGB")

        if img_actual.size != img_baseline.size:
            os.remove(actual_path)
            raise AssertionError(f"Image dimensions mismatch: {img_actual.size} vs {img_baseline.size}")

        diff_percent = self._compare_images(img_actual, img_baseline)

        if diff_percent > threshold:
            # Save diff image for Allure if needed here
            os.remove(actual_path)
            raise AssertionError(
                f"Visual difference detected: {diff_percent:.2f}% "
                f"exceeds threshold {threshold}%"
            )

        os.remove(actual_path)
