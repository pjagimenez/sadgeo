FROM image-registry.openshift-image-registry.svc:5000/openshift/ubi9-openjdk-17:1.24

COPY *.jar /deployments/app.jar

EXPOSE 8080

CMD ["java","-jar","/deployments/app.jar"]