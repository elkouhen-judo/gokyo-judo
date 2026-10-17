# Spécification technique

## Portée

Ce document décrit les contraintes d’implémentation de Gokyo. Les objectifs produit, les utilisateurs et les parcours sont décrits dans [PRD.md](PRD.md).

## Architecture

- Application Python basée sur Streamlit.
- Page de révision dans `prises_judo.py`.
- Référentiel dans `pages/1_Referentiel.py`.
- Données chargées depuis le fichier local `techniques.json`.
- Styles responsives définis dans les pages Streamlit.
- Pas de backend applicatif. La lecture des vidéos dépend de YouTube.

## Modèle de données

Chaque entrée de `techniques.json` comporte les propriétés suivantes :

- `category` : catégorie de la technique ;
- `name` : nom de la technique ;
- `youtube` : URL YouTube ;
- `description` : résumé pédagogique.

Les propriétés supplémentaires sont tolérées. L’interface actuelle ne les affiche pas.

## Règles d’affichage

- Les catégories et les techniques du référentiel sont générées à partir de `techniques.json`.
- Les techniques d’une catégorie sont présentées par ordre alphabétique.
- Les liens du référentiel ouvrent la page de révision avec les paramètres `category` et `technique` dans l’URL.
- Le lecteur accepte les formats YouTube `watch`, `youtu.be` et `shorts`.
- La vidéo conserve un ratio 16:9 en orientation portrait.
- En orientation paysage sur mobile, la vidéo occupe l’écran et les commandes de navigation restent accessibles.
- Les deux pages respectent le thème clair/sombre choisi dans Streamlit et, en l’absence de choix explicite, la préférence de couleurs du système.
- Les surfaces, textes, contrôles et menus restent contrastés dans les deux thèmes.

## Mise en page responsive

- L’interface est conçue en priorité pour les écrans mobiles.
- La navigation entre les pages se fait par un bouton de bascule dans l’en-tête de chaque page. La barre latérale Streamlit est masquée.
- En portrait, la page de révision affiche le titre, les sélecteurs, la description et la vidéo.
- Les sélecteurs gardent les libellés « Catégorie » et « Technique » visibles.
- En paysage sur mobile, le titre, les sélecteurs et la description sont masqués pour laisser la place à la vidéo.
- Les commandes interactives doivent rester utilisables au toucher et ne pas ouvrir inutilement le clavier mobile.

## Lancement

Installer les dépendances avec `pip install -r requirements.txt`, puis lancer l’application avec :

```bash
streamlit run prises_judo.py
```
