# python-sup
## Sommaire
1. User Guide
2. Developper Guide
3. Analyse des données
## 1. User Guide
Le projet python-sup (mélange entre python et parcours-sup) a pour but de montrer certaine données du dataset sous forme de graphique.
### 1.1. Déployer le projet
Tout d'abord  il faut récupérer le code : 
```
git clone https://github.com/Bastien-crg/python-sup.git
```
Puis il faut se mettre à la racine du projet et vérifier que toutes les packages nécessaire soit bien installés en allant voir le fichier `requirements.txt`.
```
python -m pip install -r requirements.txt
```
Enfin, vous pouvez lancer le projet en éxecutant `main.py`.
```
python main.py
```
Si vous souhaiter reload les fichiers CSV contenu dans `./data/` il suffit d'éxecuter le fichier `get_data.py`.
```
python get_data.py
```
### 1.2. Le DashBoard
Le dashBoard contient des cartes, des chiffres clé et des graphiques.
Tout d'abord grâce à la frise chronologique en haut, on peut choisir l'année que l'on souhaite.
La carte nous permet de voir la répartition des établissements sur le territoire et de pouvoir filtrer par type de formation.
À côté nous avons quelques chiffres clés que nous avons voulu mettre en avant ainsi que des camembert montrant la différence entre ce que les élèves demandent et ce que les élèves ont.
Enfin, plus bas dans le dashboard, nous avons d'autres graphiques plus grand que nous avons décidé d'afficher séparément afin d'avoir plus de place pour chaque graphique.
## 2. Developper Guide
### 2.1. Organisation
#### 2.1.1. Les fichiers de données
Les différents fichiers contenant les données se situent dans le dossier data.
Pour générer ces différents fichiers, nous avons créé une classe file_manager, qui prend en paramètres autant de nom de fichiers que nous voulons, les ouvres et renvoie une liste avec le contenu des fichier ouvert.
#### 2.1.2. Les graphiques
Afin de limiter le code pour générer des graphiques, nous avons créé une classe pour chaque type de graphique.
Elles sont contenues dans le dossier `./chart` et héritent toutes de la classe abstract BasicChart.
Chaque classe à un constructeur et une fonction render_chart qui met en forme les données et renvoie un graphique plotly.
#### 2.1.3. Gestion de cartes
Pour ne pas avoir de fortes lenteur lorsque l'on change de carte nous avons préférés les pré-générés.
Les cartes sont indentiques pour chaques années.
Pour les crées on a fait une fonction permettant de placer sur une carte de la france les emplacements de tous les batiments disposant d'une formation souhaité.
Ainsi que une fonction appellant la première sur toutes les formations disponible.
A noté que le fichier fournit n'est pas parfait, et que certaines formation ne dispose pas de coordonnées GSP, on ne les mets donc pas.
#### 2.1.4. Dash
Pour la création du dash nous avons décidé de le separer en trois partie:
Une collonne de gauche
une collonne de droite
et une ligne en dessous des deux collonnes.
La colonne de gauche comprend deux parties différentes. La premiere consitue la partie haute et comprend des données importantes. A noter que certaines données ne sont pas disponibles en fonction des années. La partie basse comprends deux gaphique "camenbert", seul un apparait a la fois, il est possible de choisir le quel est visible en cliquant sur le l'onglet contenant le titre de graphique entre les données et le graphique.

La partie de droite elle contient nos différentes cartes qui sont les emplacement des différentes formations disponible sur ParcourSupp. Il est possible de sélectionner une formation en particulière a l'aide de la file déroulante d'option se situant au dessus de la carte. Chaque formation a une couleur différentes et la taille des points est en fonctions de la capacité d'acceuil de l'etablissement où se situe la formation.

La dernière partie elle contient les différents graphique. Il est possible de selectionner le type de graphique au l'on veux voir. Il est aussi possible de cliquer sur le bouton "Hide/Show Graph" qui fera disparaitre ou apparaitre tous les graph. Il y a aussi un bouton "Open Graph" permettant d'ouvrir le graphique dans un autre onglet. Pour un des graphique (bar_chart) il est aussi possible de choisir les formations que on désire voir, il est possible de faire une multi-sélection. Certaines graphiques ne seront pas disponible en fonction de l'année.

A noter que au dessus de ces trois parties, entre le titre et celle-ci, il est possible de choisir l'année que l'on souhaite avoir.

### 2.2. Amélioration
Notre dashboard est plutôt lent, une amélioration possible serait de mettre en place un système de cache qui permettrait de ne pas re-manipuler les données mais seulement afficher les graphiques.
Cependant, au vu de la quantité de données, il faudrait faire attention à ce que ça ne surcharge pas trop la RAM.
## 3. Analyse des données
### 3.1. La carte
La carte peut (à première vue) nous donner l'impression que le territoire est maillé de façon homogène.
Cependant il ne faut pas oublier que les points bleu représentent les BTS qui se font dans des lycées. Si l'on décide de n'afficher que les PASS ou les écoles d'ingénieur, on voit que le nombre de points réduit et les grands pôles universitaire ressortent plus facilement (université de Toulouse, Bordeaux, Lyon, Paris...)
On peut également remarquer que l'agglomération de Paris est loin devant les autres (voir aussi le classement des villes).
### 3.2. Les graphiques
- Pour le graphique de la répartition fille/garçon, on peut voir notamment qu'il y a effectivement moins de fille que de garçon en école d'ingénieur. Par ailleurs le fait que les licences soient en tête chez les filles et les garçons confirme la part importante des licences dans les camembert.
- Pour le graphique du classement des villes, le dataset à décidé de segmenter la ville de Paris en arrondissment, car elle serait trop grosse. On peut voir qu'il y a 2 arrondissements de Paris dans le top 10. Cela rejoint ce que nous avions constaté sur les cartes.
- L'histogramme nous montre que le pic se trouve entre 30 et 39 places par formation. Le record se situe autour de 3000 place, mais pour des raison de lisibilité, nous nous sommes arrêté à 200.
- Le nuage de point représente la capacité des établissements en fonction du nombre de formation de cet établissement. On peut voir que globalement cela forme une diagonale et donc (sans surprise) plus il y a de formation, plus il y a d'élèves. Pour ce graphique, nous avons décidé prendre une échelle logarithmique afin d'avoir une meilleure dispersion des points par rapport à une échelle linéaire.
