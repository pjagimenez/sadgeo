package br.gov.ibge.geodesia.sadgeo.dashboard.service;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.FatoPainelDTO;
import java.util.*;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public interface DashboardFactsQuery {
  Map<String, String> FIELDS =
      Map.of(
          "ano",
          "anoLevantamento",
          "mes",
          "mesLevantamento",
          "campanha",
          "campanha",
          "projeto",
          "projeto",
          "uf",
          "uf",
          "municipio",
          "municipio",
          "uorgOrigem",
          "uorgOrigem",
          "situacao",
          "situacao");

  record Result(List<FatoPainelDTO> items, long total, int page, int size) {}

  final class Filter {
    private final Map<String, String> values;

    public Filter(Map<String, String> input) {
      values = new HashMap<>();
      for (String key : FIELDS.keySet()) {
        String value = input.get(key);
        if (value != null && !value.isBlank()) {
          if (value.length() > 200) throw bad("Filtro muito longo");
          values.put(key, value.trim());
        }
      }
      String q = input.getOrDefault("q", "").trim();
      if (q.length() > 200) throw bad("Pesquisa muito longa");
      values.put("q", q);
      for (String key : List.of("page", "size"))
        if (input.containsKey(key)) values.put(key, input.get(key));
      if (values.containsKey("ano")) number("ano", 0, 1, 9999);
      if (values.containsKey("mes")) number("mes", 0, 1, 12);
    }

    public String get(String name) {
      return values.get(name);
    }

    public int number(String key, int fallback, int min, int max) {
      try {
        int value = values.containsKey(key) ? Integer.parseInt(values.get(key)) : fallback;
        if (value < min || value > max) throw new NumberFormatException();
        return value;
      } catch (NumberFormatException e) {
        throw bad("Parametro invalido: " + key);
      }
    }

    public Filter facet(String field) {
      var scoped = new HashMap<String, String>();
      if (!field.equals("ano") && get("ano") != null) scoped.put("ano", get("ano"));
      if (field.equals("projeto") && get("campanha") != null)
        scoped.put("campanha", get("campanha"));
      if (field.equals("municipio") && get("uf") != null) scoped.put("uf", get("uf"));
      return new Filter(scoped);
    }

    private static ResponseStatusException bad(String message) {
      return new ResponseStatusException(HttpStatus.BAD_REQUEST, message);
    }
  }

  Result page(Filter filter, int page, int size);

  Map<String, List<String>> options(Filter filter);
}
