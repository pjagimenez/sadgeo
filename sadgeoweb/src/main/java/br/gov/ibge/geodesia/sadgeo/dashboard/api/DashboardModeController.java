package br.gov.ibge.geodesia.sadgeo.dashboard.api;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Map;
import org.springframework.core.env.Environment;
import org.springframework.core.env.Profiles;
import org.springframework.web.bind.annotation.*;
import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
import br.gov.ibge.geodesia.sadgeo.common.component.AppVersaoProvider;

@RestController
public class DashboardModeController {
    private final Environment environment;
    private final LdapProperties ldap;
    private final AppVersaoProvider version;
    private final String hostname;

    public DashboardModeController(Environment environment, LdapProperties ldap, AppVersaoProvider version) {
        this.environment = environment; this.ldap = ldap; this.version = version;
        String host = environment.getProperty("HOSTNAME", environment.getProperty("COMPUTERNAME", ""));
        if (host.isBlank()) {
            try { host = InetAddress.getLocalHost().getHostName(); }
            catch (UnknownHostException ex) { host = "indisponível"; }
        }
        this.hostname = host;
    }

    @GetMapping("/api/dashboard/config")
    public Map<String, Object> config() {
        String[] profiles = environment.getActiveProfiles();
        String profile = profiles.length == 0 ? "default" : String.join(", ", profiles);
        String label = switch (profile) {
            case "demo" -> "Demonstração";
            case "dev" -> "Desenvolvimento";
            case "prod" -> "Produção";
            case "test" -> "Testes";
            case "default" -> "Padrão";
            default -> profile;
        };
        return Map.of("demo", environment.acceptsProfiles(Profiles.of("demo")),
            "version", version.getVersion(), "authConfigured", ldap.isConfigured(),
            "profile", profile, "profileLabel", environment.getProperty("sadgeo.profile-label", label),
            "hostname", hostname);
    }
}
