# DAM
Dicom Album Manager integration for Orthanc, Paradim

## Big picture

- Postgres Orthanc
- Postgres Keycloack
- OHIF viewer
- Orthanc interface v2 plugin -> modify in the future
- Orthanc Auth: manage acces from keycloack in relation to studies
- Orthanc Keycloack: manage users
- Orthanc Nginx: reverse proxy

- if we want to customize the interface, two options:
  - change the nginx and serve the static files from the custom UI and use the orthanc API (enables more customization, but more work, more maintenance)
  - submit changes to the v2 versions for customization possibilities with the json config (less inital work, less maintenance, less customization, open source compliant)
  
- possible integrations with the ui
  - PARADIM launcher
  - album management (similar to KHEOPS, but with Orthanc reliable infrastructure)

## TODO: backend first

- [x] ajouter un utilisateur manuellement [voir procédure ici](./README.add-role.md)
- [ ] group users roles by group in keycloack
- [ ] tester avec un utilisateur sur une Azure
- [ ] finegrained the acces rules with the json file using labels and keycloack -> Pyhton script?
- [ ] connect the group off all users with AzureAD using Keycloack
- [ ] test manage users from admin -> keycloack built in?
- [ ] configure a pod for K8s/Openshift -> test with Minikube
- [ ] build a CI/CD pipeline -> Gitlab
- [ ] configure HTTPS -> Nginx, Docker-Compose, DNS

### compréhension:

- L'idée c'est de remplacer Kheops. L'Hypothèse c'est qu'un nouveau système pourrait remplacer Kheops, car il serait plus robuste pour faire face aux erreurs fatales dans l'application en production qui rendrent le système indisponible. Sans compter les outils de diagnostics qui sont défficients pour efficacement cerné le problème et les patrons architecturaux trop complexes pour le besoin. En plus, l'application devient de plus en plus lourde à maintenir, car elle n'est plus maintenue par ceux qui la développaient. On compte introduire des technologies à licence ouverte matures et vastement utilisées pour pouvoir relever le défi.

- Parmi ces technologies, Keycloack permet de gérer les droits d'accès informatique selon le concept de `realms`. Une realm définie le cadre à gérer. Dans chaque cadre, on peut avoir des `realm roles` qui déterminent les rôles du cadre. Un rôle peut être un administrateur comme un usager normal, une identité qui a du sens dans le cadre en question. 
 
- On défini l'interface du keycloack par les `clients` qui stipulent quels accès ont besoin d'authentification avec quelles `policies`, les restrictions que l'on applique. Avec tous les accès pour passer les restrictions, on est octroyé l'autorisation d'accès en échange d'un `token`, un code, qui est valide pour une `session`, une durée inscrite dans un cadre. On défini des `client scopes` qui sont partagés entre divers clients pour déterminer les protocoles à appliquer. Ceux-ci composent les policies. On peut également configurer des `events`, des évènements, pour faire la journalisation.

- Pour gérer les accès aux clients, on défini des `users`, des usagers et des `groups`, groupes dans lesquels les usagers peuvent s'inscrire pour leur associer des droits d'accès. Les usagers d'un groupe hérite des droits d'accès du groupe.
 
- Dans un monde où tous les usagers ont tous les accès, l'intégrité de l'application est compromise, car un utilisateur régulier pourrait voler de l'information, bloquer les accès à l'application. Même, de l'information sensible pourrait être exposée à un usager qui ne devrait pas les voir, ce qui est un bris éthique pour des usagers non consentant. C'est d'autant plus important dans un contexte hospitalier où les images médicales sont de nature confidentielle.
  
- Pour palier à un ce problème, une stratégie commune est de donner le moins de droits d'accès possible à un usager et de toujours associer des droits d'accès par groupe. En effet, un groupe peut regrouper plusieurs usagers et est facile à maintenir. Avec seulement les accès nécessaires, il n'est pas possible d'accéder à de l'information restreinte autrement en plus de limiter les actions possible d'effectuer. 
  
-  De plus, il est courant d'associer plus d'un groupe à un usager pour partager les droits. La raison est qu'il est fastidieux de gérer des accès individuel, car lors d'une mise à jour de sécurité, il faudrait s'assurer que chaque individu a toujours les bons droits, ce qui est une mauvaise pratique. À la place, mettre à jour le groupe, voir retirer un usager d'un groupe ou ajouter un groupe permet de gérer les accès plus efficacement et sécuritairement. 
  
-  En termes d'organisation des groupes, lorsque les groupes suivent la structure de l'organisation, on facilite une compréhension globale et un contrôle intellectuel sur la gestion de la sécurité. Il serait étrange de vouloir définir un groupe par rapport à sa fonction, car la fonction change. Or, l'appartenance à un groupe elle est flexible et permet une compréhension facile, car on peut changer les accès sans pour autant changer le nom du groupe et le groupe remplie une fonction, ce qui est intuitif. Dans une organisation, il est plus courant d'être jumelé dans une équipe avec des droits pour réaliser la fonction de l'équipe. Bref, l'organisation des groupes selon la struture de l'organisation est plus compréhensive.
  
