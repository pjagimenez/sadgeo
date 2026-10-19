package br.gov.ibge.geodesia.sadgeo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(
    exclude = org.springframework.boot.autoconfigure.ldap.LdapAutoConfiguration.class)
public class SadgeoApplication {

  public static void main(String[] args) {
    SpringApplication.run(SadgeoApplication.class, args);
  }
}
