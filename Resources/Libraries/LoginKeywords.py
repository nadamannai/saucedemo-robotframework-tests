from robot.api.deco import keyword
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from robot.libraries.BuiltIn import BuiltIn
import json
import os

class LoginKeywords:
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self.builtin = BuiltIn()
        self.selectors = self._load_selectors()
        self.config = self._load_config()
    
    def _load_selectors(self):
        """Charge les sélecteurs depuis le fichier JSON"""
        selectors_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'Variables', 'selectors.json'
        )
        with open(selectors_path, 'r') as f:
            return json.load(f)
    
    def _load_config(self):
        """Charge la configuration depuis le fichier JSON"""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'Variables', 'config.json'
        )
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _get_browser_library(self):
        """Récupère l'instance de BrowserKeywords pour accéder au driver"""
        return self.builtin.get_library_instance('Lib1')

    @keyword("Login With Standard User")
    def login_with_standard_user(self):
        """Se connecte avec l'utilisateur standard"""
        credentials = self.config['credentials']['standard_user']
        self._login(credentials['username'], credentials['password'])
        print("✓ Connecté avec l'utilisateur standard")

    @keyword("Login With Problem User")
    def login_with_problem_user(self):
        """Se connecte avec l'utilisateur problem"""
        credentials = self.config['credentials']['problem_user']
        self._login(credentials['username'], credentials['password'])
        print("✓ Connecté avec l'utilisateur problem")

    @keyword("Login With User")
    def login_with_user(self, username, password):
        """Se connecte avec les identifiants spécifiés"""
        self._login(username, password)
        print(f"✓ Connecté avec l'utilisateur: {username}")


    def _login(self, username, password):
        """Méthode privée pour gérer la connexion"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Attendre et remplir le champ username
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, self.selectors['login_page']['username_field']))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        # Remplir le champ password
        password_field = driver.find_element(By.ID, self.selectors['login_page']['password_field'])
        password_field.clear()
        password_field.send_keys(password)
        
        # Cliquer sur le bouton login
        driver.find_element(By.ID, self.selectors['login_page']['login_button']).click()
        
        # Attendre que la page inventory soit chargée
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, self.selectors['inventory_page']['inventory_list']))
        )

    @keyword("Verify Login Page Is Displayed")
    def verify_login_page_is_displayed(self):
        """Vérifie que la page de login est affichée"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Vérifier la présence des champs de login
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, self.selectors['login_page']['username_field']))
        )
        assert username_field.is_displayed(), "Champ username non visible"
        
        password_field = driver.find_element(By.ID, self.selectors['login_page']['password_field'])
        assert password_field.is_displayed(), "Champ password non visible"
        
        login_button = driver.find_element(By.ID, self.selectors['login_page']['login_button'])
        assert login_button.is_displayed(), "Bouton login non visible"
        
        print("✓ Page de login affichée correctement")

    @keyword("Verify Login Error Message")
    def verify_login_error_message(self, expected_message):
        """Vérifie le message d'erreur de connexion"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Attendre et récupérer le message d'erreur
        error_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        
        actual_message = error_element.text
        assert expected_message in actual_message, \
            f"Message d'erreur incorrect. Attendu: '{expected_message}', Obtenu: '{actual_message}'"
        
        print(f"✓ Message d'erreur correct: {actual_message}")

    @keyword("Get Error Message")
    def get_error_message(self):
        """Récupère le message d'erreur affiché"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            return error_element.text
        except NoSuchElementException:
            return None