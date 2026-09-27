# Nos Repas — app tablette (Fanny & Matthieu)

Suivi des repas quotidiens, recettes avec photos, table d'ingrédients (kcal / protéines pour 100 g),
portions calculées par profil, batch cooking avec décrément automatique, courbe de poids, calendrier + récap.

Toute l'app tient dans `www/index.html`. Les données restent sur la tablette
(localStorage pour les données, IndexedDB pour les photos).

## Compiler l'APK (même procédure que Carnet de salle)

```bash
git clone <ce dépôt> && cd App-cooking
npm install
npx cap add android        # une seule fois
npx cap sync android       # à refaire après chaque modification de www/index.html
npx cap open android       # ouvre Android Studio → Build > Build APK(s)
```

Ou en ligne de commande : `npm run build:apk` → l'APK est dans
`android/app/build/outputs/apk/debug/app-debug.apk`.

Pour tester sans compiler : ouvrir `www/index.html` dans Chrome sur la tablette
et « Ajouter à l'écran d'accueil ».

## Logique des portions

- Une recette est saisie pour le **plat entier** (grammes crus par ingrédient).
- Chaque profil a un objectif kcal/jour, un objectif protéines et une répartition
  (petit-déj 25 %, déjeuner 35 %, collation 10 %, dîner 30 %, modifiable).
- « Ta portion » = la quantité du plat qui couvre la part du repas dans l'objectif du profil.
- Dans le suivi : choix de la recette → 0.5 / 1 / 1.5 / 2 portions ou grammes exacts.
- La portion est détaillée **ingrédient par ingrédient** (grammes crus à peser). Les ingrédients
  qui se comptent (œufs, fruits, wraps…) ont une unité et un poids unitaire : la portion tombe
  sur un nombre entier (ex. « 2 œufs »), et les kcal/protéines notées correspondent à ces quantités.
- Un repas peut dépasser son objectif : il est noté quand même, la barre du repas est pleine et
  l'excédent s'affiche (+X kcal).
- « Ajouter aussi la portion de… » note le même plat pour l'autre profil, avec sa propre portion.
- Si la recette a un batch en stock, on peut y piocher : les grammes sont décomptés
  (et rendus si on supprime la ligne).

## Profils au premier lancement

Fanny (150 cm, 1370 kcal, 105 g) et Matthieu (valeurs à ajuster dans Profil > ✎).

## Icône et écran de démarrage

La toque rose (même dessin que l'onglet Recettes) est dans `resources/android/res`, copiée dans le
projet Android par le workflow. Pour la régénérer : `python3 resources/generate_icons.py`.

## Bouton retour Android

Géré par `@capacitor/app` : il ferme la fenêtre ouverte, puis revient à l'écran / l'onglet
précédent ; sur l'écran d'accueil il met l'app en arrière-plan au lieu de la fermer.
