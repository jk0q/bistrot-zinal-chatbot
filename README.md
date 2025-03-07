# BISTROT Zinal Chatbot 🏔️

Un chatbot optimisé pour commander des sandwichs et louer des sacs à dos au BISTROT Zinal.

## Fonctionnalités 🌟

### Pour les Clients
- Commande intuitive de sandwichs et wraps
- Location de sac à dos avec compartiment isotherme
- Choix de l'heure de retrait avec validation intelligente
- Système de confirmation détaillé
- Interface utilisateur améliorée avec emojis

### Pour le Restaurant
- Génération de bons de commande détaillés
- Suivi des statistiques de vente
- Gestion des heures de pointe
- Logging des opérations
- Sauvegarde sécurisée des données

## Menu 🥪

### Sandwichs
- Jambon-Fromage (8.50 CHF)
- Poulet-Crudités (9.50 CHF)

### Wraps
- Végétarien (8.50 CHF)
- Thon (9.00 CHF)

### Location
- Sac à Dos Journée (5.00 CHF)

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
python bistrot_zinal_chatbot.py
```

## Horaires de Service ⏰

- Heures d'ouverture : 7h00 - 18h00
- Délai de préparation minimum : 30 minutes
- Format de l'heure : HH:MM

## Structure des Données 📁

### Commandes
Les commandes sont sauvegardées dans le dossier `commandes/` au format JSON avec :
- Numéro de commande unique (format: BZYYYYMMDDHHMMSS)
- Date et heure de la commande
- Heure de retrait
- Articles commandés
- Montant total
- Informations client
- Statut de la commande

### Statistiques
Le système maintient des statistiques sur :
- Nombre total de commandes
- Articles les plus populaires
- Heures de pointe
- Revenus totaux

## Gestion des Erreurs 🛡️

- Validation des entrées utilisateur
- Gestion des exceptions
- Logging des erreurs
- Messages d'erreur utilisateur conviviaux

## Contact 📞

BISTROT Zinal
Route de Zinal XX, 3961 Zinal
Tél: +41XXXXXXXXX