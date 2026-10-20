package br.gov.ibge.geodesia.sadgeo.dashboard.service;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.FatoPainelDTO;
import com.fasterxml.jackson.databind.*;
import java.io.IOException;
import java.util.*;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

@Service
@Profile("demo")
public class DemoDashboardFactsQuery implements DashboardFactsQuery {
  private final List<JsonNode> rows;
  private final ObjectMapper mapper;

  public DemoDashboardFactsQuery(ObjectMapper mapper) throws IOException {
    this.mapper = mapper;
    try (var stream = new ClassPathResource("demo/dashboard.json").getInputStream()) {
      rows = new ArrayList<>();
      mapper.readTree(stream).get("fatos").forEach(rows::add);
    }
  }

  private boolean matches(JsonNode row, Filter filter) {
    for (var field : FIELDS.entrySet())
      if (filter.get(field.getKey()) != null
          && !filter.get(field.getKey()).equals(row.path(field.getValue()).asText())) return false;
    String q = filter.get("q");
    return q == null
        || q.isBlank()
        || java.util.stream.Stream.of(
                "seq",
                "campanha",
                "projeto",
                "uf",
                "municipio",
                "uorgOrigem",
                "situacao",
                "tipoLocal")
            .anyMatch(
                field ->
                    row.path(field)
                        .asText()
                        .toLowerCase(Locale.ROOT)
                        .contains(q.toLowerCase(Locale.ROOT)));
  }

  public Result page(Filter filter, int page, int size) {
    var matched =
        rows.stream()
            .filter(row -> matches(row, filter))
            .sorted(
                Comparator.<JsonNode>comparingInt(row -> row.path("anoLevantamento").asInt())
                    .reversed()
                    .thenComparing(
                        Comparator.<JsonNode>comparingInt(
                                row -> row.path("mesLevantamento").asInt())
                            .reversed())
                    .thenComparing(row -> row.path("seq").asText()))
            .toList();
    return new Result(
        matched.stream()
            .skip((long) page * size)
            .limit(size)
            .map(row -> mapper.convertValue(row, FatoPainelDTO.class))
            .toList(),
        matched.size(),
        page,
        size);
  }

  public Map<String, List<String>> options(Filter filter) {
    var result = new LinkedHashMap<String, List<String>>();
    FIELDS.forEach(
        (key, field) ->
            result.put(
                key,
                rows.stream()
                    .filter(row -> matches(row, filter.facet(key)))
                    .map(row -> row.path(field).asText(""))
                    .filter(value -> !value.isBlank())
                    .distinct()
                    .sorted()
                    .toList()));
    return result;
  }
}
