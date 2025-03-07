import time
import json
from datetime import datetime
import os

def print_with_delay(text, delay=0.5):
    print(text)
    time.sleep(delay)

def get_user_input(prompt):
    return input(prompt).lower().strip()

class BistrotZinalChatbot:
    def __init__(self):
        self.restaurant_info = {
            "nom": "BISTROT Zinal",
            "telephone": "+41XXXXXXXXX",  # À remplacer par le vrai numéro
            "adresse": "Route de Zinal XX, 3961 Zinal"
        }
        
        self.commandes_directory = "commandes"
        if not os.path.exists(self.commandes_directory):
            os.makedirs(self.commandes_directory)
        
        self.menu = {
            "sandwichs": {
                "jambon_fromage": {
                    "nom": "Sandwich Jambon-Fromage",
                    "prix": 8.50,
                    "description": "Jambon local et fromage de la vallée"
                },
                "poulet_crudites": {
                    "nom": "Sandwich Poulet-Crudités",
                    "prix": 9.50,
                    "description": "Poulet grillé, légumes frais, sauce maison"
                },
                "veggie_wrap": {
                    "nom": "Wrap Végétarien",
                    "prix": 8.50,
                    "description": "Légumes grillés, houmous, avocat"
                },
                "thon_wrap": {
                    "nom": "Wrap au Thon",
                    "prix": 9.00,
                    "description": "Thon, mayonnaise, crudités"
                }
            },
            "sac_a_dos": {
                "journee": {
                    "nom": "Location Sac à Dos Journée",
                    "prix": 5.00,
                    "description": "Sac à dos confortable avec compartiment isotherme"
                }
            }
        }

    def afficher_menu(self):
        print_with_delay("\n=== 🥪 Menu BISTROT Zinal 🎒 ===")
        
        print_with_delay("\n📌 NOS SANDWICHS ET WRAPS:")
        for id_sandwich, details in self.menu["sandwichs"].items():
            print_with_delay(f"\n{details['nom']} - {details['prix']}CHF")
            print_with_delay(f"  {details['description']}")
        
        print_with_delay("\n📌 LOCATION SAC À DOS:")
        sac = self.menu["sac_a_dos"]["journee"]
        print_with_delay(f"\n{sac['nom']} - {sac['prix']}CHF")
        print_with_delay(f"  {sac['description']}")

    def sauvegarder_commande(self, commande, total, numero_commande, heure_pickup):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        commande_details = {
            "numero_commande": numero_commande,
            "date": timestamp,
            "heure_pickup": heure_pickup,
            "items": commande,
            "total": total,
            "status": "en_attente"
        }
        
        filename = f"commandes/commande_{numero_commande}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(commande_details, f, ensure_ascii=False, indent=4)
        
        print_with_delay("\n📋 BON DE PRÉPARATION - BISTROT ZINAL")
        print_with_delay(f"Numéro: #{numero_commande}")
        print_with_delay(f"À préparer pour: {heure_pickup}")
        print_with_delay("\nArticles:")
        for item in commande:
            print_with_delay(f"  • {item}")
        
        return filename

    def valider_heure_pickup(self, heure):
        try:
            heure_obj = datetime.strptime(heure, "%H:%M")
            heure_actuelle = datetime.now().time()
            heure_pickup = heure_obj.time()
            
            # Vérifier si l'heure est entre 7h et 18h
            if heure_pickup.hour < 7 or heure_pickup.hour >= 18:
                return False, "Les retraits sont possibles entre 7h00 et 18h00"
            
            # Vérifier si l'heure est au moins 30 minutes dans le futur
            if datetime.now().hour == heure_pickup.hour:
                if heure_pickup.minute - heure_actuelle.minute < 30:
                    return False, "Veuillez prévoir au moins 30 minutes de préparation"
            
            return True, ""
        except ValueError:
            return False, "Format d'heure invalide. Utilisez HH:MM"

    def prendre_commande(self):
        print_with_delay("\n👋 Bienvenue au BISTROT Zinal!")
        print_with_delay("Je vais vous aider à commander votre repas à emporter.")
        
        while True:
            self.afficher_menu()
            commande = []
            total = 0
            
            # Commander les sandwichs/wraps
            print_with_delay("\n🥪 Quels sandwichs ou wraps souhaitez-vous ? (tapez 'fin' pour terminer)")
            
            while True:
                choix = get_user_input("\nVotre choix (ou 'fin'): ")
                if choix == 'fin':
                    break
                
                item_trouve = False
                for id_item, details in self.menu["sandwichs"].items():
                    if choix in id_item or choix in details['nom'].lower():
                        commande.append(details['nom'])
                        total += details['prix']
                        print_with_delay(f"✅ {details['nom']} ajouté à votre commande")
                        item_trouve = True
                        break
                
                if not item_trouve:
                    print_with_delay("❌ Désolé, cet article n'est pas dans notre menu")
            
            # Proposer la location de sac à dos
            if commande:
                print_with_delay("\n🎒 Souhaitez-vous louer un sac à dos pour la journée ? (oui/non)")
                if get_user_input("\nVotre choix: ") == "oui":
                    sac = self.menu["sac_a_dos"]["journee"]
                    commande.append(sac['nom'])
                    total += sac['prix']
                    print_with_delay(f"✅ {sac['nom']} ajouté à votre commande")
            
                # Demander l'heure de retrait
                while True:
                    print_with_delay("\n⏰ À quelle heure souhaitez-vous retirer votre commande ? (format HH:MM)")
                    heure_pickup = get_user_input("Heure de retrait: ")
                    valide, message = self.valider_heure_pickup(heure_pickup)
                    if valide:
                        break
                    print_with_delay(f"❌ {message}")
                
                # Générer et sauvegarder la commande
                numero_commande = datetime.now().strftime("%Y%m%d%H%M%S")
                
                print_with_delay("\n📋 Récapitulatif de votre commande:")
                for item in commande:
                    print_with_delay(f"  • {item}")
                print_with_delay(f"\n💶 Total à payer: {total:.2f}CHF")
                
                commande_filename = self.sauvegarder_commande(commande, total, numero_commande, heure_pickup)
                print_with_delay(f"\n📝 Votre commande #{numero_commande} est enregistrée")
                print_with_delay(f"🕒 Retrait à {heure_pickup} au BISTROT Zinal")
                print_with_delay(f"📍 {self.restaurant_info['adresse']}")
                print_with_delay("\n💳 Le paiement se fera sur place au moment du retrait")
                print_with_delay(f"📞 Pour toute question: {self.restaurant_info['telephone']}")
            
            print_with_delay("\n🔄 Souhaitez-vous faire une autre commande ? (oui/non)")
            if get_user_input("\nVotre choix: ") != "oui":
                print_with_delay("\n👋 Merci d'avoir choisi le BISTROT Zinal. À bientôt !")
                break

def main():
    chatbot = BistrotZinalChatbot()
    chatbot.prendre_commande()

if __name__ == "__main__":
    main()