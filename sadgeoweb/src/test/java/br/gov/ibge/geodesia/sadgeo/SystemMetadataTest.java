package br.gov.ibge.geodesia.sadgeo;

import java.time.Instant;
import org.junit.jupiter.api.Test;
import org.springframework.boot.info.BuildProperties;
import org.springframework.mock.env.MockEnvironment;
import br.gov.ibge.geodesia.sadgeo.common.component.AppVersaoProvider;
import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
import br.gov.ibge.geodesia.sadgeo.dashboard.api.DashboardModeController;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class SystemMetadataTest {
    @Test void footerUsesBuildTimeServerHostAndProfileLabel() {
        var build = mock(BuildProperties.class);
        when(build.getTime()).thenReturn(Instant.parse("2026-10-19T19:00:00Z"));
        var version = new AppVersaoProvider(build);
        var env = new MockEnvironment().withProperty("HOSTNAME", "sadgeo-pod-123");
        env.setActiveProfiles("prod");
        var controller = new DashboardModeController(env, new LdapProperties(), version);
        var config = controller.config();
        assertEquals("0.1.20261019-16",config.get("version"));
        assertEquals(config.get("version"),controller.config().get("version"));
        assertEquals("sadgeo-pod-123",config.get("hostname"));
        assertEquals("prod",config.get("profile"));
        assertEquals("Produção",config.get("profileLabel"));
        env.setProperty("sadgeo.profile-label", "Homologação");
        assertEquals("Homologação",controller.config().get("profileLabel"));
    }
}
