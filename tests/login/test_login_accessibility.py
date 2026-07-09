from pages.login_page import LoginPage
from utils.checker import UIChecker
from utils.markers import smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@Gherkin("login.feature", "Login page accessibility check")
def test_login_accessibility(
    login_page: LoginPage,
    steps: Steps,
    checker: UIChecker,
) -> None:
    with steps.given("User is on the SauceDemo login page"):
        login_page.navigate("/")

    with steps.then("Page should meet accessibility standards"):
        checker.accessibility.check_accessibility()
