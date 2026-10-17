# gokyo

Gokyo est une application Streamlit conçue pour réviser les techniques de judo sur mobile. Elle propose une page de révision avec vidéos et un référentiel des prises organisé par catégorie.

Le [PRD](PRD.md) décrit les utilisateurs, les objectifs et les parcours. La [spécification technique](spec.md) documente les données, l’architecture et le comportement responsive.

### Comment l'utiliser

1. Installez les dépendances

   ```bash
   pip install -r requirements.txt
   ```

2. Lancez l'application

   ```bash
   streamlit run prises_judo.py
   ```

3. Choisissez une catégorie puis une prise, ou ouvrez le Référentiel depuis la barre de navigation en bas.

4. Consultez la description et la vidéo YouTube. Le Référentiel contient aussi un lien vers le document officiel de la FFJudo.

### Vérification mobile

Lancez l'application, puis exécutez le contrôle Playwright :

```bash
python tests/mobile_layout_check.py
```
