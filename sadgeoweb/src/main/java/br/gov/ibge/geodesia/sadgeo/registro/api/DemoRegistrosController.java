package br.gov.ibge.geodesia.sadgeo.registro.api;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.*;
import java.io.IOException;
import java.util.*;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.web.bind.annotation.*;

@RestController
@Profile("demo")
@RequestMapping("/api/registros")
public class DemoRegistrosController {
  private final List<Map<String, Object>> rows;

  public DemoRegistrosController(ObjectMapper mapper) throws IOException {
    try (var in = new ClassPathResource("demo/dashboard.json").getInputStream()) {
      rows = mapper.convertValue(mapper.readTree(in).get("fatos"), new TypeReference<>() {});
    }
  }

  @GetMapping("/{context}")
  public Map<String, Object> list(
      @PathVariable String context,
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "25") int size,
      @RequestParam(defaultValue = "") String q,
      @RequestParam(defaultValue = "") String projeto) {
    RegistroContexts.page(page, size);
    String campanha = RegistroContexts.campanha(context);
    var filtered =
        rows.stream()
            .filter(r -> campanha == null || campanha.equals(r.get("campanha")))
            .filter(r -> projeto.isBlank() || projeto.equals(r.get("projeto")))
            .filter(
                r ->
                    q.isBlank()
                        || r.values().stream()
                            .anyMatch(
                                v ->
                                    String.valueOf(v)
                                        .toLowerCase(Locale.ROOT)
                                        .contains(q.toLowerCase(Locale.ROOT))))
            .sorted(Comparator.comparing(r -> String.valueOf(r.get("seq"))))
            .toList();
    return Map.of(
        "items",
        filtered.stream().skip((long) page * size).limit(size).toList(),
        "page",
        page,
        "size",
        size,
        "total",
        filtered.size(),
        "totalPages",
        (filtered.size() + size - 1) / size,
        "campanha",
        campanha == null ? "" : campanha);
  }
}
