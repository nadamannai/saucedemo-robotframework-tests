from robot.api.deco import keyword
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from robot.libraries.BuiltIn import BuiltIn
import json
import os
import time

class BurgerMenuKeywords:
    
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

    @keyword("Close Burger Menu")
    def close_burger_menu(self):
        """Ferme le menu burger s'il est ouvert"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        
        try:
            # Vérifier si le menu est ouvert en vérifiant la classe du wrapper
            menu_wrapper = driver.find_element(By.ID, self.selectors['burger_menu']['menu_button'])
            parent = driver.execute_script("return arguments[0].parentElement;", menu_wrapper)
            classes = parent.get_attribute("class")
            
            # Si le menu est ouvert, le fermer
            if "bm-burger-button-open" in classes or driver.find_elements(By.CSS_SELECTOR, ".bm-menu-wrap[aria-hidden='false']"):
                print("Menu déjà ouvert, fermeture...")
                close_button = driver.find_element(By.ID, self.selectors['burger_menu']['close_button'])
                close_button.click()
                time.sleep(0.5)
                print("✓ Menu burger fermé")
        except (NoSuchElementException, TimeoutException):
            print("Menu burger déjà fermé ou bouton non trouvé")

    @keyword("Open Burger Menu")
    def open_burger_menu(self):
        """Ouvre le menu burger"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        
        print(f"Tentative d'ouverture du menu burger...")
        print(f"URL actuelle: {driver.current_url}")
        
        # Fermer le menu s'il est déjà ouvert
        self.close_burger_menu()
        
        try:
            # Attendre que le bouton soit présent
            wait = WebDriverWait(driver, self.config['timeouts']['default'])
            menu_button = wait.until(
                EC.presence_of_element_located((By.ID, self.selectors['burger_menu']['menu_button']))
            )
            print(f"✓ Bouton menu burger trouvé")
            
            # Attendre qu'il soit visible
            wait.until(EC.visibility_of(menu_button))
            print(f"✓ Bouton menu burger visible")
            
            # Scroll vers le bouton
            driver.execute_script("arguments[0].scrollIntoView(true);", menu_button)
            time.sleep(0.3)
            
            # Essayer de cliquer avec JavaScript directement
            print("Clic sur le bouton menu burger...")
            driver.execute_script("arguments[0].click();", menu_button)
            time.sleep(0.5)
            
            # Attendre que le menu soit visible
            menu = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, self.selectors['burger_menu']['menu_container']))
            )
            print("✓ Menu burger ouvert avec succès")
            
        except TimeoutException as e:
            print(f"ERREUR TimeoutException: {str(e)}")
            print(f"Sélecteur utilisé: {self.selectors['burger_menu']['menu_button']}")
            # Prendre une capture d'écran pour debug
            driver.save_screenshot("debug_burger_menu_timeout.png")
            print("Screenshot sauvegardé: debug_burger_menu_timeout.png")
            raise
        except Exception as e:
            print(f"ERREUR inattendue: {str(e)}")
            driver.save_screenshot("debug_burger_menu_error.png")
            print("Screenshot sauvegardé: debug_burger_menu_error.png")
            raise

    @keyword("Verify Burger Menu Is Open")
    def verify_burger_menu_is_open(self):
        """Vérifie que le menu burger est ouvert"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        menu = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.selectors['burger_menu']['menu_container']))
        )
        assert menu.is_displayed(), "Le menu burger n'est pas ouvert"
        print("✓ Menu burger est bien ouvert")

    @keyword("Verify Burger Menu Options")
    def verify_burger_menu_options(self):
        """Vérifie que toutes les options du menu burger sont présentes"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        options = {
            "All Items": self.selectors['burger_menu']['all_items_link'],
            "About": self.selectors['burger_menu']['about_link'],
            "Logout": self.selectors['burger_menu']['logout_link'],
            "Reset App State": self.selectors['burger_menu']['reset_link']
        }
        
        for name, element_id in options.items():
            element = wait.until(
                EC.visibility_of_element_located((By.ID, element_id)),
                message=f"{name} n'est pas visible après l'attente"
            )
            assert element.is_displayed(), f"{name} n'est pas visible"
            print(f"✓ Option '{name}' vérifiée")

    @keyword("Add Product To Cart")
    def add_product_to_cart(self, product_name="Sauce Labs Backpack"):
        """
        Ajoute un produit au panier
        Args:
            product_name: Nom du produit à ajouter (par défaut: Sauce Labs Backpack)
        """
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Fermer le menu burger si ouvert
        self.close_burger_menu()
        
        try:
            # Trouver le bouton "Add to cart" pour le produit spécifié
            # Le bouton a un attribut data-test qui contient le nom du produit en lowercase et avec des tirets
            product_id = product_name.lower().replace(" ", "-")
            add_button_selector = f"button[data-test='add-to-cart-{product_id}']"
            
            print(f"Recherche du produit: {product_name}")
            print(f"Sélecteur: {add_button_selector}")
            
            add_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, add_button_selector))
            )
            
            # Scroll vers le bouton
            driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(0.3)
            
            # Cliquer sur le bouton
            driver.execute_script("arguments[0].click();", add_button)
            time.sleep(0.5)
            
            print(f"✓ Produit '{product_name}' ajouté au panier")
            
        except TimeoutException:
            print(f"ERREUR: Impossible de trouver le bouton pour '{product_name}'")
            driver.save_screenshot("debug_add_product_error.png")
            raise Exception(f"Le produit '{product_name}' n'a pas pu être ajouté au panier")
    
    @keyword("Verify Cart Badge Count")
    def verify_cart_badge_count(self, expected_count):
        """
        Vérifie que le badge du panier affiche le nombre attendu d'articles
        Args:
            expected_count: Nombre d'articles attendus (str ou int)
        """
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Fermer le menu burger si ouvert
        self.close_burger_menu()
        
        try:
            badge = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, self.selectors['inventory_page']['cart_badge']))
            )
            actual_count = badge.text
            
            assert actual_count == str(expected_count), \
                f"Le badge affiche '{actual_count}' au lieu de '{expected_count}'"
            
            print(f"✓ Badge du panier affiche bien {expected_count} article(s)")
            
        except TimeoutException:
            raise AssertionError(f"Le badge du panier n'est pas visible (attendu: {expected_count})")

    @keyword("Verify Product Button State")
    def verify_product_button_state(self, product_name, expected_state):
        """
        Vérifie l'état du bouton d'un produit (Add to cart ou Remove)
        Args:
            product_name: Nom du produit à vérifier
            expected_state: État attendu ('add' ou 'remove')
        """
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Fermer le menu burger si ouvert
        self.close_burger_menu()
        
        product_id = product_name.lower().replace(" ", "-")
        
        if expected_state.lower() == 'add':
            # Vérifier que le bouton "Add to cart" est présent
            add_button_selector = f"button[data-test='add-to-cart-{product_id}']"
            try:
                add_button = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, add_button_selector))
                )
                button_text = add_button.text.strip().upper()
                assert "ADD TO CART" in button_text, \
                    f"Le texte du bouton est '{button_text}' au lieu de 'ADD TO CART'"
                print(f"✓ Le bouton 'Add to cart' est présent pour '{product_name}'")
            except TimeoutException:
                driver.save_screenshot("debug_add_button_missing.png")
                raise AssertionError(f"Le bouton 'Add to cart' est introuvable pour '{product_name}'")
                
        elif expected_state.lower() == 'remove':
            # Vérifier que le bouton "Remove" est présent
            remove_button_selector = f"button[data-test='remove-{product_id}']"
            try:
                remove_button = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, remove_button_selector))
                )
                button_text = remove_button.text.strip().upper()
                assert "REMOVE" in button_text, \
                    f"Le texte du bouton est '{button_text}' au lieu de 'REMOVE'"
                print(f"✓ Le bouton 'Remove' est présent pour '{product_name}'")
            except TimeoutException:
                driver.save_screenshot("debug_remove_button_missing.png")
                raise AssertionError(f"Le bouton 'Remove' est introuvable pour '{product_name}'")
        else:
            raise ValueError(f"État invalide: '{expected_state}'. Utilisez 'add' ou 'remove'")

    @keyword("Click All Items")
    def click_all_items(self):
        """Clique sur l'option 'All Items' du menu"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Sauvegarder l'URL actuelle
        current_url = driver.current_url
        
        # Attendre et cliquer sur All Items
        all_items_link = wait.until(
            EC.element_to_be_clickable((By.ID, self.selectors['burger_menu']['all_items_link']))
        )
        driver.execute_script("arguments[0].click();", all_items_link)
        time.sleep(0.5)
        print("✓ Cliqué sur 'All Items'")
        
        return current_url

    @keyword("Verify Same Page")
    def verify_same_page(self, expected_url):
        """Vérifie qu'on est resté sur la même page"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        current_url = driver.current_url
        assert current_url == expected_url, \
            f"L'URL a changé : attendu '{expected_url}', obtenu '{current_url}'"
        print(f"✓ Resté sur la même page : {current_url}")

    @keyword("Click About")
    def click_about(self):
        """Clique sur l'option 'About' du menu"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Attendre et cliquer sur About
        about_link = wait.until(
            EC.element_to_be_clickable((By.ID, self.selectors['burger_menu']['about_link']))
        )
        driver.execute_script("arguments[0].click();", about_link)
        print("✓ Cliqué sur 'About'")

    @keyword("Verify Saucelabs Page Opened")
    def verify_saucelabs_page_opened(self):
        """Vérifie que la page Saucelabs s'est ouverte"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['long'])
    
        # Attendre que l'URL change et contienne saucelabs
        wait.until(lambda d: "saucelabs.com" in d.current_url.lower())
    
        current_url = driver.current_url
    
        # Extraire le domaine et le chemin de l'URL
        from urllib.parse import urlparse
        parsed_url = urlparse(current_url)
        domain = parsed_url.netloc.lower()
        path = parsed_url.path.strip('/')
    
        # Vérifier que le domaine est saucelabs.com et qu'il n'y a pas de chemin (ou juste /)
        valid_domains = ["saucelabs.com", "www.saucelabs.com"]
        is_valid_domain = domain in valid_domains
        is_root_path = path == ""
    
        assert is_valid_domain and is_root_path, \
            f"Page Saucelabs non ouverte correctement. URL actuelle : {current_url} (domaine: {domain}, chemin: /{path})"
    
        print(f"✓ Page Saucelabs ouverte : {current_url}")

    @keyword("Return To Inventory Page")
    def return_to_inventory_page(self):
        """Retourne à la page inventory depuis n'importe quelle page"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        current_url = driver.current_url
        print(f"URL actuelle avant retour: {current_url}")
        
        # Vérifier le nombre de fenêtres
        window_count = len(driver.window_handles)
        print(f"Nombre de fenêtres ouvertes: {window_count}")
        
        if window_count > 1:
            # Si plusieurs fenêtres, revenir à la première (principale)
            print("Fermeture de la fenêtre actuelle et retour à la fenêtre principale...")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        
        # Vérifier l'URL actuelle
        current_url = driver.current_url
        print(f"URL après switch: {current_url}")
        
        # Si on n'est pas sur inventory, y naviguer
        if "inventory" not in current_url.lower():
            print("Navigation vers la page inventory...")
            inventory_url = f"{self.config['urls']['base_url']}/inventory.html"
            driver.get(inventory_url)
            
            # Attendre que la page soit chargée
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, self.selectors['inventory_page']['inventory_list']))
            )
            print(f"✓ Retour à la page inventory: {driver.current_url}")
        else:
            print("✓ Déjà sur la page inventory")
        
        return driver.current_url

    @keyword("Click About And Return")
    def click_about_and_return(self):
        """Clique sur About, vérifie la page, et retourne automatiquement à inventory"""
        # Cliquer sur About
        self.click_about()
        time.sleep(3)
        
        # Vérifier la page Saucelabs
        try:
            self.verify_saucelabs_page_opened()
            print("✓ Page Saucelabs vérifiée avec succès")
        except Exception as e:
            print(f"⚠ Échec de vérification de la page Saucelabs: {str(e)}")
        
        # Retourner automatiquement à inventory
        return self.return_to_inventory_page()

    @keyword("Test About Page With Auto Return")
    def test_about_page_with_auto_return(self, expect_success=True):
        """
        Test complet de la page About avec retour automatique à inventory
        Args:
            expect_success: Si False, l'échec de vérification est attendu (problem_user)
        """
        # Cliquer sur About
        self.click_about()
        time.sleep(3)
        
        # Vérifier la page Saucelabs
        verification_success = False
        try:
            self.verify_saucelabs_page_opened()
            verification_success = True
            print("✓ Page Saucelabs vérifiée avec succès")
        except Exception as e:
            if expect_success:
                print(f"✗ ÉCHEC INATTENDU: {str(e)}")
            else:
                print(f"✓ ÉCHEC ATTENDU (problem_user): {str(e)}")
        
        # Retourner automatiquement à inventory
        final_url = self.return_to_inventory_page()
        
        # Lever une exception si la vérification a échoué de manière inattendue
        if not verification_success and expect_success:
            raise AssertionError(f"La page Saucelabs ne s'est pas ouverte correctement")
        
        return final_url

    @keyword("Click Reset App State")
    def click_reset_app_state(self):
        """Clique sur l'option 'Reset App State' du menu"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Attendre et cliquer sur Reset App State
        reset_link = wait.until(
            EC.element_to_be_clickable((By.ID, self.selectors['burger_menu']['reset_link']))
        )
        driver.execute_script("arguments[0].click();", reset_link)
        time.sleep(1)
        print("✓ Cliqué sur 'Reset App State'")

    @keyword("Verify Cart Is Empty")
    def verify_cart_is_empty(self):
        """Vérifie que le panier est vide (badge absent)"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        
        # Fermer le menu burger
        self.close_burger_menu()
        
        # Vérifier que le badge du panier n'existe pas
        try:
            badge = driver.find_element(By.CLASS_NAME, self.selectors['inventory_page']['cart_badge'])
            assert not badge.is_displayed(), "Le badge du panier est toujours visible"
        except NoSuchElementException:
            print("✓ Le panier est vide (pas de badge)")

    @keyword("Verify Cart Is Empty After Reset")
    def verify_cart_is_empty_after_reset(self, product_name="Sauce Labs Backpack"):
        """
        Vérifie complètement que le panier est vide après reset en vérifiant :
        1. Le badge du panier n'existe pas ou affiche 0
        2. Le bouton 'Remove' est redevenu 'Add to cart'
        
        Args:
            product_name: Nom du produit à vérifier (par défaut: Sauce Labs Backpack)
        """
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Fermer le menu burger
        self.close_burger_menu()
        time.sleep(0.5)
        
        errors = []
        
        # 1. Vérifier que le badge du panier n'existe pas ou est à 0
        print("Vérification du badge du panier...")
        try:
            badge = driver.find_element(By.CLASS_NAME, self.selectors['inventory_page']['cart_badge'])
            if badge.is_displayed():
                badge_text = badge.text
                if badge_text != "0":
                    error_msg = f"Le badge du panier affiche '{badge_text}' au lieu de 0 ou être absent"
                    print(f"✗ {error_msg}")
                    errors.append(error_msg)
                else:
                    print("⚠ Le badge affiche 0 (devrait être absent)")
            else:
                print("✓ Le badge du panier n'est pas visible")
        except NoSuchElementException:
            print("✓ Le badge du panier n'existe pas (panier vide)")
        
        # 2. Vérifier que le bouton 'Remove' est redevenu 'Add to cart'
        print(f"Vérification du bouton pour '{product_name}'...")
        product_id = product_name.lower().replace(" ", "-")
        
        # Vérifier que le bouton Remove n'existe pas/n'est pas visible
        remove_button_selector = f"button[data-test='remove-{product_id}']"
        try:
            remove_button = driver.find_element(By.CSS_SELECTOR, remove_button_selector)
            if remove_button.is_displayed():
                error_msg = f"Le bouton 'Remove' est toujours visible pour '{product_name}'"
                print(f"✗ {error_msg}")
                errors.append(error_msg)
            else:
                print(f"✓ Le bouton 'Remove' n'est pas visible pour '{product_name}'")
        except NoSuchElementException:
            print(f"✓ Le bouton 'Remove' n'existe pas pour '{product_name}'")
        
        # Vérifier que le bouton 'Add to cart' est présent et visible
        add_button_selector = f"button[data-test='add-to-cart-{product_id}']"
        try:
            add_button = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, add_button_selector))
            )
            
            if not add_button.is_displayed():
                error_msg = f"Le bouton 'Add to cart' n'est pas visible pour '{product_name}'"
                print(f"✗ {error_msg}")
                errors.append(error_msg)
            else:
                button_text = add_button.text.strip().upper()
                if "ADD TO CART" in button_text:
                    print(f"✓ Le bouton 'Add to cart' est présent et visible pour '{product_name}'")
                else:
                    error_msg = f"Le texte du bouton est '{button_text}' au lieu de 'ADD TO CART'"
                    print(f"✗ {error_msg}")
                    errors.append(error_msg)
                    
        except TimeoutException:
            error_msg = f"Le bouton 'Add to cart' est introuvable pour '{product_name}'"
            print(f"✗ {error_msg}")
            errors.append(error_msg)
            driver.save_screenshot("debug_add_button_not_found.png")
        
        # Si des erreurs ont été trouvées, lever une exception
        if errors:
            driver.save_screenshot("debug_cart_not_empty_after_reset.png")
            error_summary = "\n".join([f"  - {err}" for err in errors])
            raise AssertionError(
                f"Le panier n'est pas correctement vide après reset:\n{error_summary}"
            )
        
        print("✓ Le panier est complètement vide après reset (badge absent + bouton 'Add to cart' restauré)")

    @keyword("Click Logout")
    def click_logout(self):
        """Clique sur l'option 'Logout' du menu"""
        browser_lib = self._get_browser_library()
        driver = browser_lib.driver
        wait = WebDriverWait(driver, self.config['timeouts']['default'])
        
        # Attendre et cliquer sur Logout
        logout_link = wait.until(
            EC.element_to_be_clickable((By.ID, self.selectors['burger_menu']['logout_link']))
        )
        driver.execute_script("arguments[0].click();", logout_link)
        print("✓ Cliqué sur 'Logout'")

    @keyword("Verify Saucelabs Page Opened Or Continue")
    def verify_saucelabs_page_opened_or_continue(self):
        """Vérifie la page Saucelabs mais continue en cas d'échec"""
        try:
            self.verify_saucelabs_page_opened()
            return True
        except Exception as e:
            print(f"⚠ La vérification de la page Saucelabs a échoué: {str(e)}")
            print("➜ Continuation du test...")
            return False