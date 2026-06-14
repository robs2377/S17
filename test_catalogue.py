import unittest
from livre_s17 import Livre
import catalogue as f

class TestCatalogue(unittest.TestCase):

    def setUp(self):
        self.livre1 = Livre("1984", "Orwell", "9780451524935", 328, 1949)
        self.livre2 = Livre("La Ferme des animaux", "Orwell", "9782070375165", 112, 1945)
        self.livre3 = Livre("Le Meilleur des mondes", "Huxley", "9780060850524", 288, 1932)
        self.livre4 = Livre("Fahrenheit 451", "Bradbury", "9781451673319", 256, 1953)
        
        # Doublon avec meme isbn
        self.doublon = Livre("1984 (réédition)", "Orwell", "9780451524935", 400, 1980)
        
        self.catalogue_test = [self.livre1, self.livre2, self.livre3, self.livre4]
        self.catalogue_avec_doublon = self.catalogue_test + [self.doublon]

    # 1. TESTS D'ORDRE POUR CHAQUE FONCTION DE TRI
    def test_tri_par_auteur_puis_annee_recente(self):
        resultat = f.trier_par_auteur_puis_annee_recente(self.catalogue_test)
        couple_obtenus = [(livre.auteur, livre.annee) for livre in resultat]
        self.assertEqual(couple_obtenus, [('Bradbury' ,1953), ('Huxley', 1932), ('Orwell', 1949), ('Orwell', 1945)])

    # 2. TEST DE NON-MODIFICATION DE LA LISTE ORIGINALE
    def test_non_modification_catalogue(self):
        """Vérifie que la liste d'origine n'est pas modifiée par un tri."""
        titres_initiaux = [livre.titre for livre in self.catalogue_test]
        
        f.trier_par_auteur_puis_annee_recente(self.catalogue_test)
        
        titres_apres_tri = [livre.titre for livre in self.catalogue_test]
        self.assertEqual(titres_initiaux, titres_apres_tri)

    #  3. TEST DE STABILITE
    def test_stabilite_du_tri(self):
        """Vérifie que deux livres de la même année conservent leur ordre d'entrée."""
        livre_1 = Livre("info", "Robs", "1111111111111", 100, 2026)
        livre_2 = Livre("chimie", "Robs", "2222222222222", 100, 2026)
        liste_stable = [livre_1, livre_2]
        
        resultat = f.trier_par_auteur_puis_annee_recente(liste_stable)
        
        self.assertEqual(resultat[0].titre, "info")
        self.assertEqual(resultat[1].titre, "chimie")

    # 4. TEST DE DÉDOUBLONNAGE (TAILLE ET ORDRE)
    def test_dedoublonner(self):
        """Vérifie la taille finale après dédoublonnement et la conservation de l'ordre."""
        self.assertEqual(f.compter_distincts(self.catalogue_avec_doublon), 4)
        
        resultat_dedoublonne = f.dedoublonner(self.catalogue_avec_doublon)
        self.assertEqual(len(resultat_dedoublonne), 4)
        self.assertEqual(resultat_dedoublonne[0].titre, "1984")

    # 5. TEST DE REGROUPEMENT (CLÉS ET TAILLES DES GROUPES)
    def test_regroupement_par_auteur(self):
        """Vérifie les clés présentes dans le dictionnaire et la taille des groupes."""
        dictionnaire_groupes = f.regrouper_par_auteur(self.catalogue_test)
        
        self.assertIn("Orwell", dictionnaire_groupes)
        self.assertIn("Huxley", dictionnaire_groupes)
        self.assertIn("Bradbury", dictionnaire_groupes)
        
        self.assertEqual(len(dictionnaire_groupes["Orwell"]), 2)
        self.assertEqual(len(dictionnaire_groupes["Huxley"]), 1)

if __name__ == '__main__':
    unittest.main()
