# PROJECT.md — Context for LLM Agents

## 1. Context

**What it is:** Playwright BDD testing framework with custom Gherkin parser and strict step-by-step verification.

**Goals:** e2e test automation, Allure reporting, strict `.feature` ↔ code verification, scalable test architecture.

**Stack:** Python 3.11+, Playwright, pytest, pytest-xdist, allure-pytest, pydantic-settings, loguru, Poetry.

## 2. Architecture

```
┌──────────────────────────────────────────────────────┐
│              CI/CD (GitHub Actions)                   │
│  lint → test → allure-report → pages-deployment       │
└──────────────────────┬───────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────┐
│                    conftest.py                        │
│  playwright → browser → context → page → config      │
│  checker, steps, users_data, products_data           │
└──────────────────────┬───────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────┐
│                 tests/ (Gherkin tests)                │
│  @Gherkin("file", "scenario")                         │
│  steps.given/when/then() → checker.*                 │
└──────────┬──────────────────────┬────────────────────┘
           │                      │
┌──────────▼──────────┐  ┌──────▼──────────────┐
│  pages/             │  │  pages/components/   │
│  Page Objects       │  │  Component Objects   │
│  (BasePage)         │  │  (ProductCard,       │
│  LoginPage, etc.    │  │   CartLineItem)      │
└─────────────────────┘  └─────────────────────┘
           │
┌──────────▼──────────────────────────────────────┐
│  utils/                                          │
│  gherkin_parser.py → parse_feature_file()       │
│  steps_wrapper.py → @Gherkin + Steps            │
│  checker/ → UIChecker (text, button, count)     │
│  element.py → Element + resolve_locator()        │
│  config.py → Settings (pydantic-settings)       │
│  logger.py → loguru wrapper                     │
└──────────────────────────────────────────────────┘
```

## 3. Key Files

### core
- **`conftest.py`** — session/func fixtures: playwright, browser, context, page, config; allure hooks (screenshot/video/log on failure)
- **`tests/conftest.py`** — page fixtures (login_page, products_page, cart_page, checkout_page), checker, steps, users_data, products_data
- **`utils/config.py`** — Settings (pydantic-settings), reads `.env`

### gherkin
- **`utils/gherkin_parser.py`** — parses `.feature` files → GherkinFeature / GherkinScenario / GherkinStep
- **`utils/steps_wrapper.py`** — `@Gherkin` decorator (binding + allure labeling + auto-parametrize); Steps (given/when/then + 1-to-1 verification)

### checkers
- **`utils/checker/ui_checker.py`** — UIChecker: common, text, button, count
- **`utils/checker/checkers/common_checker.py`** — check_presence (is_visible/is_hidden), check_attribute, check_color
- **`utils/checker/checkers/text_checker.py`** — check_text, check_font
- **`utils/checker/checkers/button_checker.py`** — button checks
- **`utils/checker/checkers/count_checker.py`** — count verification
- **`utils/checker/dto.py`** — ElementDTO, TextElementDTO, ButtonElementDTO, ImageElementDTO, CountDTO
- **`utils/checker/mixins.py`** — PresenceMixin, ValueTextMixin, ValueColorMixin, ValueFontMixin

### pages
- **`pages/base_page.py`** — BasePage (navigate, get_url, wait_for_url, take_screenshot); `__init_subclass__` auto-names Element attributes
- **`pages/login_page.py`** — LoginPage (username, password, login, error)
- **`pages/products_page.py`** — ProductsPage (product_by_name, click_cart_icon, logout)
- **`pages/cart_page.py`** — CartPage (cart_line_item, click_checkout, click_continue_shopping)
- **`pages/checkout_page.py`** — CheckoutPage (fill_information, click_finish/cancel/continue)

### components
- **`pages/components/base_component.py`** — Component (_root Locator, locator(Element) → scoped Locator)
- **`pages/components/product_card.py`** — ProductCard (add_to_cart, remove_from_cart)
- **`pages/components/cart_line_item.py`** — CartLineItem (get_name)

