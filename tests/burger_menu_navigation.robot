*** Settings ***
Documentation    Tests de navigation dans le menu burger de SauceDemo
...              Tests séparés par fonctionnalité pour chaque type d'utilisateur

Library    ../Resources/Libraries/BrowserKeywords.py    WITH NAME    Lib1
Library    ../Resources/Libraries/LoginKeywords.py    WITH NAME    Lib2
Library    ../Resources/Libraries/BurgerMenuKeywords.py    WITH NAME    Lib3

Library    BuiltIn

Suite Setup       Open Browser To URL
Suite Teardown    Close Browser



*** Test Cases ***
# ============================================================================
# TESTS STANDARD USER
# ============================================================================

Test Menu Burger Global Standard User
    [Documentation]    Test d'ouverture du menu burger et vérification des options
    ...                pour l'utilisateur standard
    [Tags]    burger_menu    standard_user    menu_visibility    critical
    
    Log    === TEST MENU BURGER GLOBAL - STANDARD USER ===    console=yes
    
    # Connexion
    Login With Standard User
    Sleep    2s
    
    # Test du menu burger
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Vérification menu ouvert    Verify Burger Menu Is Open
    
    Execute Test Step    Vérification des 4 options    Verify Burger Menu Options
    
    # Fermer le menu pour les tests suivants
    Close Burger Menu
    
    Log    === ✓ TEST MENU BURGER GLOBAL RÉUSSI ===    console=yes

Test All Items Option For Standard User
    [Documentation]    Test de l'option "All Items" du menu burger
    ...                Vérifie qu'on reste sur la même page
    [Tags]    burger_menu    standard_user    all_items
    
    Log    === TEST ALL ITEMS - STANDARD USER ===    console=yes
    
    # Ouvrir le menu
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    # Tester All Items
    ${status}    ${current_url}=    Run Keyword And Ignore Error    Click All Items
    Sleep    1s
    
    Run Keyword If    '${status}' == 'PASS'
    ...    Execute Test Step    Vérification même page    Verify Same Page    ${current_url}
    ...    ELSE
    ...    Fail    Échec lors du clic sur All Items
    
    Log    === ✓ TEST ALL ITEMS RÉUSSI ===    console=yes

Test About Option Standard User
    [Documentation]    Test de l'option "About" du menu burger
    ...                Vérifie la redirection vers Saucelabs et le retour
    [Tags]    burger_menu    standard_user    about
    
    Log    === TEST ABOUT - STANDARD USER ===    console=yes
    
    # Ouvrir le menu
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    # Tester About avec retour automatique
    Execute Test Step    Clic sur About    Click About
    Sleep    3s
    
    Execute Test Step    Vérification page Saucelabs    Verify Saucelabs Page Opened
    
    Execute Test Step    Retour automatique à inventory    Return To Inventory Page
    
    # Vérifier qu'on est bien sur la page inventory
    ${current_url}=    Get Current URL
    Should Contain    ${current_url}    inventory    msg=Pas sur la page inventory après le test About
    
    Log    === ✓ TEST ABOUT RÉUSSI ===    console=yes

Test Reset App State Standard User
    [Documentation]    Test de l'option "Reset App State" du menu burger
    ...                Vérifie que le panier est vidé et que les boutons sont restaurés
    [Tags]    burger_menu    standard_user    reset    critical
    
    Log    === TEST RESET APP STATE - STANDARD USER ===    console=yes
    
    # Ajouter un produit au panier
    Execute Test Step    Ajout d'un produit au panier    Add Product To Cart    Sauce Labs Backpack
    Sleep    1s
    
    # Vérifier que le badge affiche 1
    Execute Test Step    Vérification badge panier (1)    Verify Cart Badge Count    1
    
    # Vérifier que le bouton est passé à "Remove"
    Execute Test Step    Vérification bouton Remove    Verify Product Button State    Sauce Labs Backpack    remove
    
    # Ouvrir le menu pour reset
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Clic Reset App State    Click Reset App State
    
    # Vérifications après reset
    Execute Test Step    Vérification badge panier vide    Verify Cart Is Empty
    
    Execute Test Step    Vérification bouton Add to cart    Verify Product Button State    Sauce Labs Backpack    add
    
    # Vérification complète combinée
    Execute Test Step    Vérification complète panier vide    Verify Cart Is Empty After Reset    Sauce Labs Backpack
    
    Log    === ✓ TEST RESET APP STATE RÉUSSI ===    console=yes

