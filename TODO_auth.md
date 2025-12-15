# TODO - Service d'Authentification

### 🛠️ Phase 1 : Initialisation & Infrastructure

* [ ] **Choix de la technologie** : Choisir une techno différente de celle des autres services (ex: si *Films* est en Python, faire celui-ci en **Node.js/Express**, **Go**, ou **Java Spring Security**).
* [ ] **Structure du projet** : Initialiser le dossier, le `package.json` (ou équivalent), et le linter.
* [ ] **Configuration de l'environnement** : Créer un fichier `.env` pour stocker les secrets.
    * *Important :* Ne jamais commiter ce fichier sur Git.
    * Variables requises : `PORT`, `DB_URL`, `JWT_SECRET` (clé de cryptage).
* [ ] **Connexion Base de Données** : Configurer la connexion (PostgreSQL, MySQL ou MongoDB) spécifique à ce service.

### 💾 Phase 2 : Modélisation des Données (BDD)

* [ ] **Création du schéma `User`** :
    * `id` (Unique, Primary Key).
    * `email` (Unique, Indexé).
    * `password` (Type String, pour stocker le **Hash**, jamais le mot de passe clair).
    * `role` (String ou Enum : 'USER', 'ADMIN').
    * `type_tarif` (Pour le bonus : 'ETUDIANT', 'CHOMEUR', 'STANDARD').
    * `created_at`.

### 🔐 Phase 3 : Logique de Sécurité (Cœur du système)

* [ ] **Hachage des mots de passe** :
    * Installer une librairie de hachage (ex: `bcrypt` ou `argon2`).
    * Créer une fonction utilitaire pour hacher un mot de passe à l'inscription.
    * Créer une fonction pour comparer un mot de passe clair avec un hash lors du login.
* [ ] **Gestion des Tokens (JWT)** :
    * Installer une librairie JWT (ex: `jsonwebtoken`).
    * Créer une fonction pour **générer** un token contenant l'ID de l'user et son Rôle.
    * Définir une durée de vie du token (ex: 1 heure).

### 📡 Phase 4 : Développement des Endpoints (API)

#### 1. Inscription (`POST /auth/register`)
* [ ] Valider les données reçues (Email valide ? Mot de passe assez fort ?).
* [ ] Vérifier si l'email existe déjà en BDD (Renvoyer erreur 409 si oui).
* [ ] Hacher le mot de passe.
* [ ] Sauvegarder l'utilisateur.
* [ ] Renvoyer un succès (201 Created).

#### 2. Connexion (`POST /auth/login`)
* [ ] Chercher l'utilisateur par email.
* [ ] Si non trouvé -> Erreur (401 Unauthorized).
* [ ] Si trouvé -> Comparer le mot de passe hashé.
* [ ] Si mot de passe incorrect -> Erreur (401).
* [ ] Si tout est bon -> Générer le Token JWT.
* [ ] Renvoyer le token au client.

#### 3. Profil (`GET /auth/me`)
* [ ] Créer un **Middleware d'authentification** :
    * Il doit intercepter la requête.
    * Vérifier la présence du Header `Authorization: Bearer <token>`.
    * Vérifier la signature du Token avec la `JWT_SECRET`.
* [ ] Décoder le token pour récupérer l'ID utilisateur.
* [ ] Chercher l'utilisateur en BDD.
* [ ] Renvoyer les infos (sans le mot de passe !).

### ⚖️ Phase 5 : Conformité & Bonus (Aspect Légal)
*Conformément à nos consignes sur la loi :*
* [ ] **RGPD / CNIL** : S'assurer que tu ne stockes que les données nécessaires.
* [ ] Ajouter une mention ou une case à cocher (côté front) pour le consentement.
* [ ] *(Bonus)* **OAuth** : Ajouter un bouton "Se connecter avec Google/GitHub" (nécessite d'utiliser Passport.js ou Auth0).

### 🐳 Phase 6 : Déploiement

* [ ] **Dockerfile** : Créer l'image du service.
* [ ] **Docker-compose** : L'ajouter à la stack générale avec sa propre base de données.

---

### Résumé des Endpoints à fournir aux autres membres du groupe :

| Méthode | URL         | Description                                                 | Body requis               |
| :------ | :---------- | :---------------------------------------------------------- | :------------------------ |
| `POST`  | `/register` | Créer un compte                                             | `{email, password, type}` |
| `POST`  | `/login`    | Se connecter                                                | `{email, password}`       |
| `GET`   | `/me`       | Qui suis-je ?                                               | Header `Authorization`    |
| `POST`  | `/validate` | (Optionnel) Pour que les autres services vérifient le token | `{token}`                 |

PS : Merci Gemini