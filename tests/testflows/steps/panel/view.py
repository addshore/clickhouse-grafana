from testflows.core import *
from testflows.asserts import error

from steps.delay import delay
from steps.panel.locators import locators
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By as SelectBy

import steps.ui as ui


@TestStep(When)
def wait_fill_actual_toggle(self):
    """Wait Fill/Actual toggle to be clickable."""

    ui.wait_for_element_to_be_clickable(
        select_type=SelectBy.CSS_SELECTOR, element="[data-testid='data-testid radio-button']"
    )


@TestStep(When)
def click_fill_toggle(self):
    """Click Fill toggle."""

    locators.fill.click()


@TestStep(When)
def click_actual_toggle(self):
    """Click Actual toggle."""

    locators.actual.click()


@TestStep(When)
def click_select_datasource_button(self):
    """Click select datasource button."""

    locators.select_datasource_button.click()


@TestStep(When)
def click_datasource_in_select_datasource_dropdown(self, datasource_name):
    """Click select datasource button."""

    locators.select_datasource(datasource_name=datasource_name).click()


@TestStep(When)
def click_sql_editor_toggle(self, query_name):
    """Click SQL editor toggle."""
    locators.sql_editor_toggle(query_name).click()


@TestStep(When)
def wait_sql_editor_toggle(self):
    """Wait SQL editor toggle to be loaded."""

    ui.wait_for_element_to_be_present(
        select_type=SelectBy.CSS_SELECTOR, element=f"[id*='option-sql']"
    )


@TestStep(When)
def select_first_query_row(self):
    """Select first query row in SQL editor."""
    locators.row_in_sql_editor.click()


@TestStep(When)
def click_on_the_visualization(self):
    """Click on the visualization."""
    locators.visualization.click()


@TestStep(When)
def click_add_query_button(self):
    """Click Add query button."""
    locators.add_query_button.click()


@TestStep(When)
def click_expression_button(self):
    """Click Expression button."""
    locators.expression_button.click()


@TestStep(When)
def go_to_sql_editor(self, query_name='A'):
    """Wait sql editor toggle and click it."""
    with By("waiting sql editor toggle"):
        wait_sql_editor_toggle()

    with By("clicking SQL Editor toggle"):
        click_sql_editor_toggle(query_name=query_name)


@TestStep(When)
def wait_sql_editor_input(self):
    """Wait SQL editor input field."""
    ui.wait_for_element_to_be_present(
        select_type=SelectBy.CSS_SELECTOR, element=f"[class='view-lines monaco-mouse-cursor-text']"
    )


@TestStep(When)
def select_input_query(self, query_name):
    """Select input query using triple click on textarea."""

    ActionChains(self.context.driver).double_click(locators.sql_editor_input(query_name=query_name)).click(locators.sql_editor_input(query_name=query_name)).perform()


@TestStep(When)
def clear_panel_title(self):
    """Clear panel title."""
    locators.panel_title_textfield.clear()


@TestStep(When)
def enter_panel_title(self, panel_title):
    """Enter panel title."""
    locators.panel_title_textfield.send_keys(panel_title)


@TestStep(When)
def change_panel_title(self, panel_title):
    """Change panel title"""
    with By("clearing panel title"):
        clear_panel_title()

    with And("entering new panel title"):
        enter_panel_title(panel_title=panel_title)


@TestStep(When)
def change_repeat_by_variable_option(self, variable_name):
    """Change repeat by variable option."""

    locators.repeat_by_variable_dropdown.send_keys(variable_name)


@TestStep(When)
def enter_sql_editor_input(self, query, query_name='A'):
    """Enter SQL request into sql editor input field."""

    with By("waiting SQL editor"):
        wait_sql_editor_input()

    with By("selecting input string"):
        select_input_query(query_name=query_name)

    with By("entering request"):
        locators.input_in_sql_editor(query_name=query_name).send_keys(query)


@TestStep(When)
def get_input_query(self, query_name='A'):
    """Get SQL query."""

    return locators.input_in_sql_editor(query_name=query_name).text