Test Logout Standard User
    [Documentation]    Test de l'option "Logout" du menu burger
    ...                Vérifie la déconnexion et le retour à la page login
    [Tags]    burger_menu    standard_user    logout    critical
    
    Log    === TEST LOGOUT - STANDARD USER ===    console=yes
    
    # Ouvrir le menu
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Clic Logout    Click Logout
    Sleep    2s
    
    # Vérification retour à la page login
    Execute Test Step    Vérification page login    Verify Login Page Is Displayed
    
    Log    === ✓ TEST LOGOUT RÉUSSI ===    console=yes

# ============================================================================
# TESTS PROBLEM USER
# ============================================================================

Test Menu Burger Global Problem User
    [Documentation]    Test d'ouverture du menu burger et vérification des options
    ...                pour l'utilisateur problem_user
    [Tags]    burger_menu    problem_user    menu_visibility    known_issue
    
    Log    === TEST MENU BURGER GLOBAL - PROBLEM USER ===    console=yes
    
    # Connexion
    Open Browser To URL
    Login With Problem User
    Sleep    2s
    
    # Test du menu burger
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Vérification menu ouvert    Verify Burger Menu Is Open
    
    Execute Test Step    Vérification des 4 options    Verify Burger Menu Options
    
    # Fermer le menu pour les tests suivants
    Close Burger Menu
    
    Log    === ✓ TEST MENU BURGER GLOBAL RÉUSSI ===    console=yes

Test All Items Option For Problem User
    [Documentation]    Test de l'option "All Items" du menu burger
    ...                pour problem_user
    [Tags]    burger_menu    problem_user    all_items    known_issue
    
    Log    === TEST ALL ITEMS - PROBLEM USER ===    console=yes
    
    # Ouvrir le menu
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    # Tester All Items
    ${status}    ${current_url}=    Run Keyword And Ignore Error    Click All Items
    Sleep    1s
    
    Run Keyword If    '${status}' == 'PASS'
    ...    Execute Test Step    Vérification même page    Verify Same Page    ${current_url}
    ...    ELSE
    ...    Log    ⚠ Échec lors du clic sur All Items (problem_user)    console=yes    level=WARN
    
    Log    === ✓ TEST ALL ITEMS TERMINÉ ===    console=yes

Test About Option Problem User
    [Documentation]    Test de l'option "About" du menu burger pour problem_user
    ...                ÉCHEC ATTENDU: La page Saucelabs ne s'ouvre pas correctement
    [Tags]    burger_menu    problem_user    about    known_issue
    
    Log    === TEST ABOUT - PROBLEM USER ===    console=yes
    
    # Ouvrir le menu
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    # Tester About avec gestion d'échec attendu
    Execute Test Step    Clic sur About    Click About
    Sleep    3s
    
    # Vérification avec gestion d'échec attendu
    ${about_success}=    Run Keyword And Return Status    Verify Saucelabs Page Opened
    
    Run Keyword If    ${about_success}
    ...    Log    ⚠ INATTENDU: La page Saucelabs s'est ouverte pour problem_user    console=yes    level=WARN
    ...    ELSE
    ...    Log    ✗ ÉCHEC ATTENDU: La page Saucelabs ne s'est pas ouverte pour problem_user    console=yes    level=INFO
    
    # Marquer comme échec non-bloquant dans le rapport
    Run Keyword If    not ${about_success}
    ...    BuiltIn.Run Keyword And Continue On Failure
    ...    Fail    Page Saucelabs non ouverte (comportement attendu pour problem_user)
    
    # Retour automatique à inventory
    Execute Test Step    Retour automatique à inventory    Return To Inventory Page
    
    # Vérifier qu'on est bien sur la page inventory
    ${current_url}=    Get Current URL
    Should Contain    ${current_url}    inventory    msg=Pas sur la page inventory après le test About
    
    Log    === ✓ TEST ABOUT TERMINÉ (avec échec attendu) ===    console=yes

