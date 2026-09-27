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

- Une recette est saisie pour **1 portion** (recette de référence, grammes crus par ingrédient).
  Si tu as une recette pour 4, le bouton « ramener à 1 portion » divise toutes les quantités.
- Au moment de manger, on choisit 0,5 / 1 / 1,5 / 2 portions ou une valeur libre (1,25…) :
  chaque ingrédient est multiplié par ce nombre (règle de 3). Les ingrédients qui se comptent
  (œufs, fruits, wraps…) sont arrondis à l'unité entière.
- Chaque profil garde un objectif kcal/jour et une répartition par repas : la barre du repas
  montre où on en est. Un repas qui dépasse est noté quand même (barre pleine + excédent affiché).
- « Ajouter aussi pour… » note le même plat pour l'autre profil, avec son propre nombre de portions.
- Batch : on indique le nombre de portions préparées ; chaque portion mangée est décomptée
  (et rendue si on supprime la ligne).

## Profils au premier lancement

Fanny (150 cm, 1370 kcal, 105 g) et Matthieu (valeurs à ajuster dans Profil > ✎).

## Icône et écran de démarrage

La toque rose (même dessin que l'onglet Recettes) est dans `resources/android/res`, copiée dans le
projet Android par le workflow. Pour la régénérer : `python3 resources/generate_icons.py`.

## Bouton retour Android

Géré par `@capacitor/app` : il ferme la fenêtre ouverte, puis revient à l'écran / l'onglet
précédent ; sur l'écran d'accueil il met l'app en arrière-plan au lieu de la fermer.
