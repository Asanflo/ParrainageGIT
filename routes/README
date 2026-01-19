# Documentation API - Gestion des Étudiants et Surprises

## 📋 Table des matières
- [Authentification](#authentification)
- [Étudiants (Students)](#étudiants-students)
- [Surprises](#surprises)

---

## 🔐 Authentification

### POST `/api/auth/login`
**Connexion d'un étudiant avec matricule et mot de passe.**

#### Headers
```
Content-Type: application/json
```

#### Corps de la requête
```json
{
  "matricule": "2026A001",
  "password": "motdepasse123"
}
```

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `matricule` | string | ✅ Oui | Matricule unique de l'étudiant |
| `password` | string | ✅ Oui | Mot de passe de l'étudiant |

#### Réponses

**✅ 200 OK** - Authentification réussie
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJh...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJh...",
  "student_name": "Florentin Agassem"
}
```

**❌ 401 Unauthorized** - Identifiants invalides
```json
{
  "msg": "Identifiants invalides"
}
```

---

### POST `/api/auth/refresh`
**Rafraîchit le token d'accès à partir d'un refresh token valide.**

#### Headers
```
Authorization: Bearer <refresh_token>
Content-Type: application/json
```

#### Conditions
- Un refresh token valide doit être fourni dans l'en-tête Authorization

#### Réponses

**✅ 200 OK** - Nouveau token généré
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

**❌ 401 Unauthorized** - Token invalide ou expiré
```json
{
  "msg": "Token invalide ou expiré"
}
```

---

## 👨‍🎓 Étudiants (Students)

### POST `/api/student/`
**Crée un nouvel étudiant dans le système.**

#### Headers
```
Content-Type: application/json
```

#### Corps de la requête
```json
{
  "matricule": "24IN01",
  "nom_complet": "Jean Dupont",
  "niveau": 3,
  "filiere": "GLO",
  "telephone": "699123456",
  "competences": ["Python", "Flask", "SQL"],
  "centres_interet": ["Backend", "Sécurité"],
  "reseaux_sociaux": {
    "linkedin": "https://linkedin.com/in/jeandupont",
    "github": "https://github.com/jeandupont"
  }
}
```

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `matricule` | string | ✅ Oui | Matricule unique (max 15 caractères) |
| `nom_complet` | string | ✅ Oui | Nom complet de l'étudiant (max 255 caractères) |
| `niveau` | integer | ✅ Oui | Niveau d'études (1-5) |
| `filiere` | string | ✅ Oui | Filière d'études (max 50 caractères) |
| `telephone` | string | ❌ Non | Numéro de téléphone (max 20 caractères) |
| `competences` | array[string] | ❌ Non | Liste des compétences techniques |
| `centres_interet` | array[string] | ❌ Non | Liste des centres d'intérêt |
| `reseaux_sociaux` | object | ❌ Non | Liens vers les réseaux sociaux (linkedin, github, etc.) |

#### Conditions
- Le matricule doit être unique dans le système
- Les champs `matricule`, `nom_complet` et `niveau` sont obligatoires

#### Réponses

**✅ 201 Created** - Étudiant créé avec succès
```json
{
  "msg": "Student créé",
  "student": {
    "id": 13,
    "matricule": "24IN01",
    "nom_complet": "Jean Dupont",
    "niveau": 3,
    "filiere": "GLO",
    "telephone": "699123456",
    "competences": ["Python", "Flask", "SQL"],
    "centres_interet": ["Backend", "Sécurité"],
    "reseaux_sociaux": {
      "linkedin": "https://linkedin.com/in/jeandupont",
      "github": "https://github.com/jeandupont"
    },
    "photo_profil": null,
    "created_at": "2026-01-17T11:56:38",
    "updated_at": "2026-01-17T11:56:38"
  }
}
```

**❌ 400 Bad Request** - Champs obligatoires manquants
```json
{
  "msg": "matricule, nom et niveau requis"
}
```

**❌ 400 Bad Request** - Matricule déjà existant
```json
{
  "msg": "matricule déjà existant"
}
```

#### Notes
- Un token et un mot de passe sont générés automatiquement pour l'étudiant
- Le mot de passe initial correspond au token généré

---

### GET `/api/student/me`
**Récupère les informations de l'étudiant actuellement connecté via JWT.**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)

#### Réponses

**✅ 200 OK** - Informations de l'étudiant
```json
{
  "student": {
    "id": 1,
    "matricule": "2026A001",
    "nom_complet": "Florentin Agassem",
    "niveau": 3,
    "filiere": "Informatique",
    "telephone": "+237690000000",
    "competences": ["Python", "SQL"],
    "centres_interet": ["AI", "Web"],
    "reseaux_sociaux": {
      "linkedin": "https://linkedin.com/in/florentin"
    },
    "photo_profil": null,
    "created_at": "2026-01-17T10:00:00",
    "updated_at": "2026-01-17T10:00:00"
  }
}
```

**❌ 401 Unauthorized** - JWT manquant ou invalide
```json
{
  "msg": "Missing Authorization Header"
}
```

**❌ 404 Not Found** - Étudiant non trouvé
```json
{
  "msg": "404 Not Found: The requested resource was not found"
}
```

---

### GET `/api/student/`
**Retourne la liste complète des étudiants.**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)

#### Réponses

**✅ 200 OK** - Liste des étudiants
```json
[
  {
    "id": 1,
    "matricule": "2026A001",
    "nom_complet": "Florentin Agassem",
    "niveau": 3,
    "filiere": "Informatique",
    "telephone": "+237690000000",
    "competences": ["Python", "SQL"],
    "centres_interet": ["AI", "Web"],
    "reseaux_sociaux": {
      "linkedin": "https://linkedin.com/in/florentin"
    },
    "photo_profil": null,
    "created_at": "2026-01-17T10:00:00",
    "updated_at": "2026-01-17T10:00:00"
  },
  {
    "id": 2,
    "matricule": "2026A002",
    "nom_complet": "Marie Durant",
    "niveau": 4,
    "filiere": "GLO",
    "telephone": "+237699999999",
    "competences": ["Java", "Spring"],
    "centres_interet": ["Backend"],
    "reseaux_sociaux": {},
    "photo_profil": null,
    "created_at": "2026-01-17T10:30:00",
    "updated_at": "2026-01-17T10:30:00"
  }
]
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

---

### PUT `/api/student/<int:student_id>`
**Met à jour certaines informations de l'étudiant.**

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Paramètres d'URL

| Paramètre | Type | Description |
|-----------|------|-------------|
| `student_id` | integer | ID de l'étudiant à modifier |

#### Corps de la requête
```json
{
  "telephone": "+237690000001",
  "photo_profil": "https://example.com/photo.jpg",
  "competences": ["Python", "Django", "React"],
  "centres_interet": ["Web", "Blockchain"],
  "reseaux_sociaux": {
    "linkedin": "https://linkedin.com/in/florentin",
    "twitter": "https://twitter.com/florentin"
  }
}
```

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `telephone` | string | ❌ Non | Nouveau numéro de téléphone |
| `photo_profil` | string | ❌ Non | URL de la photo de profil |
| `competences` | array[string] | ❌ Non | Liste mise à jour des compétences |
| `centres_interet` | array[string] | ❌ Non | Liste mise à jour des centres d'intérêt |
| `reseaux_sociaux` | object | ❌ Non | Liens mis à jour vers les réseaux sociaux |

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)
- Seuls les champs fournis seront modifiés
- Les champs `matricule`, `nom_complet`, `niveau` et `filiere` ne peuvent pas être modifiés

#### Réponses

**✅ 200 OK** - Étudiant mis à jour
```json
{
  "msg": "Student mis à jour",
  "student": {
    "id": 1,
    "matricule": "2026A001",
    "nom_complet": "Florentin Agassem",
    "niveau": 3,
    "filiere": "Informatique",
    "telephone": "+237690000001",
    "competences": ["Python", "Django", "React"],
    "centres_interet": ["Web", "Blockchain"],
    "reseaux_sociaux": {
      "linkedin": "https://linkedin.com/in/florentin",
      "twitter": "https://twitter.com/florentin"
    },
    "photo_profil": "https://example.com/photo.jpg",
    "created_at": "2026-01-17T10:00:00",
    "updated_at": "2026-01-17T12:00:00"
  }
}
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

**❌ 404 Not Found** - Étudiant non trouvé

---

### DELETE `/api/student/<int:student_id>`
**Supprime un étudiant de la base de données.**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Paramètres d'URL

| Paramètre | Type | Description |
|-----------|------|-------------|
| `student_id` | integer | ID de l'étudiant à supprimer |

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)
- La suppression entraînera la suppression en cascade des surprises créées par cet étudiant

#### Réponses

**✅ 200 OK** - Étudiant supprimé
```json
{
  "msg": "Student supprimé"
}
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

**❌ 404 Not Found** - Étudiant non trouvé

---

## 🎁 Surprises

### POST `/api/surprises/`
**Crée une nouvelle surprise pour l'étudiant connecté.**

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Corps de la requête
```json
{
  "titre": "Bienvenue dans le programme",
  "type_media": "TEXTE",
  "contenu": "Félicitations pour ton parcours !"
}
```

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `titre` | string | ✅ Oui | Titre de la surprise (max 100 caractères) |
| `type_media` | string | ✅ Oui | Type de média : `TEXTE`, `GIF`, `IMAGE`, `VIDEO`, `LIEN`, `AUDIO`, `DEFI` |
| `contenu` | string | ✅ Oui | Contenu textuel ou URL du média |

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)
- **L'étudiant connecté doit être de niveau 4** (restriction métier importante)
- Tous les champs (`titre`, `type_media`, `contenu`) sont obligatoires