Test Reset App State Problem User
    [Documentation]    Test de l'option "Reset App State" du menu burger
    ...                pour problem_user
    [Tags]    burger_menu    problem_user    reset    known_issue
    
    Log    === TEST RESET APP STATE - PROBLEM USER ===    console=yes
    
    # Ajouter un produit au panier
    Execute Test Step    Ajout d'un produit au panier    Add Product To Cart    Sauce Labs Backpack
    Sleep    1s
    
    # Vérifier que le badge affiche 1
    Execute Test Step    Vérification badge panier (1)    Verify Cart Badge Count    1
    
    # Vérifier que le bouton est passé à "Remove"
    Execute Test Step    Vérification bouton Remove    Verify Product Button State    Sauce Labs Backpack    remove
    
    # Ouvrir le menu pour reset
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Clic Reset App State    Click Reset App State
    
    # Vérifications après reset
    Execute Test Step    Vérification badge panier vide    Verify Cart Is Empty
    
    Execute Test Step    Vérification bouton Add to cart    Verify Product Button State    Sauce Labs Backpack    add
    
    # Vérification complète combinée
    Execute Test Step    Vérification complète panier vide    Verify Cart Is Empty After Reset    Sauce Labs Backpack
    
    Log    === ✓ TEST RESET APP STATE RÉUSSI ===    console=yes

Test Logout Problem User
    [Documentation]    Test de l'option "Logout" du menu burger pour problem_user
    ...                Vérifie la déconnexion et le retour à la page login
    [Tags]    burger_menu    problem_user    logout    known_issue
    
    Log    === TEST LOGOUT - PROBLEM USER ===    console=yes
    
    # Ouvrir le menu
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Clic Logout    Click Logout
    Sleep    2s
    
    # Vérification retour à la page login
    Execute Test Step    Vérification page login    Verify Login Page Is Displayed
    
    Log    === ✓ TEST LOGOUT RÉUSSI ===    console=yes

# ============================================================================
# TEST LOCKED USER
# ============================================================================

Test Locked Out User Cannot Login
    [Documentation]    Vérifie que l'utilisateur verrouillé ne peut pas se connecter
    ...                Un message d'erreur approprié doit être affiché
    [Tags]    login    locked_user    negative_test
    
    Log    === TEST UTILISATEUR VERROUILLÉ ===    console=yes
    
    # Se reconnecter après le test précédent
    Open Browser To URL
    
    # Tenter de se connecter avec l'utilisateur verrouillé
    Login With Locked Out User   
    
    # Vérifier le message d'erreur
    Verify Login Error Message    Epic sadface: Sorry, this user has been locked out.
    
    Log    === ✓ TEST LOCKED USER RÉUSSI ===    console=yes

*** Keywords ***
Execute Test Step
    [Documentation]    Exécute une étape de test avec logging amélioré
    ...                Permet de tracer clairement chaque action dans les logs
    [Arguments]    ${step_name}    ${keyword_name}    @{args}
    
    Log    ▶ ${step_name}    console=yes
    
    ${status}    ${result}=    Run Keyword And Ignore Error    ${keyword_name}    @{args}
    
    Run Keyword If    '${status}' == 'PASS'
    ...    Log    ✓ ${step_name}: RÉUSSI    console=yes    level=INFO
    ...    ELSE
    ...    Run Keyword And Continue On Failure    Fail    ${step_name}: ${result}
    
    [Return]    ${status}    ${result}

Execute Step And Continue
    [Documentation]    Exécute une étape et continue même en cas d'échec
    ...                Utile pour les étapes non-critiques
    [Arguments]    ${step_name}    ${keyword_name}    @{args}
    
    Log    ▶ ${step_name} (continue on failure)    console=yes
    
    ${status}    ${result}=    Run Keyword And Ignore Error    ${keyword_name}    @{args}
    
    Run Keyword If    '${status}' == 'PASS'
    ...    Log    ✓ ${step_name}: RÉUSSI    console=yes    level=INFO
    ...    ELSE
    ...    Log    ✗ ${step_name}: ÉCHEC - ${result}    console=yes    level=WARN
    
    [Return]    ${status}