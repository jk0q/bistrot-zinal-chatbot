# BISTROT Zinal Chatbot 🏔️

Un chatbot simple pour commander des sandwichs et louer des sacs à dos au BISTROT Zinal.

## Fonctionnalités 🌟

- Commande de sandwichs et wraps variés
- Location de sac à dos avec compartiment isotherme
- Choix de l'heure de retrait
- Génération de bons de commande
- Sauvegarde des commandes au format JSON

## Menu 🥪

- Sandwich Jambon-Fromage (8.50 CHF)
- Sandwich Poulet-Crudités (9.50 CHF)
- Wrap Végétarien (8.50 CHF)
- Wrap au Thon (9.00 CHF)
- Location Sac à Dos Journée (5.00 CHF)

## Installation 🛠️

1. Clonez le dépôt :
```bash
git clone https://github.com/jk0q/bistrot-zinal-chatbot.git
cd bistrot-zinal-chatbot
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation 🚀

Lancez le chatbot :
```bash
python hotel_breakfast_chatbot.py
```

## Horaires de retrait ⏰

- Les commandes peuvent être retirées entre 7h00 et 18h00
- Prévoir au moins 30 minutes de préparation
- Format de l'heure : HH:MM

## Structure des données 📁

Les commandes sont sauvegardées dans le dossier `commandes/` au format JSON avec les informations suivantes :
- Numéro de commande unique
- Date et heure de la commande
- Heure de retrait
- Articles commandés
- Montant total
- Statut de la commande

## Contact 📞

BISTROT Zinal
Route de Zinal XX, 3961 Zinal
Tél: +41XXXXXXXXX