#### Réponses

**✅ 201 Created** - Surprise créée
```json
{
  "msg": "Surprise créée avec succès",
  "surprise": {
    "id": 1,
    "titre": "Bienvenue dans le programme",
    "type_media": "TEXTE",
    "contenu": "Félicitations pour ton parcours !",
    "mentor_id": 42,
    "date_creation": "2026-01-17T13:00:00"
  }
}
```

**❌ 403 Forbidden** - L'étudiant n'est pas de niveau 4
```json
{
  "msg": "Seuls les étudiants de niveau 4 peuvent créer une surprise"
}
```

**❌ 400 Bad Request** - Champ obligatoire manquant
```json
{
  "msg": "Champ obligatoire manquant : titre"
}
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

---

### GET `/api/surprises/`
**Récupère toutes les surprises créées par l'utilisateur connecté.**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)

#### Réponses

**✅ 200 OK** - Liste des surprises du mentor
```json
[
  {
    "id": 1,
    "titre": "Bienvenue",
    "type_media": "TEXTE",
    "contenu": "Message de bienvenue",
    "mentor_id": 42,
    "date_creation": "2026-01-17T13:00:00"
  },
  {
    "id": 2,
    "titre": "Motivation du jour",
    "type_media": "IMAGE",
    "contenu": "https://example.com/motivation.jpg",
    "mentor_id": 42,
    "date_creation": "2026-01-17T14:00:00"
  }
]
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

