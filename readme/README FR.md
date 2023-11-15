# Téléchargeur d'Images Reddit

## Description

Le Téléchargeur d'Images Reddit est un script Python qui permet de télécharger des images à partir de posts Reddit. Il est capable de télécharger des images à partir de liens externes comme Imgur.

## Fonctionnalités

- Télécharge des images à partir de posts Reddit.
- Prend en charge les liens externes comme Imgur.
- Gère différents types de formats d'image (JPEG, PNG, etc.).
- Gestion des erreurs pour les URL invalides ou le contenu inaccessible.

## Comment ça marche

Le script fonctionne en effectuant des requêtes HTTP vers les URL de posts Reddit spécifiées. Il analyse la réponse HTML pour trouver les liens d'images, puis télécharge les images en utilisant la bibliothèque `requests`.

## Prérequis

- Python 3.6 ou supérieur
- Bibliothèque Python `requests`

## Installation

1. Assurez-vous que Python 3.6 ou supérieur est installé sur votre machine.
2. Clonez ce dépôt sur votre machine locale en utilisant `git clone https://github.com/votreusername/telechargeur-images-reddit.git`.
3. Installez la bibliothèque `requests` en utilisant pip : `pip install requests`.

## Utilisation

1. Ouvrez un terminal et naviguez jusqu'au répertoire où vous avez cloné le dépôt.
2. Exécutez le script Python `reddit_scraper.py` avec l'URL du post Reddit comme argument. Par exemple : `python reddit_scraper.py https://www.reddit.com/r/exemplepost`.

## Contribution

Les contributions sont les bienvenues ! Pour contribuer à ce projet, veuillez forker ce dépôt, apporter vos modifications, puis ouvrir une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Auteur

MrFlappy0 (Discord: [mrflappy0](https://discord.com/users/mrflappy0)))

## Remerciements

Merci d'utiliser le Téléchargeur d'Images Reddit !
