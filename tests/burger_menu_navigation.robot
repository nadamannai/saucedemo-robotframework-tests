*** Settings ***
Documentation    Tests de navigation dans le menu burger de SauceDemo
...              avec différents types d'utilisateurs et gestion adaptative des échecs

Library    ../Resources/Libraries/BrowserKeywords.py    WITH NAME    Lib1
Library    ../Resources/Libraries/LoginKeywords.py    WITH NAME    Lib2
Library    ../Resources/Libraries/BurgerMenuKeywords.py    WITH NAME    Lib3
Library    BuiltIn

Suite Setup       Open Browser To URL
Suite Teardown    Close Browser

*** Variables ***
${STANDARD_USER}        standard_user
${PROBLEM_USER}         problem_user
${LOCKED_USER}          locked_out_user
${PASSWORD}             secret_sauce

*** Test Cases ***
Test Burger Menu With Standard User
    [Documentation]    Test complet du menu burger avec l'utilisateur standard
    ...                Toutes les fonctionnalités doivent fonctionner correctement
    [Tags]    burger_menu    standard_user    critical
    
    Log    === TEST AVEC UTILISATEUR STANDARD ===    console=yes
    
    # Connexion
    Login With User    ${STANDARD_USER}    ${PASSWORD}
    Sleep    2s
    
    # Test du menu burger avec type d'utilisateur standard
    Test Complete Burger Menu Navigation For User Type    user_type=standard
    
    Log    === ✓ TEST STANDARD USER RÉUSSI ===    console=yes