**❌ 404 Not Found** - Étudiant non trouvé

#### Notes
- Seules les surprises créées par l'étudiant connecté sont retournées
- Utilise la relation `back_populates` du modèle Student

---

### PUT `/api/surprises/<int:surprise_id>`
**Met à jour une surprise existante.**

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Paramètres d'URL

| Paramètre | Type | Description |
|-----------|------|-------------|
| `surprise_id` | integer | ID de la surprise à modifier |

#### Corps de la requête
```json
{
  "titre": "Nouveau titre",
  "type_media": "VIDEO",
  "contenu": "https://example.com/video.mp4"
}
```

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `titre` | string | ❌ Non | Nouveau titre de la surprise |
| `type_media` | string | ❌ Non | Nouveau type de média |
| `contenu` | string | ❌ Non | Nouveau contenu |

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)
- **L'étudiant connecté doit être de niveau 4**
- Seuls les champs fournis seront modifiés

#### Réponses

**✅ 200 OK** - Surprise mise à jour
```json
{
  "msg": "Surprise mise à jour",
  "surprise": {
    "id": 1,
    "titre": "Nouveau titre",
    "type_media": "VIDEO",
    "contenu": "https://example.com/video.mp4",
    "mentor_id": 42,
    "date_creation": "2026-01-17T13:00:00"
  }
}
```