@TestStep(When)
def actual(self):
    """Wait Fill/Actual toggle and click actual."""

    with By("waiting actual toggle"):
        wait_fill_actual_toggle()

    with By("clicking actual toggle"):
        click_actual_toggle()


@TestStep(When)
def fill(self):
    """Wait Fill/Actual toggle and click fill."""

    with By("waiting fill toggle"):
        wait_fill_actual_toggle()

    with By("clicking fill toggle"):
        click_fill_toggle()


@TestStep(When)
def wait_visualization(self):
    """Wait visualization to be loaded."""

    ui.wait_for_element_to_be_visible(
        select_type=SelectBy.CSS_SELECTOR, element=f"[data-testid='data-testid panel content']"
    )


@TestStep(When)
def take_visualization_screenshot(self, screenshot_name):
    """Take screenshot for visualization."""

    locators.visualization.screenshot(f'./screenshots/{screenshot_name}.png')


@TestStep(Then)
def take_screenshot_for_visualization(self, screenshot_name):
    with Then(f"I wait visualization to be loaded"):
        wait_visualization()

    with Then("I take screenshot"):
        take_visualization_screenshot(screenshot_name=screenshot_name)


@TestStep(When)
def double_click_on_visualization(self):
    """Double-click on visualization to change time range"""

    ActionChains(self.context.driver).double_click(locators.visualization).click(locators.visualization).perform()


@TestStep(When)
def wait_datasource_in_datasource_dropdown(self, datasource_name):
    """Wait panel menu button for panel."""

    ui.wait_for_element_to_be_clickable(
        select_type=SelectBy.XPATH, element=f"//div[@data-testid='data-source-card' and .//text()='{datasource_name}']"
    )


@TestStep(When)
def select_datasource_in_panel_view(self, datasource_name):
    """Select datasource in datasource dropdown."""
    with By("clicking datasource dropdown"):
        click_select_datasource_button()
    with By("waiting datasource in datasource dropdown"):
        wait_datasource_in_datasource_dropdown(datasource_name=datasource_name)
    with delay():
        with By("selecting datasource in dropdown"):
            click_datasource_in_select_datasource_dropdown(datasource_name=datasource_name)


@TestStep(Then)
def check_panel_error_exists(self):
    """Check panel error exists."""
    with By("checking error"):
        try:
            ui.wait_for_element_to_be_visible(
                select_type=SelectBy.CSS_SELECTOR,
                element="[data-testid='data-testid Panel status error']"
            )
            return True
        except:
            return False


@TestStep(When)
def click_inspect_query_button(self):
    """Click inspect query button."""

    locators.query_inspector_button.click()


@TestStep(When)
def click_inspect_query_refresh_button(self):
    """Click inspect query button."""

    locators.query_inspector_refresh_button.click()


@TestStep(When)
def get_query_inspector_url_text(self):
    """Get url text from query inspector."""

    with By("getting url from query inspector"):
        return locators.query_inspector_url.text


@TestStep(Then)
def check_query_inspector_request(self, url_parts):
    """Check url in query inspector."""

    with By("opening query inspector"):
        with delay():
            click_inspect_query_button()

    with By("clicking refresh button in query inspector"):
        with delay():
            click_inspect_query_refresh_button()

    with By("checking url contains necessary parts"):
        for url_part in url_parts:
            with By(f"checking url contains {url_part}"):
                assert url_part in get_query_inspector_url_text(), error()


@TestStep(When)
def change_query_name(self, query_name, new_query_name):
    """Change query name."""

    locators.query_name_field(query_name=query_name).click()
    locators.query_name_textfield(query_name=query_name).send_keys(new_query_name)
    locators.query_name_textfield(query_name=query_name).send_keys(Keys.ENTER)


@TestStep(When)
def change_expression_name(self, expression_name, new_expression_name):
    """Change expression name."""

    locators.expression_name_field(expression_name=expression_name).click()
    locators.expression_name_textfield(expression_name=expression_name).send_keys(new_expression_name)
    locators.expression_name_textfield(expression_name=expression_name).send_keys(Keys.ENTER)


@TestStep(When)
def click_duplicate_query(self, query_name):
    """Click duplicate query."""

    locators.duplicate_query_button(query_name=query_name).click()