- On peut comprendre maintenant comment les accès pourraient être gérés dans Orthanc, mais plus spécifiquement à Orthanc, les accès sont gérés par authentification. Cependant, l'authentification est globale, lorsque l'on a accès au serveur Orthanc, ce qui donne tous les accès à tous ceux qui se connectent sur le serveur. Pour pallier à cela, `Orthanc-Team`, l'équipe qui gère Orthanc, à développé un plugin, une extension, pour pouvoir gérer les accès par utilisateur avec `Keycloack`, `Orthanc-Auth-Service` et `Nginx`. L'astuce qu'ils ont employés, c'est d'utiliser les `labels`, les étiquettes sur les studies pour contrôler l'accès et de passer une configuration .json au service d'authentification de orthanc. 
  
- Un protocole `JWT` est utilisé pour les codes qui sont des fichiers .json encryptés essentiellement qui ajoutent de l'information par rapport au code token qui sera utilisé par le Orthanc-Auth service. Keycloack agit comme un `middleware`, une couche d'authentification intermédiaire entre Orthanc auth service et Keycloack. Il gère essentiellement l'authentification des usagers et les rôles que l'on peut attribuer. L'accès est servi par un `reverse-proxy`, un proxy inversé qui gère les requettes HTTP et HTTPS pour servir l'application web sur la couche applicative à l'aide de fichiers statiques ou d'appels API. Un `certibot`, un robot de renouvellement de certificats est utilisé pour palier à l'expiration des certificats gérant le `TLS`, la couche de transport sécurisée que Nginx gère. Essentiellement, Nginx va distribuer les appels vers Orthanc-Auth, l'API d'Orthanc, l'interface Web de Orthanc et Keycloack.

- Le projet est axé sur l'apect `backend`, la partie en arrière-plan de l'application avec un `fork`, une base du régistre de code distribué open-source du Orthanc-Auth-Service. On souhaite y intégrer le `Azure AD`, le service de régistre des utilisateurs Microsoft utilisé par l'Université Laval, un contrôle des accès par groupe, l'authentification HTTPS et le déploiement de l'application sur `Kubernetes` à l'aide d'un pipeline `CI/CD`, pour le déploiement et l'intégration en continue. 
  
- Dans le futur, ces services d'authentification pourront s'intégrer avec le job manager et faire une gestion par le concept d'albums qui regroupent des `studies`, des études, entre-elles moyennant une interface intéractive qui pourrait s'intégrer à l'extension version 2 de l'interface de Orthanc ou en utilisant une nouvelle interface plus intuitive.


### résumé pour l'affiche

Le projet met l'accent sur une alternative à Kheops quant à la gestion des usagers, pour pallier à sa robustesse insuffisante face aux erreurs fatales en production. Dans Orthanc, l'authentification est globale, ce qui signifie que tous ceux qui ont accès au serveur ont accès à toutes les ressources. Pour résoudre ce problème, l'équipe Orthanc a développé un plugin permettant de gérer les accès par utilisateur en utilisant Keycloak, Orthanc-Auth-Service et Nginx. L'astuce consiste à utiliser des labels sur les études pour contrôler l'accès et à passer une configuration JSON au service d'authentification d'Orthanc.

Un protocole JWT est utilisé pour les codes, qui sont essentiellement des fichiers JSON encryptés ajoutant des informations au token utilisé par le service Orthanc-Auth. Keycloak agit comme un middleware, une couche intermédiaire d'authentification entre le service Orthanc-Auth et Keycloak, gérant l'authentification des utilisateurs et les rôles attribués. L'accès est servi par un reverse-proxy, qui gère les requêtes HTTP et HTTPS pour servir l'application web via des fichiers statiques ou des appels API. Un certibot est utilisé pour renouveler les certificats TLS gérés par Nginx, qui distribue les appels vers Orthanc-Auth, l'API d'Orthanc, l'interface web d'Orthanc et Keycloak.

Le projet se concentre sur le backend, avec un fork du registre de code open-source d'Orthanc-Auth-Service. L'objectif est d'intégrer Azure AD, le service de registre des utilisateurs de Microsoft utilisé par l'Université Laval, pour un contrôle des accès par groupe, l'authentification HTTPS et le déploiement de l'application sur Kubernetes via un pipeline CI/CD pour le déploiement et l'intégration continue.

À l'avenir, ces services d'authentification pourront s'intégrer avec le job manager et gérer les études par le concept d'albums, offrant une interface interactive qui pourrait s'intégrer à l'extension version 2 de l'interface d'Orthanc ou utiliser une nouvelle interface plus intuitive.