**❌ 403 Forbidden** - L'étudiant n'est pas de niveau 4
```json
{
  "msg": "Seuls les étudiants de niveau 4 peuvent modifier une surprise"
}
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

**❌ 404 Not Found** - Surprise non trouvée

---

### DELETE `/api/surprises/<int:surprise_id>`
**Supprime une surprise.**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Paramètres d'URL

| Paramètre | Type | Description |
|-----------|------|-------------|
| `surprise_id` | integer | ID de la surprise à supprimer |

#### Conditions
- L'utilisateur doit être authentifié (JWT valide requis)
- **L'étudiant connecté doit être de niveau 4**

#### Réponses

**✅ 200 OK** - Surprise supprimée
```json
{
  "msg": "Surprise supprimée avec succès"
}
```

**❌ 403 Forbidden** - L'étudiant n'est pas de niveau 4
```json
{
  "msg": "Seuls les étudiants de niveau 4 peuvent supprimer une surprise"
}
```

**❌ 401 Unauthorized** - JWT manquant ou invalide

**❌ 404 Not Found** - Surprise non trouvée

**❌ 500 Internal Server Error** - Erreur serveur
```json
{
  "msg": "Message d'erreur détaillé"
}
```

---

## 📝 Notes Importantes

### Authentification
- Tous les endpoints (sauf `/api/auth/login` et `/api/student/` POST) nécessitent un JWT valide
- Le JWT doit être envoyé dans l'en-tête : `Authorization: Bearer <access_token>`
- Les tokens JWT ont une durée de validité limitée
- Utilisez `/api/auth/refresh` avec le refresh token pour obtenir un nouveau access token

### Restrictions métier
- **Surprises** : Seuls les étudiants de **niveau 4** peuvent créer, modifier ou supprimer des surprises
- **Matricules** : Doivent être uniques dans le système
- **Mot de passe initial** : Généré automatiquement et correspond au token lors de la création d'un étudiant

### Types de média supportés pour les surprises
- `TEXTE` : Contenu textuel simple
- `GIF` : URL vers un GIF animé
- `IMAGE` : URL vers une image
- `VIDEO` : URL vers une vidéo
- `LIEN` : URL générique
- `AUDIO` : URL vers un fichier audio
- `DEFI` : Défi textuel ou URL

### Relations entre modèles
- Un étudiant peut créer plusieurs surprises (relation 1-N)
- Un étudiant peut être mentor de plusieurs autres étudiants
- Un étudiant ne peut avoir qu'un seul mentor (relation 1-1)
- La suppression d'un étudiant entraîne la suppression de ses surprises (cascade)

---

## 🚀 Exemples d'utilisation avec curl

### Créer un étudiant
```bash
curl -X POST http://127.0.0.1:5000/api/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "matricule": "24IN01",
    "nom_complet": "Jean Dupont",
    "niveau": 3,
    "filiere": "GLO",
    "telephone": "699123456"
  }'
```

### Se connecter
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "matricule": "24IN01",
    "password": "token_genere"
  }'
```

### Créer une surprise (nécessite niveau 4)
```bash
curl -X POST http://127.0.0.1:5000/api/surprises/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Bienvenue !",
    "type_media": "TEXTE",
    "contenu": "Message de bienvenue"
  }'
```

### Récupérer mes informations
```bash
curl -X GET http://127.0.0.1:5000/api/student/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```