@TestStep(When)
def click_duplicate_expression(self, expression_name):
    """Click duplicate expression."""

    locators.duplicate_expression_button(expression_name=expression_name).click()


@TestStep(When)
def click_hide_response_query(self, query_name):
    """Click hide response query button."""

    locators.hide_response_query_button(query_name=query_name).click()


@TestStep(When)
def click_hide_response_expression(self, expression_name):
    """Click hide response expression button."""

    locators.hide_response_expression_button(expression_name=expression_name).click()


@TestStep(When)
def click_delete_query(self, query_name):
    """Click delete query button."""

    locators.delete_query_button(query_name=query_name).click()


@TestStep(When)
def click_hide_response_expression(self, expression_name):
    """Click delete expression button."""

    locators.delete_expression_button(expression_name=expression_name).click()


@TestStep(When)
def enter_expression_operation(self, expression_name, operation_type):
    """Enter expression operation type."""

    locators.expression_operation_dropdown(expression_name=expression_name).send_keys(operation_type)
    locators.expression_operation_dropdown(expression_name=expression_name).send_keys(Keys.ENTER)


@TestStep(When)
def enter_expression(self, expression_name, expression):
    """Enter expression."""

    locators.expression_textfield(expression_name=expression_name).send_keys(expression)
    locators.expression_textfield(expression_name=expression_name).send_keys(Keys.ENTER)


@TestStep(When)
def enter_time(self, time_from, time_to):
    """Enter time."""

    with When("I open time modal"):
        with delay():
            locators.time_picker_button.click()

    with When("I enter time from"):
        with delay():
            locators.time_picker_from_textfield.clear()
            locators.time_picker_from_textfield.send_keys(time_from)

    with When("I enter time to"):
        with delay():
            locators.time_picker_to_textfield.clear()
            locators.time_picker_to_textfield.send_keys(time_to)

    with When("I click submit button"):
        with delay():
            locators.time_picker_submit_button.click()


@TestStep(When)
def enter_data_source_for_query(self, query_name, datasource_name):
    """Enter data source for query."""

    locators.data_source_picker(query_name=query_name).send_keys(datasource_name)
    locators.data_source_picker(query_name=query_name).send_keys(Keys.ENTER)


@TestStep(When)
def click_apply_button(self):
    """Click apply button for panel."""

    locators.apply_button.click()


@TestStep(When)
def click_discard_button(self):
    """Click apply button for panel."""

    locators.discard_button.click()


@TestStep(When)
def click_run_query_button(self):
    """Click Run Query button."""

    locators.run_query_button.click()


@TestStep(When)
def click_table_view_toggle(self):
    """Click table view toggle."""

    locators.table_view_toggle.click()


@TestStep(Then)
def check_data_is_missing_text(self):
    """Check that 'Data is missing a time field' text is displayed."""
    with By("checking 'Data is missing a time field' text is displayed"):
        try:
            ui.wait_for_element_to_be_visible(
                select_type=SelectBy.XPATH,
                element='//*[text()="Data is missing a time field"]'
            )
            return True
        except:
            return False


@TestStep(Then)
def check_columns_in_table_view(self, columns):
    """Check that columns in table view is displayed."""
    with By(f"checking {','.join(columns)} columns is displayed"):
        try:
            for column_name in columns:
                ui.wait_for_element_to_be_visible(
                    select_type=SelectBy.XPATH,
                    element=f'//*[text()="{column_name}"]'
                )
            return True
        except:
            return False


@TestStep(Then)
def check_no_data_text(self):
    """Check that columns in table view is displayed."""
    with By(f"checking 'No data' text is displayed"):
        try:
            ui.wait_for_element_to_be_visible(
                select_type=SelectBy.XPATH,
                element=f'//*[text()="No data"]'
            )
            return True
        except:
            return False


@TestStep(Then)
def check_error_for_table_view(self):
    """Check that columns in table view is displayed."""
    with By(f"checking 'No data' text is displayed"):
        try:
            ui.wait_for_element_to_be_visible(
                select_type=SelectBy.XPATH,
                element=f'//*[text()="No data"]'
            )
            return True
        except:
            return False

