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

- [ ] finegrained the acces rules with the json file using labels and keycloack -> Pyhton script?
- [ ] connect the group off all users with AzureAD using Keycloack
- [ ] test manage users from admin -> keycloack built in?
- [ ] configure a pod for K8s/Openshift -> test with Minikube
- [ ] build a CI/CD pipeline -> Gitlab
- [ ] configure HTTPS -> Nginx, Docker-Compose, DNS

### compréhension:

- Keycloack permet de gérer les droits d'accès informatique selon le concept de `realms`. Une realm définie le cadre à gérer. Dans chaque cadre, on peut avoir des `realm roles` qui déterminent les rôles du cadre. Un rôle peut être un administrateur comme un usager normal, une identité qui a du sens dans le cadre en question. 
  
- On défini l'interface du keycloack par les `clients` qui stipulent quels accès ont besoin d'authentification avec quelles `policies`. Les policies sont des restrictions que l'on applique. Avec tous les accès pour passer les restrictions, on est octroyé l'autorisation d'accès en échange d'un `token`, un code, qui est valide pour une `session`, une durée inscrite dans un cadre. On défini des `client scopes` qui sont partagés entre divers clients pour déterminer les protocols à appliquer. Ceux-ci composent les policies.