Test Burger Menu With Problem User
    [Documentation]    Test du menu burger avec problem_user
    ...                Échec attendu sur la page About (ne s'ouvre pas)
    ...                Les autres fonctionnalités doivent continuer à être testées
    [Tags]    burger_menu    problem_user    known_issue
    
    Log    === TEST AVEC PROBLEM USER ===    console=yes
    
    # Se reconnecter après le test précédent
    Open Browser To URL
    Login With User    ${PROBLEM_USER}    ${PASSWORD}
    Sleep    2s
    
    # Test du menu burger avec type d'utilisateur problem
    Test Complete Burger Menu Navigation For User Type    user_type=problem
    
    Log    === ✓ TEST PROBLEM USER TERMINÉ ===    console=yes

Test Locked Out User Cannot Login
    [Documentation]    Vérifie que l'utilisateur verrouillé ne peut pas se connecter
    ...                Un message d'erreur approprié doit être affiché
    [Tags]    login    locked_user    negative_test
    
    Log    === TEST UTILISATEUR VERROUILLÉ ===    console=yes
    
    # Se reconnecter après le test précédent
    Open Browser To URL
    
    # Tenter de se connecter avec l'utilisateur verrouillé
    Login With User Should Fail    ${LOCKED_USER}    ${PASSWORD}
    
    # Vérifier le message d'erreur
    Verify Login Error Message    Epic sadface: Sorry, this user has been locked out.
    
    Log    === ✓ TEST LOCKED USER RÉUSSI ===    console=yes

*** Keywords ***
Test Complete Burger Menu Navigation For User Type
    [Documentation]    Keyword adaptatif pour tester le menu burger selon le type d'utilisateur
    ...                - standard: toutes les fonctionnalités doivent fonctionner
    ...                - problem: About peut échouer mais le test continue
    [Arguments]    ${user_type}=standard
    
    # Déterminer le comportement attendu pour About selon le type d'utilisateur
    ${continue_on_about_failure}=    Set Variable If    
    ...    '${user_type}' == 'problem'    ${TRUE}    ${FALSE}
    
    Log    Configuration: continue_on_about_failure=${continue_on_about_failure}    console=yes
    
    # === ÉTAPE 1: Ouvrir et vérifier le menu burger ===
    Execute Test Step    Ouverture du menu burger    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Vérification menu ouvert    Verify Burger Menu Is Open
    
    Execute Test Step    Vérification des 4 options    Verify Burger Menu Options
    
    # === ÉTAPE 2: Tester "All Items" ===
    Log    Test de All Items    console=yes
    ${status}    ${current_url}=    Run Keyword And Ignore Error    Click All Items
    Sleep    1s
    
    Run Keyword If    '${status}' == 'PASS'
    ...    Execute Test Step    Vérification même page    Verify Same Page    ${current_url}
    ...    ELSE
    ...    Log    ⚠ Échec lors du clic sur All Items    console=yes    level=WARN
    
    # === ÉTAPE 3: Tester "About" avec retour automatique ===
    Log    Test de About avec retour automatique    console=yes
    Execute Test Step    Ouverture du menu    Open Burger Menu
    Sleep    1s
    
    # Comportement conditionnel selon le type d'utilisateur
    Run Keyword If    ${continue_on_about_failure}
    ...    Test About With Auto Return For Problem User
    ...    ELSE
    ...    Test About With Auto Return For Standard User
    
    # === ÉTAPE 4: Vérifier qu'on est bien sur la page inventory ===
    Log    Vérification page inventory après retour    console=yes
    ${current_url}=    Get Current URL
    Should Contain    ${current_url}    inventory    msg=Pas sur la page inventory après le test About
    Log    ✓ Retour sur la page inventory confirmé    console=yes
    
    # === ÉTAPE 5: Tester "Reset App State" ===
    Log    Test de Reset App State    console=yes
    
    # Ajouter un produit au panier avant le test de reset
    Execute Test Step    Ajout d'un produit au panier    Add Product To Cart    Sauce Labs Backpack
    Sleep    1s
    
    # Vérifier que le badge affiche 1
    Execute Test Step    Vérification badge panier (1)    Verify Cart Badge Count    1
    
    # Vérifier que le bouton est passé à "Remove"
    Execute Test Step    Vérification bouton Remove    Verify Product Button State    Sauce Labs Backpack    remove
    
    # Ouvrir le menu pour reset
    Execute Test Step    Ouverture du menu    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Clic Reset App State    Click Reset App State
    
    # Vérification complète après reset
    Execute Test Step    Vérification badge panier vide    Verify Cart Is Empty
    
    Execute Test Step    Vérification bouton Add to cart    Verify Product Button State    Sauce Labs Backpack    add
    
    # Vérification complète combinée (optionnelle, pour double validation)
    Execute Test Step    Vérification complète panier vide    Verify Cart Is Empty After Reset    Sauce Labs Backpack
    
    # === ÉTAPE 6: Déconnexion ===
    Log    Déconnexion    console=yes
    Execute Test Step    Ouverture du menu    Open Burger Menu
    Sleep    1s
    
    Execute Test Step    Clic Logout    Click Logout
    Sleep    2s
    
    # === ÉTAPE 7: Vérification finale ===
    Execute Test Step    Vérification page login    Verify Login Page Is Displayed
    
    Log    ✓ Toutes les étapes du test ont été exécutées    console=yes

Test About With Auto Return For Standard User
    [Documentation]    Test de About pour standard_user avec retour automatique
    
    Execute Test Step    Clic sur About    Click About
    Sleep    3s
    
    Execute Test Step    Vérification page Saucelabs    Verify Saucelabs Page Opened
    
    Execute Test Step    Retour automatique à inventory    Return To Inventory Page

Test About With Auto Return For Problem User
    [Documentation]    Test de About pour problem_user avec retour automatique et gestion d'erreur
    
    Execute Test Step    Clic sur About    Click About
    Sleep    3s
    
    # Vérification avec gestion d'échec attendu
    ${about_success}=    Run Keyword And Return Status    Verify Saucelabs Page Opened
    
    Run Keyword If    ${about_success}
    ...    Log    ⚠ INATTENDU: La page Saucelabs s'est ouverte pour problem_user    console=yes    level=WARN
    ...    ELSE
    ...    Log    ✗ ÉCHEC: La page Saucelabs ne s'est pas ouverte pour problem_user    console=yes    level=INFO
    
    # Marquer comme échec non-bloquant dans le rapport
    Run Keyword If    not ${about_success}
    ...    BuiltIn.Run Keyword And Continue On Failure
    ...    Fail    Page Saucelabs non ouverte (comportement attendu pour problem_user)
    
    # Retour automatique à inventory dans tous les cas
    Execute Test Step    Retour automatique à inventory    Return To Inventory Page

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

