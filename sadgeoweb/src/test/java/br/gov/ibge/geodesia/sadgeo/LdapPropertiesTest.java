package br.gov.ibge.geodesia.sadgeo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.context.annotation.Configuration;
import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
import static org.junit.jupiter.api.Assertions.*;

class LdapPropertiesTest {
    @Configuration @EnableConfigurationProperties(LdapProperties.class) static class Config {}
    @Test void bindsIndividualSettingsAndBuildsLdapsUrl() {
        new ApplicationContextRunner().withUserConfiguration(Config.class).withPropertyValues(
            "sadgeo.auth.ldap.host=ad.example.org", "sadgeo.auth.ldap.port=1636",
            "sadgeo.auth.ldap.domain=example.org", "sadgeo.auth.ldap.base-dn=DC=example,DC=org",
            "sadgeo.auth.ldap.connect-timeout-ms=2500", "sadgeo.auth.ldap.read-timeout-ms=6000"
        ).run(context -> {
            var settings = context.getBean(LdapProperties.class);
            settings.validate();
            assertTrue(settings.isConfigured());
            assertEquals("ad.example.org", settings.getHost());
            assertEquals(1636, settings.getPort());
            assertEquals("example.org", settings.getDomain());
            assertEquals("", settings.getUrl());
            assertEquals("ldaps://ad.example.org:1636", settings.effectiveUrl());
            assertEquals("DC=example,DC=org", settings.getBaseDn());
            assertEquals(2500,settings.getConnectTimeoutMs());
            assertEquals(6000,settings.getReadTimeoutMs());
        });
    }
    @Test void preservesExistingUrlOverride() {
        var p=new LdapProperties();p.setUrl("ldaps://legacy.example.org:636");p.setDomain("example.org");
        p.validate();assertEquals("ldaps://legacy.example.org:636",p.effectiveUrl());
    }
    @Test void rejectsPlaintextPartialAndInvalidSettings() {
        var p=new LdapProperties();assertFalse(p.isConfigured());p.validate();
        p.setHost("ad.example.org");assertThrows(IllegalArgumentException.class,p::validate);
        p.setDomain("example.org");p.setPort(0);assertThrows(IllegalArgumentException.class,p::validate);
        p.setPort(636);p.setUrl("ldap://ad.example.org");assertThrows(IllegalArgumentException.class,p::validate);
        p.setUrl("");p.setConnectTimeoutMs(0);assertThrows(IllegalArgumentException.class,p::validate);
    }
}
