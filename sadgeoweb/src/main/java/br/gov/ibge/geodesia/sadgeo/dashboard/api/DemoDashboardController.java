package br.gov.ibge.geodesia.sadgeo.dashboard.api;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.io.IOException;

@RestController
@Profile("demo")
@RequestMapping("/api/dashboard")
public class DemoDashboardController {
    private final JsonNode data;
    public DemoDashboardController(ObjectMapper mapper) throws IOException {
        try (var stream = new ClassPathResource("demo/dashboard.json").getInputStream()) {
            data = mapper.readTree(stream);
        }
    }
    @GetMapping("/{section}") public JsonNode section(@PathVariable String section) {
        if (!data.has(section)) throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        return data.get(section);
    }
}
