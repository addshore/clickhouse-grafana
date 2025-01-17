from testflows.core import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By as SelectBy


class Locators:
    # Locators for panel page

    @property
    def fill(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[id*='option-0-radiogroup']")

    @property
    def actual(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[id*='option-2-radiogroup']")

    @property
    def visualization(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[data-testid='data-testid panel content']")

    @property
    def select_datasource_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[data-testid='data-testid Select a data source']")

    def select_datasource(self, datasource_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f"//div[@data-testid='data-source-card' and .//text()='{datasource_name}']")

    def sql_editor_toggle(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f"//*[contains(@data-rbd-draggable-id, '{query_name}')]//*[contains(@id, 'option-sql')]")

    def sql_editor_input(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f"//*[contains(@data-rbd-draggable-id, '{query_name}')]//*[@class='view-lines monaco-mouse-cursor-text']")

    def input_in_sql_editor(self, query_name='A'):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f"//*[contains(@data-rbd-draggable-id, '{query_name}')]//*[@class='inputarea monaco-mouse-cursor-text']")

    @property
    def panel_title_textfield(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[id='PanelFrameTitle']")
    
    @property
    def repeat_by_variable_dropdown(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[id='repeat-by-variable-select']")

    @property
    def panel_error(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[data-testid='data-testid Panel status error']")

    @property
    def panel_error_for_table_view(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[aria-label='Panel header error']")

    @property
    def query_inspector_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[aria-label='Query inspector button']")

    @property
    def query_inspector_refresh_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[aria-label='Panel inspector Query refresh button']")

    @property
    def query_inspector_url(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, "//*[(@class='json-formatter-string' and "
                                                   "contains(text(), 'api')) or "
                                                   "(@class='json-formatter-string json-formatter-url' and "
                                                   "contains(text(), 'http'))]")

    @property
    def add_query_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[data-testid='data-testid query-tab-add-query']")

    @property
    def expression_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, "[data-testid='query-tab-add-expression']")

    def query_name_field(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{query_name}")]//button[@data-testid="query-name-div"]')

    def query_name_textfield(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{query_name}")]//button[@data-testid="query-name-div"]//input')

    def duplicate_query_button(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{query_name}")]//button[@data-testid="data-testid Duplicate query"]')

    def hide_response_query_button(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{query_name}")]//button[@data-testid="data-testid Hide response"]')

    def delete_query_button(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{query_name}")]//button[@data-testid="data-testid Remove query"]')

    def expression_name_field(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//button[@data-testid="query-name-div"]')

    def expression_name_textfield(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//button[@data-testid="query-name-div"]//input')

    def expression_query_button(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//button[@data-testid="data-testid Duplicate query"]')

    def hide_response_expression_button(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//button[@data-testid="data-testid Hide response"]')

    def delete_expression_button(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//button[@data-testid="data-testid Remove query"]')

    def expression_operation_dropdown(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH,
                                   f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//div[contains(@class, "grafana-select-value-container")]')

    def expression_textfield(self, expression_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH,
                                   f'//*[contains(@data-rbd-draggable-id, "{expression_name}")]//div[contains(@class, "grafana-select-value-container")]')

    @property
    def time_picker_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[data-testid="data-testid TimePicker Open Button"]')

    @property
    def time_picker_from_textfield(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[data-testid="data-testid Time Range from field"]')

    @property
    def time_picker_to_textfield(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[data-testid="data-testid Time Range to field"]')

    @property
    def time_picker_submit_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[data-testid="data-testid TimePicker submit button"]')

    def data_source_picker(self, query_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[contains(@data-rbd-draggable-id, "{query_name}")]//input[@data-testid="data-testid Select a data source"]')

    @property
    def apply_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[data-testid="data-testid Apply changes and go back to dashboard"]')

    @property
    def discard_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[title="Undo all changes"]')

    @property
    def run_query_button(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//div[contains(@id, "A")]//button')

    @property
    def data_is_missing_text(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[text()="Data is missing a time field"]')

    @property
    def no_data_text(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[text()="No data"]')

    @property
    def table_view_toggle(self):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.CSS_SELECTOR, f'[for="table-view"]')

    def table_column_name(self, column_name):
        driver: WebDriver = current().context.driver
        return driver.find_element(SelectBy.XPATH, f'//*[text()="{column_name}"]')


locators = Locators()
