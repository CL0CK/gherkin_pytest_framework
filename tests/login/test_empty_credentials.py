from pages.login_page import LoginPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import TextElementDTO
from utils.markers import smoke


@smoke
@Gherkin("login.feature", "Login with empty credentials")
def test_empty_credentials(login_page: LoginPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")

    with steps.step(1):
        with steps.when():
            login_page.click_login()
        with steps.then():
            checker.check_text(login_page.ERROR_CONTAINER, TextElementDTO(value_text="Username is required", contains_text=True))
