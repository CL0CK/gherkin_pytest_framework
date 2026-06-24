from pages.login_page import LoginPage
from utils.checker import TextElementDTO
from utils.markers import critical, smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@critical
@Gherkin("login.feature", "Login with locked out user")
def test_locked_out_user(login_page: LoginPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")

    with steps.step(1):
        with steps.when():
            login_page.login("locked_out_user", "secret_sauce")
        with steps.then():
            checker.text.check(login_page.ERROR_CONTAINER, TextElementDTO(value_text="Sorry", contains_text=True))
