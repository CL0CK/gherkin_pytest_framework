from pages.login_page import LoginPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import TextElementDTO
from utils.markers import smoke


@smoke
@Gherkin("login.feature", "Login with invalid credentials")
def test_invalid_credentials(login_page: LoginPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")

    with steps.step(1):
        with steps.when():
            login_page.login("invalid_user", "invalid_password")
        with steps.then():
            checker.check_text(login_page.ERROR_CONTAINER, TextElementDTO(value_text="do not match", contains_text=True))