### utilities
- **`utils/element.py`** — Element (selector + name), `resolve_locator(page, Element|Locator) → Locator`
- **`utils/markers.py`** — smoke, regression, critical decorators
- **`utils/logger/`** — loguru wrapper (get_logger, PageLogger)
- **`utils/allure/step.py`** — CheckStep decorator (Allure step grouping)

### data
- **`data/users.yaml`** — valid_user, invalid credentials, checkout info
- **`data/products.yaml`** — products list with names
- **`features/*.feature`** — Gherkin feature files

## 4. How Gherkin Works

1. `.feature` file → `parse_feature_file()` → list of GherkinStep
2. `@Gherkin("file.feature", "Scenario name")` decorates test:
   - **Collection:** finds scenario by name, raises `ValueError` if not found
   - **Run:** binds steps to `Steps` instance
   - **After:** `verify_complete()` — all steps executed?
3. `steps.given/when/then(description)` — context manager:
   - Verifies text and type 1-to-1 against `.feature`
   - Creates Allure step + log
4. `steps.step()` — **container** for when/then pair (one Allure step, not verified against `.feature`)
5. `checker.*` accepts `Element | Locator`:
   - `Element` → resolved via `page.locator(selector)` (page-level)
   - `Locator` → passed through unchanged (scoped)
6. Scenario Outline + Examples → auto-parametrized via `pytest.mark.parametrize`

## 5. How to Write a New Test

```python
@smoke
@Gherkin("feature.feature", "Scenario name")
def test_something(
    login_page: LoginPage,
    products_page: ProductsPage,
    cart_page: CartPage,
    steps: Steps,
    checker: UIChecker,
    users_data: dict,
    products_data: dict,
) -> None:
    user = users_data["valid_user"]

    with steps.given("User is on login page"):
        login_page.navigate("/")

    with steps.step():
        with steps.when("User logs in"):
            login_page.login(user["username"], user["password"])
        with steps.then("User sees products"):
            checker.common.check_presence(
                products_page.PRODUCT_CONTAINER,
                ElementDTO(is_visible=True),
            )
```

## 6. Patterns

### ✅ Correct Patterns

**1. Component.scoped_locator() for assertions**
```python
line_item = cart_page.cart_line_item()
checker.text.check(line_item.locator(line_item.ITEM_NAME), dto)
```
`Component.locator(Element)` returns a `Locator` scoped to `_root`. Checker accepts `Locator` and passes it through.

**2. @Gherkin + Steps for strict verification**
```python
@Gherkin("file.feature", "Scenario")
def test_something(steps: Steps, checker: UIChecker):
    with steps.given("..."):
        ...
    with steps.step():
        with steps.when("..."):
            ...
        with steps.then("..."):
            checker.common.check_presence(...)
```
Each step verified 1-to-1 against `.feature`. Mismatch → `AssertionError`.

**3. Test data via fixtures**
```python
user = users_data["valid_user"]
product = products_data["products"][0]["name"]
```
All tests use YAML fixtures. No hardcoded strings.

**4. resolve_locator for Element | Locator**
```python
# Checker accepts both. Locator returned as-is (preserves scoping).
# Element resolved via page.locator(selector).
```

**5. Page fixture isolation**
```python
# Each test: new context → new_page()
```

**6. Element as stateless selector**
```python
USERNAME_INPUT = Element("#user-name")  # stateless, shared across instances
```

**7. __init_subclass__ for auto-name**
```python
class BasePage:
    def __init_subclass__(cls, **kwargs):
        for attr_name, value in cls.__dict__.items():
            if isinstance(value, Element) and not value._name:
                value._name = attr_name
```

**8. Settings via pydantic-settings**
```python
class Settings(BaseSettings):
    base_url: str = "https://www.saucedemo.com"
    model_config = {"env_file": ".env"}
```

