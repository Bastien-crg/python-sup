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
Le dashBoard contient des cartes, des chiffres clés et dans graphiques.
Tout d'abord grâce à la frise chronologique en haut, on peut choisir l'année que l'on souhaite.
La carte nous permet de voir la répartition des établissement sur le territoire et de pouvoir filtrer par type de foramtion.
A côtés nous avons quelques chiffres clés que nous avons voulu mettre en avant ainsi que des camembert montrant la différence entre ce que les élèves demandent et ce que les élèves ont.
Enfin, plus bas dans le dashboard, nous avons d'autres graphiques plus grand que nous avons décidé d'afficher séparément afin d'avoir plus de place pour chaque graphique.
## 2. Developper Guide
### 2.1. Organisation
#### 2.1.1. Les fichiers de données
Les différents fichiers contenant les données se situe dans le dossier data.
Pour générer ces différents fichiers, nous avons créé une classe file_manager, qui prend en paramètres autant de nom de fichier que nous voulons, les ouvres et renvoie une liste avec le contenu des fichier ouvert.
#### 2.1.2. Les graphiques
Afin de limiter le code pour générer des graphique, nous avons créé une classe pour chaque type de graphique.
Elles sont contenue dans dossier chart et héritent toutes de la classe abstract BasicChart.
Chaque classe à un constructeur et une fonction render_chart qui met en forme les données et renvoie un graphique plotly.
#### 2.1.3. Gestion de cartes
YANN
#### 2.1.4. Dash
YANN
### 2.2. Amélioration
Notre dashboard est plutôt lent, une amélioration possible serait de mettre en place un système de cache qui permettrait de ne pas remanipuler les données mais seulement afficher les graphiques.
Cependant au vue de la quantité de données il faudrait faire attention à ce que ça ne surcharge pas trop la RAM.
## 3. Analyse des données
### 3.1. La carte
La carte peut (à première vue) nous donner l'impression que le territoire est maillé de façon homogène.
Cependant il ne faut pas oublier que les point bleu représent les BTS qui se font dans des lycées. Si l'on décide de n'afficher que les PASS ou les écoles d'ingénieur, on voit que le nombre de point se réduit et les grand pôle universitaire ressortent plus facilement (université de Toulouse, Bordeaux, Lyon, Paris...)
On peut également remarqué que l'agglomération de Paris est loin devant les autres (voir aussi classement des villes).
### 3.2. Les graphiques

- Pour le graphique de la répartion fille/garçon, on peut voir notament qu'il y a effectivement moins de fille que de garçon en école d'ingénieur. Par ailleurs le fait que les licences soit en tête chez les fille et les garçon confirme la part important des licences dans les camembert.
- Pour le graphique du classement des villes, le dataset à décidé de segmenter la ville de Paris en arrondissment car elle serait trop grosse. On peut voir qu'il y a 2 arrondissements de paris des le top 10. Cela rejoint ce que nous avions constaté sur les cartes.
- L'histogramme nous montre que le pique se trouve entre 30 et 39 places par formation. Le record se situe autour de 3000 place, mais pour des raison de lisibilité, nous nous sommes arrêté à 200.
- Le nuage de point représente la capacité des établissements en fonction du nombre de formation de cette établissement. On peut voir que globalement cela forme une diagonale et donc (sans surprise) plus il y a de foramtion, plus il yva d'élèves. Pour ce graphique nous avons décidé prendre une échelle logarithmique afin d'avoir un meilleur dispersion des points par rapport à une échelle linéaire.
