package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;

import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
import org.junit.jupiter.api.Test;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.context.annotation.Configuration;

class LdapPropertiesTest {

  @Configuration
  @EnableConfigurationProperties(LdapProperties.class)
  static class Config {}

  @Test
  void bindsSettingsAndBuildsLdapUrl() {
    new ApplicationContextRunner()
        .withUserConfiguration(Config.class)
        .withPropertyValues(
            "sadgeo.auth.ldap.protocol=ldap",
            "sadgeo.auth.ldap.host=ad.example.org",
            "sadgeo.auth.ldap.port=389",
            "sadgeo.auth.ldap.domain=example.org",
            "sadgeo.auth.ldap.base-dn=DC=example,DC=org",
            "sadgeo.auth.ldap.connect-timeout-ms=2500",
            "sadgeo.auth.ldap.read-timeout-ms=6000")
        .run(context -> {
          var settings = context.getBean(LdapProperties.class);

          assertDoesNotThrow(settings::validate);

          assertTrue(settings.isConfigured());
          assertEquals("ldap", settings.getProtocol());
          assertEquals("ad.example.org", settings.getHost());
          assertEquals(389, settings.getPort());
          assertEquals("example.org", settings.getDomain());
          assertEquals("DC=example,DC=org", settings.getBaseDn());
          assertEquals("ldap://ad.example.org:389", settings.effectiveUrl());
        });
  }

  @Test
  void preservesExistingUrlOverride() {
    var p = new LdapProperties();

    p.setProtocol("ldaps");
    p.setUrl("ldaps://legacy.example.org:636");
    p.setDomain("example.org");

    assertDoesNotThrow(p::validate);

    assertEquals(
        "ldaps://legacy.example.org:636",
        p.effectiveUrl());
  }

  @Test
  void requiresProtocolHostPortAndDomain() {
    var p = new LdapProperties();

    assertThrows(
        IllegalArgumentException.class,
        p::validate);

    p.setProtocol("ldap");

    assertThrows(
        IllegalArgumentException.class,
        p::validate);

    p.setHost("ad.example.org");

    assertThrows(
        IllegalArgumentException.class,
        p::validate);

    p.setDomain("example.org");

    assertThrows(
        IllegalArgumentException.class,
        p::validate);

    p.setPort(389);

    assertDoesNotThrow(
        p::validate);
  }

  @Test
  void rejectsInvalidProtocol() {
    var p = new LdapProperties();

    p.setProtocol("ftp");
    p.setHost("ad.example.org");
    p.setPort(389);
    p.setDomain("example.org");

    assertThrows(
        IllegalArgumentException.class,
        p::validate);
  }

  @Test
  void acceptsLdapUrlOverride() {
    var p = new LdapProperties();

    p.setProtocol("ldap");
    p.setDomain("example.org");
    p.setUrl("ldap://ad.example.org:389");

    assertDoesNotThrow(
        p::validate);

    assertEquals(
        "ldap://ad.example.org:389",
        p.effectiveUrl());
  }
}