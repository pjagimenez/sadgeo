package br.gov.ibge.geodesia.sadgeo.dashboard.api;
import org.springframework.core.env.Environment;
import org.springframework.core.env.Profiles;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
@RestController
public class DashboardModeController {
    private final Environment environment;
    private final LdapProperties ldap;
    public DashboardModeController(Environment environment, LdapProperties ldap) { this.environment = environment; this.ldap = ldap; }
    @GetMapping("/api/dashboard/config") public Map<String, Object> config() {
        return Map.of("demo", environment.acceptsProfiles(Profiles.of("demo")), "version", "0.1.0",
            "authConfigured", ldap.isConfigured());
    }
}
