# PRD de Gokyo

## 1. Résumé

Gokyo aide les judokas à réviser les techniques de judo sur leur téléphone. L’application réunit une page de révision avec vidéos et un référentiel des techniques généré depuis les données du projet.

## 2. Contexte et références

Le dépôt contient une application Streamlit, un fichier `techniques.json` et deux pages : `prises_judo.py` pour réviser les techniques et `pages/1_Referentiel.py` pour parcourir le référentiel.

Le programme fédéral est accessible depuis la page Référentiel : [document officiel FFJudo](https://www.ffjudo.com/resource-file/document/1789035361_068de2d2976847c37f5a.pdf).

La présente version formalise le comportement attendu à partir de l’application existante. Elle ne prétend pas valider la conformité du contenu pédagogique au document fédéral.

## 3. Utilisateurs

- Judokas qui révisent les noms et les démonstrations des techniques.
- Entraîneurs qui veulent retrouver rapidement une technique pendant un cours.
- Parents et accompagnants qui souhaitent consulter le nom et une explication courte.

## 4. Objectifs

- Rendre la révision d’une technique simple sur un téléphone.
- Donner accès rapidement à une démonstration vidéo et à une description courte.
- Proposer un référentiel parcourable par catégorie et relié aux fiches de révision.
- Permettre le partage d’un lien vers une technique sélectionnée.
- Donner à l’application une identité visuelle énergique, jeune et lisible.

## 5. Hors périmètre

- Comptes utilisateurs, suivi individuel de progression et synchronisation entre appareils.
- Création ou hébergement de vidéos par l’application.
- Modification des exigences officielles de grade ou certification.
- Fonctionnement hors ligne des vidéos YouTube.

## 6. Parcours principaux

### Réviser une technique

1. Le judoka ouvre la page de révision.
2. Il choisit une catégorie puis une technique.
3. Il consulte le nom, la description et la vidéo intégrée.
4. Il peut passer à la technique précédente ou suivante.

### Parcourir le référentiel

1. Le judoka ouvre le Référentiel depuis le bouton dans l’en-tête de la page Réviser.
2. Il parcourt les catégories et ouvre celle qui l’intéresse.
3. Il sélectionne une technique pour ouvrir sa fiche de révision.
4. Il peut ouvrir le document officiel de la FFJudo depuis la page.

### Simuler un tirage d’examen

1. Le judoka ouvre « Défi UV2 » depuis l’en-tête d’une page.
2. Il tire 6 techniques debout et 4 techniques au sol, avec au moins une technique de chaque famille du domaine.
3. Il essaie de réaliser les techniques lui-même et peut demander un nouveau tirage.

### Partager une fiche

La sélection de catégorie et de technique figure dans les paramètres `category` et `technique` de l’URL afin qu’un lien partagé ouvre la fiche correspondante.

## 7. Exigences produit

- La page de révision propose les catégories et techniques disponibles.
- Une technique est sélectionnée par défaut.
- Le changement de catégorie sélectionne une technique de cette catégorie.
- La fiche affiche le nom, une courte description et une vidéo YouTube intégrée.
- Le nom de la technique affiche sa position dans la catégorie, par exemple « 2/6 ».
- Les sélecteurs de catégorie et de technique conservent leurs libellés visibles.
- Les sélecteurs restent utilisables au clavier ; la suppression du clavier tactile ne retire pas leur focus ni leur ordre de tabulation.
- Les commandes précédente et suivante permettent de naviguer dans les techniques.
- La page Référentiel regroupe dynamiquement les techniques selon les catégories des données.
- Le Référentiel propose une recherche instantanée par nom de technique ou famille, sans distinction de casse, d’accent ou de tiret.
- Les familles et leurs techniques apparaissent avant le détail pédagogique de l’UV2.
- La page « Défi UV2 » tire 6 techniques debout et 4 au sol, en couvrant chaque famille, sans chronomètre ni score.
- Un nouveau tirage reste affiché jusqu’à ce que le judoka en demande un autre.
- Chaque technique du référentiel mène à sa fiche avec la catégorie et la technique sélectionnées.
- Un lien vers le document officiel FFJudo est visible sur la page Référentiel.
- Chaque page donne accès aux deux autres vues depuis son en-tête.
- Les boutons restent visibles, compréhensibles et faciles à toucher sur petit écran.
- Le titre et le lien vers la source officielle laissent apparaître rapidement les premières catégories du référentiel.

## 8. Principes d’interface

- Concevoir d’abord pour le téléphone, y compris les petits écrans.
- Utiliser une palette resserrée autour du bleu électrique, du bleu nuit et de fonds clairs, avec une typographie lisible.
- Garder un contraste suffisant entre le texte, les fonds et les commandes.
- Ne pas utiliser la couleur seule pour indiquer l’état actif ou l’action.
- Donner aux commandes tactiles une zone d’interaction confortable.
- En paysage sur mobile, privilégier la vidéo et garder la navigation à portée de doigt.

## 9. Critères d’acceptation

- Depuis la page de révision, un utilisateur peut choisir une technique et voir son nom, sa description et sa vidéo.
- La sélection est reflétée dans les paramètres `category` et `technique` de l’URL.
- Les commandes précédente et suivante changent la technique affichée.
- La fiche indique la position de la technique dans sa catégorie.
- La recherche du Référentiel filtre les techniques et affiche un état explicite lorsqu’aucun résultat ne correspond.
- Le Défi UV2 produit 6 techniques debout et 4 au sol, couvre toutes les familles et ne répète aucune technique dans un tirage.
- Le référentiel reflète les catégories et techniques présentes dans `techniques.json` sans liste dupliquée dans le code HTML.
- Un lien de technique dans le référentiel ouvre la fiche correspondante.
- Le lien du document fédéral ouvre le PDF officiel.
- Les deux pages sont utilisables sur mobile en portrait et en paysage, sans barre latérale et sans défilement horizontal de la page.
- Les textes et commandes restent lisibles avec la palette vive retenue.
- Les liens de navigation conservent un nom accessible lorsque leur libellé visible est compacté sur mobile.

## 10. Décision de direction visuelle

**Pourquoi :** l’interface précédente utilisait une palette discrète rouge et beige. Le besoin exprimé est une apparence plus jeune et plus sportive, adaptée aux judokas de 15 à 18 ans.

**Choix :** adopter le bleu électrique comme accent unique, avec du bleu nuit pour le texte et des fonds clairs. Les états actifs s’appuient aussi sur des libellés, des icônes ou des formes.

**Coût :** les deux pages doivent conserver les mêmes couleurs et états d’interaction. Le contraste doit être vérifié lors de tout changement ultérieur de palette.
