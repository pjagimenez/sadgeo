--Criar o BuildConfig
oc new-build  --binary=true  --strategy=docker --name=sadgeo -n dgc-cged-gsd-des

oc get bc -n dgc-cged-gsd-des
oc get is -n dgc-cged-gsd-des

--Gerar o JAR localmente
mvn clean deploy -Pproduction
  - vai criar  o META-INF/build-info.properties
  
  
--Fazer o build da imagem
oc start-build sadgeo --from-dir=target/ocp --follow -n dgc-cged-gsd-des

--Criar Secret Oracle
oc create secret generic sadgeo-db --from-literal=SADGEO_ORACLE_URL="jdbc:oracle:thin:@//oradesent2.ibge.gov.br:1521/pent2" --from-literal=SADGEO_ORACLE_USER="srvSADGEO"   --from-literal=SADGEO_ORACLE_PASSWORD="Gsd!25*MaruD"

--Criar a aplicação
oc new-app sadgeo:latest --name=sadgeo

--Associar as variáveis
--oc set env deployment/sadgeo --from=secret/sadgeo-db
--oc set env dc/sadgeo --from=secret/sadgeo-db
oc set env dc/sadgeo SPRING_PROFILES_ACTIVE=prod
oc set env dc/sadgeo --from=configmap/geodesia-variaveis
oc set env dc/sadgeo --from=secret/bd-srvsadgeo  --prefix=bd_srvsadgeo_


--Expor o serviço
oc expose service sadgeo

oc get route


oc set probe dc/sadgeo  --readiness  --get-url=http://:8080/actuator/health/readiness --initial-delay-seconds=60  --period-seconds=15
oc set probe dc/sadgeo  --liveness   --get-url=http://:8080/actuator/health/liveness  --initial-delay-seconds=120  --period-seconds=30
  
--Recursos recomendados
oc set resources deployment/sadgeo --requests=cpu=500m,memory=2Gi --limits=cpu=2,memory=8Gi

--Verificar o POD
oc get pods


oc logs -f dc/sadgeo


oc rollout latest dc/sadgeo