**9. Checker via fixture**
```python
@pytest.fixture
def checker(page: Page) -> UIChecker:
    return UIChecker(page)
```

**10. Steps fixture per test**
```python
@pytest.fixture
def steps() -> Steps:
    return Steps()
```
Each test gets a fresh `Steps` instance. Pointer resets between tests.

### ❌ Anti-Patterns

**1. Element without component + checker on full page**
```python
# ❌ checker.text.check(cart_page.cart_line_item().ITEM_NAME, dto)
# ✅ line_item.locator(line_item.ITEM_NAME)
```
If multiple elements match the selector on the page — ambiguous. Always use `component.locator(Element)`.

**2. is_visible=True + is_hidden=True (no-op)**
```python
# ❌ ElementDTO(is_visible=True, is_hidden=True)
# ✅ ElementDTO(is_visible=False, is_hidden=True)
```
Both flags cancel each other out in `check_presence`. Use `is_visible=False` for hidden checks.

**3. Hardcoded credentials**
```python
# ❌ login_page.login("standard_user", "secret_sauce")
# ✅ login_page.login(user["username"], user["password"])
```

**4. locator.count without call**
```python
# ❌ count = locator.count  # always truthy (method reference)
# ✅ count = locator.count()
```

**5. String interpolation in CSS selectors**
```python
# ❌ f".inventory_item:has-text('{product_name}')"
# ✅ self.page.locator(".inventory_item").filter(has_text=product_name)
```
Unescaped dynamic values break CSS. Use Playwright's `Locator.filter()`.

**6. Shared mutable state on class level**
```python
# ❌ class Element: page: Page (mutable class attribute)
# ✅ Element is stateless; resolve_locator(page, element)
```

**7. @Gherkin without steps fixture**
```python
# ❌ @Gherkin("file", "scenario") def test_something(login_page):
# ✅ def test_something(login_page, steps, checker):
```
`@Gherkin` requires `steps: Steps` in the function signature.

## 7. CI/CD

**Pipeline:**
```
push/pull_request → lint (ruff + mypy + bandit) → test (pytest + xdist) → allure-report → pages-deployment
```

**Workflows:**
- **`test.yml`** — lint → test → allure-report (triggered on push/pull_request/manual)
- **`check-unimplemented.yml`** — nightly cron (scenario coverage report)
- **`workflow_dispatch`** — manual run with inputs (browser, test_filter)

**Inputs:**
- `test_filter` — pytest filter (`-m smoke`, `tests/login/`, `-k test_login`)
- `browser` — chromium | firefox | webkit | all

## 8. Run Locally

```bash
# Install
poetry install

# Run all tests
poetry run pytest

# Run with filter
poetry run pytest -m smoke
poetry run pytest tests/login/
poetry run pytest -v -k test_login

# Allure report
poetry run pytest --alluredir=allure-results
allure serve allure-results

# Linting
poetry run ruff check .
poetry run mypy .
poetry run bandit -r -ll --exclude tests/ .
```

## 9. Planned Tasks

1. **🔲 Flaky test detection** — Allure-based analysis of pass/fail patterns across runs
2. **🔲 Multi-environment support** — staging/prod switching via config
3. **🔲 pytest-reruns for flaky tests** — automatic retry with configurable limits
4. **🔲 Assertion coverage check** — script verifying every @Gherkin test contains at least one assert
5. **🔲 Expected failures** — mark tests as "known issue" with Jira ticket link; tracked separately, doesn't break CI
6. **🔲 Expanded test coverage** — image checks, API testing, font verification, accessibility checks
7. **🔲 Performance tracking** — duration metrics per test; alert on regression
8. **🔲 Test summary report** — PNG pie chart of results (passed/failed/broken/expected_failed) + duration; extensible notification adapter (Slack/Telegram webhook); sent after every CI run
