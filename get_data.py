import requests

# 2021
req = requests.get("https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcoursup/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B")
url_content = req.content
csv_file = open("./data/fr-esr-parcoursup-2021.csv","wb")
csv_file.write(url_content)
csv_file.close()

# 2020
req = requests.get("https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcoursup_2020/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B")
url_content = req.content
csv_file = open("./data/fr-esr-parcoursup-2020.csv","wb")
csv_file.write(url_content)
csv_file.close()

# 2019
req = requests.get("https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcoursup-2019/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B")
url_content = req.content
csv_file = open("./data/fr-esr-parcoursup-2019.csv","wb")
csv_file.write(url_content)
csv_file.close()

# 2018
req = requests.get("https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcoursup-2018/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B")
url_content = req.content
csv_file = open("./data/fr-esr-parcoursup-2018.csv","wb")
csv_file.write(url_content)
csv_file.close()

