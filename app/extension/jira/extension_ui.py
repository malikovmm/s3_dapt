import os

from selenium.webdriver.common.by import By
from PIL import Image
from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import ProjectFolderPage, PopupManager
from util.conf import JIRA_SETTINGS

def project_page_load(webdriver, datasets):
    page = ProjectFolderPage(webdriver, datasets['project_key'])
    @print_timing("selenium_s3_project_page_load")
    def measure():
        page.go_to()
        page.wait_for_page_loaded()
    measure()
    PopupManager(webdriver).dismiss_default_popup()

def project_page_create_folder(webdriver, datasets):
    page = ProjectFolderPage(webdriver, datasets['project_key'])

    @print_timing("project_page_create_folder")
    def measure():
        PopupManager(webdriver).dismiss_default_popup()

        @print_timing('project_page_create_folder:load_page')
        def sub_measure():
            page.go_to()
            page.wait_for_page_loaded()

        sub_measure()

        @print_timing('project_page_create_folder:folder_creating')
        def sub_measure():
            page.create_folder()

        sub_measure()
    measure()
    PopupManager(webdriver).dismiss_default_popup()


def project_page_upload(webdriver, datasets):
    page = ProjectFolderPage(webdriver, datasets['project_key'])
    temp_file = Image.new(mode='RGB', size=(64, 64), color='red')
    temp_file_path = os.path.join(os.getcwd(), BasePage.generate_random_string(10) + '.jpg')
    temp_file.save(temp_file_path)

    @print_timing("project_page_upload")
    def measure():
        PopupManager(webdriver).dismiss_default_popup()

        @print_timing('project_page_upload:load_page')
        def sub_measure():
            page.go_to()
            page.wait_for_page_loaded()

        sub_measure()

        @print_timing('project_page_upload:uploading')
        def sub_measure():
            page.upload_file(temp_file_path)

        sub_measure()
    measure()
    os.remove(temp_file_path)
    PopupManager(webdriver).dismiss_default_popup()


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()

