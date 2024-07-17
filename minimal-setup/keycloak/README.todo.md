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

- [x] ajouter un utilisateur manuellement [voir procédure ici](./manual-integration/README.add-role.md)
- [ ] tester avec un utilisateur sur une Azure -> insérer les credentials (avoir une config automatique -> variable d'env)
- [ ] ajouter les labels automatiquement
- [ ] gérer les accès dans Keycloack automatiquement
- [ ] users by group in Keycloack

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
  
- Pour les clients on peut également leur attribuer des rôles: `Realm Management` (pour la gestion des accès globale), `Broker` (pour les partis tierces de connection), `Account` (pour que l'utilisateur personnalise son propre compte). Dans notre cas, on peut attribuer un accès spécifique au `admin-cli` pour permettre l'accès par ligne de commande via l'API de orthanc-auth-service.

- Pour gérer les accès aux clients, on défini des `users`, des usagers et des `groups`, groupes dans lesquels les usagers peuvent s'inscrire pour leur associer des droits d'accès. Les usagers d'un groupe hérite des droits d'accès du groupe.
 
- Dans un monde où tous les usagers ont tous les accès, l'intégrité de l'application est compromise, car un utilisateur régulier pourrait voler de l'information, bloquer les accès à l'application. Même, de l'information sensible pourrait être exposée à un usager qui ne devrait pas les voir, ce qui est un bris éthique pour des usagers non consentant. C'est d'autant plus important dans un contexte hospitalier où les images médicales sont de nature confidentielle.
  
- Pour palier à un ce problème, une stratégie commune est de donner le moins de droits d'accès possible à un usager et de toujours associer des droits d'accès par groupe. En effet, un groupe peut regrouper plusieurs usagers et est facile à maintenir. Avec seulement les accès nécessaires, il n'est pas possible d'accéder à de l'information restreinte autrement en plus de limiter les actions possible d'effectuer. 
  
-  De plus, il est courant d'associer plus d'un groupe à un usager pour partager les droits. La raison est qu'il est fastidieux de gérer des accès individuel, car lors d'une mise à jour de sécurité, il faudrait s'assurer que chaque individu a toujours les bons droits, ce qui est une mauvaise pratique. À la place, mettre à jour le groupe, voir retirer un usager d'un groupe ou ajouter un groupe permet de gérer les accès plus efficacement et sécuritairement. 
  
-  En termes d'organisation des groupes, lorsque les groupes suivent la structure de l'organisation, on facilite une compréhension globale et un contrôle intellectuel sur la gestion de la sécurité. Il serait étrange de vouloir définir un groupe par rapport à sa fonction, car la fonction change. Or, l'appartenance à un groupe elle est flexible et permet une compréhension facile, car on peut changer les accès sans pour autant changer le nom du groupe et le groupe remplie une fonction, ce qui est intuitif. Dans une organisation, il est plus courant d'être jumelé dans une équipe avec des droits pour réaliser la fonction de l'équipe. Bref, l'organisation des groupes selon la struture de l'organisation est plus compréhensive.
  
- On peut comprendre maintenant comment les accès pourraient être gérés dans Orthanc, mais plus spécifiquement à Orthanc, les accès sont gérés par authentification. Cependant, l'authentification est globale, lorsque l'on a accès au serveur Orthanc, ce qui donne tous les accès à tous ceux qui se connectent sur le serveur. Pour pallier à cela, `Orthanc-Team`, l'équipe qui gère Orthanc, à développé un plugin, une extension, pour pouvoir gérer les accès par utilisateur avec `Keycloack`, `Orthanc-Auth-Service` et `Nginx`. L'astuce qu'ils ont employés, c'est d'utiliser les `labels`, les étiquettes sur les studies pour contrôler l'accès et de passer une configuration .json au service d'authentification de orthanc. 

- stratégie: ajouter une study comme admin sans label, c'est-à-dire avec aucun accès pour les autres sans authorisation (on ne veut pas que se soit un non admin qui téléverse, sinon on pourrait téléverser des fichiers indésirables sans les authorisations). Si c'est une machine, on doit faire une demande pour un token comme un utilisateur normal ou l'isoler dans un réseau privé. La différence, c'est qu'un mécanisme automatique est mis en place pour assurer l'authentification si la session est terminée. Dans Orthanc, si on a les droits, on peut ajouter une étiquette à la study avec un label spécifique pour donner accès à un groupe d'utilisateurs en fonction de leur rôle. Conséquemment, le label devient la représentation du rôle. Si les accès sont définis d'avance et stable, on peut les changer manuellement dans l'interface ou par un script. Toutefois, les rôles peuvent changer et associer des labels aux utilisateurs en fonction du rôle de manière automatique est nécessaire. La raison: quand on modifie un rôle, qu'on ajoute un rôle ou qu'on retire un rôle, on doit modifier les labels associés aux utilisateurs qui ont ce rôle. Sinon, on pourrait se retrouver avec des utilisateurs qui manquent des accès ou des utilisateurs qui ont des accès alors qu'ils ne devraient pas les avoir. 

- La question qui se pose: comment-est ce qu'on gère l'attribution des labels automatiquement? Il faut prendre en compte que l'on peut avoir plusieurs labels pour un même utilisateur, car un utilisateur peut remplir plusieurs rôles à la fois. Aussi, les utilisateurs ont des rôles dynamqiques à travers le temps, leurs rôles peuvent changer. Également, le rôle en tant que tel peut changer, c'est-à-dire que le nom du rôle et les authorisations peuvent changer. Plusieurs rôles peuvent être associés à des règles contradictoires quant aux authorisations par rapport aux studies si les studies sont jumellés ensemble pour un même utilisateur avec un ou plusieurs labels différents.
  
- Par exemple: si un utilisateur est attribué le rôle à la fois d'externe et de docteur, il peut voir toutes les studies associé à chacun des labels permis par ce rôle, les règles sont différentes pour chacunes des studies. Si la study pour le rôle d'externe est partagée, il n'y a pas de problème, car tous les utilisateurs peuvent voir les studies d'externe. Par contre, ce n'est pas vrai pour les studies de docteur. Il ne devrait pas pouvoir les partager sans précaution, car ces études ont à priori des informations sensibles. Ces données ne doivent pas être partagées.

- Donc, lorsque l'on retire un label, il faut également retirer des accès pour potentillement plusieurs usagers, ce qui implique qu'il faut un rôle avec plus d'accès pour pouvoir modifier, retirer un label. Pour assurer l'unicité de la transaction, il faut mettre un mécanisme en place de verrou pour éviter une transaction indésirable. Dans le cas d'un étât impossible, on rejette la requête. Par exmple, retirer un label externe pendant qu'un utilisateur docteur avec une study de label externe retire l'accès externe de la study, un utilisateur doit immédiatement ne plus avoir la possibilitée de donner les accès. Un verrou permettrait d'éviter efficacement la concurrence. 

- Bref, une study avec aucun label n'est accessible qu'à un utilisateur avec tous les droits. Retirer les labels d'une study peut être fait uniquement par un utilisateur qui a les droits de modifications pour tous les labels de la study. Le droit de modification des labels d'une study est un rôle prévilégié. 



  
- Un protocole `JWT` est utilisé pour les codes qui sont des fichiers .json encryptés essentiellement qui ajoutent de l'information par rapport au code token qui sera utilisé par le Orthanc-Auth service. Keycloack agit comme un `middleware`, une couche d'authentification intermédiaire entre Orthanc auth service et Keycloack. Il gère essentiellement l'authentification des usagers et les rôles que l'on peut attribuer. L'accès est servi par un `reverse-proxy`, un proxy inversé qui gère les requettes HTTP et HTTPS pour servir l'application web sur la couche applicative à l'aide de fichiers statiques ou d'appels API. Un `certibot`, un robot de renouvellement de certificats est utilisé pour palier à l'expiration des certificats gérant le `TLS`, la couche de transport sécurisée que Nginx gère. Essentiellement, Nginx va distribuer les appels vers Orthanc-Auth, l'API d'Orthanc, l'interface Web de Orthanc et Keycloack.

- Le projet est axé sur l'apect `backend`, la partie en arrière-plan de l'application avec un `fork`, une base du régistre de code distribué open-source du Orthanc-Auth-Service. On souhaite y intégrer le `Azure AD`, le service de régistre des utilisateurs Microsoft utilisé par l'Université Laval, un contrôle des accès par groupe, l'authentification HTTPS et le déploiement de l'application sur `Kubernetes` à l'aide d'un pipeline `CI/CD`, pour le déploiement et l'intégration en continue. 
  
- Dans le futur, ces services d'authentification pourront s'intégrer avec le job manager et faire une gestion par le concept d'albums qui regroupent des `studies`, des études, entre-elles moyennant une interface intéractive qui pourrait s'intégrer à l'extension version 2 de l'interface de Orthanc ou en utilisant une nouvelle interface plus intuitive.
# Stratégie

## permissions
```
all
view
download
delete
send
modify
anonymize
upload
q-r-remote-modalities
settings
api-view
share
```

## labels et permissions
- externe (par défault) -> `accès à Orthanc seulement`
- admin -> `all`
- superuser (au-dessus de admin) -> `compte de secours` (nice to have)
- {nom-projet} -> lecture données d'un projet -> `view`
- on veut garder le configuration permissions.json de orthanc-auth-service manuelle pour l'instant (nice to have automatique)
- on veut que les labels soient assignées de manière automatique pour un utilisateur qui gère le projet {nom-projet},
- une study peut faire partie de plusieurs projets
- ${nom-projet}
- ${nom-groupe-recherche}
- extern

## rôles et groupes à assigner

- On associe un Users à un Group sur Keycloack lorsque possible, puis par Users uniquement si impossible
- Un User peut faire partie de plusieurs groupes 
- Pyramide des droits: (ascendant du moins de droits à celui ayant tous les droits)
    1. Group extern (par défault) -> `accès à Orthanc seulement`
    2. Group {nom-groupe-recherche} -> (ex: GRPM, IUCPQ) regroupe des projets -> `view (sur les données du groupe)`
    3. Group {nom-projet} -> lecture données d'un projet -> `view`
    4. Group {nom-projet}-manager -> gérer le projet -> `send, download, modify, upload, share, delete le label du {nom-projet} -> (sur les données du projet)`
    5. Group {nom-groupe-recherche}-manager -> gérer tous les projets du groupe -> `send, download, modify, upload, share, delete le label du {nom-projet} -> (sur les données des projets)`
    6. Group admin -> `all`
    7. Role superuser (au-dessus de admin) -> `compte de secours` (nice to have)

## structure d'héritage des droits d'accès

[voir le schéma](./auth_pyramid.drawio) : les droits sont divisés selon le diagramme de Venn où les groupes, des ensembles, partagent des droits par intersection. En couleur, on a les groupes qui peuvent modifier les labels des groupes qui sont inscrits à l'intérieur de leurs domaine. Cependant, les groupes de recherche sont une condition supplémentaire pour délimiter les groupes. Un User dans un groupe n'a pas accès aux autres groupes à moins d'y être inscrit. Le user doit être inscrit dans un des groupes qui contient le projet et au projet pour pouvoir y être inscrit. Les cases blanches ont des droits de view uniquement. Les cases de couleur ont des droits d'ajouter, retirer des labels de leur groupe qu'ils fédèrent uniquement (le groupe immédiatement inscrit à l'intérieur). Or, puisqu'un User avec un tel pouvoir hérite de tous les droits inscrits à l'intérieur, subséquement, les groupes en couleur ont le droit de regard jusqu'au projet qui contient un ensemble de studies.

### Illustrons les possibilitées de fédération des accès

 Par exemple, le research-group-manager possède le rôle de manager du research-group. Dans ce groupe de recherche, il y a 3 projets. le projet 1 est sous fédération par le project-manger-1 et les projets 2 et 3 sont sous la fédération du project-manager-2. Le research-group-manager possède le rôle pour modifier les labels qui sont sous la fédération des projects-manager 1 et 2. Donc, il possède les rôles des projects-manager, ce qui implique qu'il peut modifier les labels des projets 1, 2 et 3.

### Illustrons les possibilitées de fédération des accès partagés

 Prenons un autre exemple où un projet est sous la fédération de plusieurs projects manager. Le project-manager 1 et le project-manager 2 ont les droits de modifier le projet 1 sous leur fédération. Le project manager à la possibilité de retirer ses accès et de le donner à un autre project-manager. À défaut qu'il y ait un projet manager qui fédère le projet, le projet est orphelin dans le groupe en attente que le research-group-manager attribue le projet à un project-manager dans le research-group.

### Illustrons les possibilitées où un usager peut se voir attribuer un rôle dans un groupe.

1. externe: il n'a aucun accès appart Orthan vide
2. ${nom-bot}: permettre l'écriture des données sans accès
3. ${nom-projet}: il a accès en lecture à ce projet conditionnel à avoir accès au groupe
4. ${nom-groupe-recherche}: il a accès au groupe
5. ${nom-projet}-manager: il peut modifier les accès à tous les ${nom-projet} associés
6. ${nom-groupe-recherche}-manager: il peut modifier les accès à ${nom-groupe-recherche} ce qui implique tous les projects-manager de ce groupe et tous leurs ${nom-projet}
7. l'admin peut modifier les accès de tout ceux précédemment pour tous les ${nom-groupe-recherche} et a essentiellement presque tous les droits
8. le superuser est un compte de récupération pour l'admin si on veut qui possède les clés de toute l'application

### Illustrons les possibilitées de labels pour des studies et comment on peut y accéder.

1. la study fait partie du projet-1, du groupe-recherche-1, donc elle a les labels projet-1 et groupe-recherche-1.
2. la study fait partie du projet-1 et du projet-2, en plus de faire partie du groupe-recherche, donc elle peut être accédée par le User qui fait partie du groupe-recherche **et** qu'il fait partie du projet-1 **ou** du projet-2
3. la study fait partie du projet-1 qui fait partie du groupe-recherche-1 et groupe-recherche-2, donc un User peut y accéder s'il fait partie du groupe de recherche 1 **ou** du groupe de recherche 2 **et** qu'il fait partie du projet-1

### Illustrons les possibilitées d'un User qui possède un project-manager Role ou un research-group-manager de modifier les accès. Un project manager peut être utile s'il gère une grande quantitée de projets dans un même groupe. Un group manager peut être utile si on veut diviser le groupe en sous-groupes. Peut-être que le groupe admin est suffisant pour une petite organisation.

1. Le project-manager fédère le `projet-1` et le `projet-2`. Il souhaite partager une study qui est disponible dans le `groupe-de-recherche`. Il ajoute un label projet-1 à la study en question. Maintenant au lieu d'avoir le label `groupe-de-recherche` uniquement, il a maintenant `groupe-de-recherche` et `projet-1`. Il ne pourrait pas ajouter `projet-3`, car il ne fédère pas le projet-3. Il ne pourrait pas changer le groupe non plus, car il n'a pas les droits du group-de-recherche-manager qui lui peut ajouter ou retirer le label `groupe-de-recherche` à une study quelconque.
2. Le groupe-de-recherche-manager fédère le `groupe-de-recherche-1` et le `groupe-de-recherche-2`. Le `groupe-de-recherche-2` n'a pas de studies en ce moment étiquettées par ce groupe, il pourrait décider de retirer le `groupe-de-recherche-1` de sa fédération, ce qui rendrait les studies disponibles seulement par le groupe admin (en retirant tous les labels associés au `groupe-de-recherche-1` pour les studies qui en possède). Il pourrait aussi décider d'ajouter un lien symbolique avec le `groupe-de-recherche-2` pour qu'elles soient accessibles par les utilisateurs du `groupe-de-recherche-2`.

### Illustrons les possibilités d'un admin et d'une machine

1. l'admin peut téléverser, télécharger, partager, etc, il possède tous les accès. Il peut également décider de supprimer des studies. Il peut ajouter, retirer les labels et modifier les accès des autres utilisateurs. Il est essentiel pour l'organisation, c'est lui qui a accès à Keycloack finalement. C'est lui qui attribue les rôles.
2. Une machine qui téléverse des données peut être authentifiée comme admin pour pouvoir insérer des données. Cependant, peut-être qu'une telle machine possède trop de droits, il n'est pas toujours nécessaire d'avoir tous les droits pour insérer des données ou encore anonymiser. Il sera nécessaire d'intégrer des machines pour gérer l'anonymisation dans PARADIM. Cette machine est ajoutée dans un groupe `bot` donné avec le droit d'écriture uniquement en plus. Il faut limiter les accès dans les clients pour faire uniquement la tâche par API. On pourrait ajouter un rôle de machine dans ce cas pour permettre un tel accès.



