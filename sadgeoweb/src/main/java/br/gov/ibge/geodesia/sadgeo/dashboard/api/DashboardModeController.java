package br.gov.ibge.geodesia.sadgeo.dashboard.api;
import org.springframework.core.env.Environment;
import org.springframework.core.env.Profiles;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
@RestController
public class DashboardModeController {
    private final Environment environment;
    public DashboardModeController(Environment environment) { this.environment = environment; }
    @GetMapping("/api/dashboard/config") public Map<String, Object> config() {
        return Map.of("demo", environment.acceptsProfiles(Profiles.of("demo")), "version", "0.1.0");
    }
}
