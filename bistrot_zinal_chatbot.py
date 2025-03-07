import time
import json
from datetime import datetime, timedelta
import os
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass, asdict
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bistrot_zinal.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

@dataclass
class MenuItem:
    nom: str
    prix: float
    description: str
    categorie: str
    id: str
    disponible: bool = True

@dataclass
class Commande:
    numero_commande: str
    date: str
    heure_pickup: str
    items: List[str]
    total: float
    status: str
    nom_client: Optional[str] = None
    telephone_client: Optional[str] = None

class BistrotZinalChatbot:
    def __init__(self):
        self._charger_configuration()
        self._initialiser_stockage()
        self.commande_en_cours: List[MenuItem] = []
        
    def _charger_configuration(self) -> None:
        """Charge la configuration du restaurant et du menu"""
        self.restaurant_info = {
            "nom": "BISTROT Zinal",
            "telephone": "+41XXXXXXXXX",
            "adresse": "Route de Zinal XX, 3961 Zinal",
            "heures_ouverture": {
                "debut": 7,
                "fin": 18,
                "preparation": 30  # minutes
            }
        }
        
        # Menu avec dataclasses pour une meilleure structure
        self.menu: Dict[str, MenuItem] = {
            "jambon_fromage": MenuItem(
                nom="Sandwich Jambon-Fromage",
                prix=8.50,
                description="Jambon local et fromage de la vallée",
                categorie="sandwich",
                id="jambon_fromage"
            ),
            "poulet_crudites": MenuItem(
                nom="Sandwich Poulet-Crudités",
                prix=9.50,
                description="Poulet grillé, légumes frais, sauce maison",
                categorie="sandwich",
                id="poulet_crudites"
            ),
            "veggie_wrap": MenuItem(
                nom="Wrap Végétarien",
                prix=8.50,
                description="Légumes grillés, houmous, avocat",
                categorie="wrap",
                id="veggie_wrap"
            ),
            "thon_wrap": MenuItem(
                nom="Wrap au Thon",
                prix=9.00,
                description="Thon, mayonnaise, crudités",
                categorie="wrap",
                id="thon_wrap"
            ),
            "sac_journee": MenuItem(
                nom="Location Sac à Dos Journée",
                prix=5.00,
                description="Sac à dos confortable avec compartiment isotherme",
                categorie="location",
                id="sac_journee"
            )
        }

    def _initialiser_stockage(self) -> None:
        """Initialise les dossiers de stockage"""
        self.commandes_directory = "commandes"
        os.makedirs(self.commandes_directory, exist_ok=True)
        
        # Créer un fichier de statistiques s'il n'existe pas
        self.stats_file = os.path.join(self.commandes_directory, "statistiques.json")
        if not os.path.exists(self.stats_file):
            self._initialiser_statistiques()

    def _initialiser_statistiques(self) -> None:
        """Initialise le fichier de statistiques"""
        stats = {
            "total_commandes": 0,
            "articles_populaires": {},
            "heures_populaires": {},
            "revenu_total": 0.0
        }
        self._sauvegarder_statistiques(stats)

    def _sauvegarder_statistiques(self, stats: Dict) -> None:
        """Sauvegarde les statistiques"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)

    def _mettre_a_jour_statistiques(self, commande: Commande) -> None:
        """Met à jour les statistiques après une commande"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            
            stats["total_commandes"] += 1
            stats["revenu_total"] += commande.total
            
            heure = commande.heure_pickup.split(':')[0]
            stats["heures_populaires"][heure] = stats["heures_populaires"].get(heure, 0) + 1
            
            for item in commande.items:
                stats["articles_populaires"][item] = stats["articles_populaires"].get(item, 0) + 1
            
            self._sauvegarder_statistiques(stats)
            
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour des statistiques: {e}")

    def afficher_menu(self) -> None:
        """Affiche le menu de manière organisée"""
        self._afficher_titre("Menu BISTROT Zinal", "🥪")
        
        categories = {
            "sandwich": "SANDWICHS",
            "wrap": "WRAPS",
            "location": "LOCATION"
        }
        
        for categorie, titre in categories.items():
            items = [item for item in self.menu.values() if item.categorie == categorie and item.disponible]
            if items:
                self._afficher_section(titre, items)

    def _afficher_titre(self, titre: str, emoji: str = "") -> None:
        """Affiche un titre formaté"""
        print_with_delay(f"\n{'='*20} {emoji} {titre} {emoji} {'='*20}")

    def _afficher_section(self, titre: str, items: List[MenuItem]) -> None:
        """Affiche une section du menu"""
        print_with_delay(f"\n📌 {titre}:")
        for item in items:
            print_with_delay(f"\n{item.nom} - {item.prix:.2f}CHF")
            print_with_delay(f"  {item.description}")

    def valider_heure_pickup(self, heure: str) -> Tuple[bool, str]:
        """Valide l'heure de retrait avec gestion des erreurs améliorée"""
        try:
            heure_obj = datetime.strptime(heure, "%H:%M")
            heure_pickup = heure_obj.time()
            maintenant = datetime.now()
            
            # Vérifier les heures d'ouverture
            if (heure_pickup.hour < self.restaurant_info["heures_ouverture"]["debut"] or 
                heure_pickup.hour >= self.restaurant_info["heures_ouverture"]["fin"]):
                return False, f"Les retraits sont possibles entre {self.restaurant_info['heures_ouverture']['debut']}h00 et {self.restaurant_info['heures_ouverture']['fin']}h00"
            
            # Calculer le délai minimum
            temps_preparation = timedelta(minutes=self.restaurant_info["heures_ouverture"]["preparation"])
            heure_pickup_complete = datetime.combine(maintenant.date(), heure_pickup)
            
            if heure_pickup_complete < maintenant + temps_preparation:
                return False, f"Veuillez prévoir au moins {self.restaurant_info['heures_ouverture']['preparation']} minutes de préparation"
            
            return True, ""
            
        except ValueError:
            return False, "Format d'heure invalide. Utilisez HH:MM"

    def _generer_numero_commande(self) -> str:
        """Génère un numéro de commande unique"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BZ{timestamp}"

    def sauvegarder_commande(self, commande: Commande) -> str:
        """Sauvegarde la commande avec gestion des erreurs"""
        try:
            filename = os.path.join(self.commandes_directory, f"commande_{commande.numero_commande}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(asdict(commande), f, ensure_ascii=False, indent=4)
            
            self._mettre_a_jour_statistiques(commande)
            self._afficher_bon_preparation(commande)
            
            return filename
            
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de la commande: {e}")
            raise

    def _afficher_bon_preparation(self, commande: Commande) -> None:
        """Affiche le bon de préparation"""
        self._afficher_titre("BON DE PRÉPARATION - BISTROT ZINAL", "📋")
        print_with_delay(f"Numéro: #{commande.numero_commande}")
        print_with_delay(f"À préparer pour: {commande.heure_pickup}")
        if commande.nom_client:
            print_with_delay(f"Client: {commande.nom_client}")
        print_with_delay("\nArticles:")
        for item in commande.items:
            print_with_delay(f"  • {item}")

    def _obtenir_infos_client(self) -> Tuple[str, str]:
        """Obtient les informations du client"""
        print_with_delay("\n📝 Pour finaliser votre commande, merci de nous indiquer :")
        nom = input("Votre nom : ").strip()
        tel = input("Votre numéro de téléphone : ").strip()
        return nom, tel

    def prendre_commande(self) -> None:
        """Gère le processus de commande principal"""
        self._afficher_titre("Bienvenue au BISTROT Zinal!", "👋")
        print_with_delay("Je vais vous aider à commander votre repas à emporter.")
        
        while True:
            try:
                self.afficher_menu()
                commande_items = []
                total = 0
                
                # Commander les sandwichs/wraps
                print_with_delay("\n🥪 Quels sandwichs ou wraps souhaitez-vous ? (tapez 'fin' pour terminer)")
                
                while True:
                    choix = get_user_input("\nVotre choix (ou 'fin'): ")
                    if choix == 'fin':
                        break
                    
                    item = self._trouver_item(choix)
                    if item:
                        commande_items.append(item.nom)
                        total += item.prix
                        print_with_delay(f"✅ {item.nom} ajouté à votre commande")
                    else:
                        print_with_delay("❌ Désolé, cet article n'est pas dans notre menu")
                
                if commande_items:
                    # Proposer la location de sac à dos
                    if self._proposer_sac_a_dos():
                        sac = self.menu["sac_journee"]
                        commande_items.append(sac.nom)
                        total += sac.prix
                    
                    # Obtenir l'heure de retrait
                    heure_pickup = self._obtenir_heure_retrait()
                    
                    # Obtenir les informations du client
                    nom_client, tel_client = self._obtenir_infos_client()
                    
                    # Créer et sauvegarder la commande
                    commande = Commande(
                        numero_commande=self._generer_numero_commande(),
                        date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                        heure_pickup=heure_pickup,
                        items=commande_items,
                        total=total,
                        status="en_attente",
                        nom_client=nom_client,
                        telephone_client=tel_client
                    )
                    
                    self._afficher_recapitulatif(commande)
                    filename = self.sauvegarder_commande(commande)
                    
                    self._afficher_confirmation(commande)
                
                if not self._demander_nouvelle_commande():
                    break
                    
            except Exception as e:
                logging.error(f"Erreur lors de la prise de commande: {e}")
                print_with_delay("❌ Une erreur est survenue. Veuillez réessayer.")
                if not self._demander_nouvelle_commande():
                    break

    def _trouver_item(self, recherche: str) -> Optional[MenuItem]:
        """Trouve un item dans le menu"""
        recherche = recherche.lower()
        for item in self.menu.values():
            if (recherche in item.id.lower() or 
                recherche in item.nom.lower() or 
                recherche in item.description.lower()):
                return item
        return None

    def _proposer_sac_a_dos(self) -> bool:
        """Propose la location de sac à dos"""
        print_with_delay("\n🎒 Souhaitez-vous louer un sac à dos pour la journée ? (oui/non)")
        return get_user_input("\nVotre choix: ") == "oui"

    def _obtenir_heure_retrait(self) -> str:
        """Obtient une heure de retrait valide"""
        while True:
            print_with_delay("\n⏰ À quelle heure souhaitez-vous retirer votre commande ? (format HH:MM)")
            heure_pickup = get_user_input("Heure de retrait: ")
            valide, message = self.valider_heure_pickup(heure_pickup)
            if valide:
                return heure_pickup
            print_with_delay(f"❌ {message}")

    def _afficher_recapitulatif(self, commande: Commande) -> None:
        """Affiche le récapitulatif de la commande"""
        self._afficher_titre("Récapitulatif de votre commande", "📋")
        for item in commande.items:
            print_with_delay(f"  • {item}")
        print_with_delay(f"\n💶 Total à payer: {commande.total:.2f}CHF")

    def _afficher_confirmation(self, commande: Commande) -> None:
        """Affiche la confirmation de la commande"""
        print_with_delay(f"\n📝 Votre commande #{commande.numero_commande} est enregistrée")
        print_with_delay(f"🕒 Retrait à {commande.heure_pickup} au BISTROT Zinal")
        print_with_delay(f"📍 {self.restaurant_info['adresse']}")
        print_with_delay("\n💳 Le paiement se fera sur place au moment du retrait")
        print_with_delay(f"📞 Pour toute question: {self.restaurant_info['telephone']}")

    def _demander_nouvelle_commande(self) -> bool:
        """Demande si le client veut faire une nouvelle commande"""
        print_with_delay("\n🔄 Souhaitez-vous faire une autre commande ? (oui/non)")
        if get_user_input("\nVotre choix: ") != "oui":
            print_with_delay("\n👋 Merci d'avoir choisi le BISTROT Zinal. À bientôt !")
            return False
        return True

def print_with_delay(text: str, delay: float = 0.5) -> None:
    """Affiche du texte avec un délai"""
    print(text)
    time.sleep(delay)

def get_user_input(prompt: str) -> str:
    """Obtient et nettoie l'entrée utilisateur"""
    return input(prompt).lower().strip()

def main():
    try:
        chatbot = BistrotZinalChatbot()
        chatbot.prendre_commande()
    except KeyboardInterrupt:
        print_with_delay("\n\n👋 Au revoir !")
    except Exception as e:
        logging.error(f"Erreur fatale: {e}")
        print_with_delay("\n❌ Une erreur est survenue. Veuillez réessayer plus tard.")

if __name__ == "__main__":
    main()