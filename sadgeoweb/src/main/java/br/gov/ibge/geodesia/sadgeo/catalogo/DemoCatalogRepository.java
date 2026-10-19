package br.gov.ibge.geodesia.sadgeo.catalogo;

import java.util.*;
import org.springframework.context.annotation.Profile;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Repository;

@Repository
@Profile("demo")
public class DemoCatalogRepository implements CatalogRepository {
  private final Map<String, List<Map<String, Object>>> data = new HashMap<>();

  public DemoCatalogRepository(TableCatalog catalog) {
    for (var t : catalog.all()) {
      var row = new LinkedHashMap<String, Object>();
      for (var f : t.fields()) {
        Object value =
            switch (f.type()) {
              case "date" -> "2026-01-01";
              case "money", "number", "integer" -> "1";
              default -> f.maxLength() <= 4 ? "1" : "Exemplo";
            };
        row.put(f.name(), value);
      }
      if (t.id().equals("localizacao")) {
        row.put("TIPO_LOCAL", "01");
        row.put("DESCRICAO", "Marco geodésico (demo)");
      }
      if (t.id().equals("fonte-coordenada")) row.put("CD_FONTE_COORDENADA", "01");
      data.put(t.id(), new ArrayList<>(List.of(row)));
    }
  }

  private Object display(Object value) {
    if (value instanceof java.math.BigDecimal n) return n.toPlainString();
    if (value instanceof java.sql.Timestamp d) return d.toLocalDateTime().toString();
    return value;
  }

  @Override
  public List<String> keys(TableCatalog.Table t) {
    return t.demoKeys();
  }

  private boolean matches(TableCatalog.Table t, Map<String, Object> row, Map<String, Object> key) {
    return key.entrySet().stream()
        .allMatch(
            e -> {
              var f =
                  t.fields().stream()
                      .filter(x -> x.name().equals(e.getKey()))
                      .findFirst()
                      .orElseThrow();
              if (List.of("integer", "number", "money").contains(f.type()))
                return new java.math.BigDecimal(row.get(e.getKey()).toString())
                        .compareTo(new java.math.BigDecimal(e.getValue().toString()))
                    == 0;
              return Objects.equals(
                  String.valueOf(row.get(e.getKey())), String.valueOf(e.getValue()));
            });
  }

  private List<Map<String, Object>> filtered(TableCatalog.Table t, String q) {
    return data.get(t.id()).stream()
        .filter(
            r ->
                q.isBlank()
                    || r.values().stream()
                        .anyMatch(
                            v ->
                                String.valueOf(v)
                                    .toLowerCase(Locale.ROOT)
                                    .contains(q.toLowerCase(Locale.ROOT))))
        .toList();
  }

  @Override
  public synchronized List<Map<String, Object>> list(
      TableCatalog.Table t, int offset, int size, String q) {
    return filtered(t, q).stream()
        .skip(offset)
        .limit(size)
        .map(r -> (Map<String, Object>) new LinkedHashMap<>(r))
        .toList();
  }

  @Override
  public synchronized long count(TableCatalog.Table t, String q) {
    return filtered(t, q).size();
  }

  @Override
  public synchronized Map<String, Object> find(TableCatalog.Table t, Map<String, Object> key) {
    return data.get(t.id()).stream()
        .filter(r -> matches(t, r, key))
        .findFirst()
        .map(r -> (Map<String, Object>) new LinkedHashMap<>(r))
        .orElse(null);
  }

  @Override
  public synchronized void insert(TableCatalog.Table t, Map<String, Object> values) {
    var key = new LinkedHashMap<String, Object>();
    keys(t).forEach(k -> key.put(k, values.get(k)));
    if (find(t, key) != null) throw new DuplicateKeyException("Código existente");
    var row = new LinkedHashMap<String, Object>();
    t.columns().forEach(c -> row.put(c, display(values.get(c))));
    if (t.id().equals("equipamento") && !values.containsKey("STATUS_PERMANENCIA"))
      row.put("STATUS_PERMANENCIA", "S");
    data.get(t.id()).add(row);
  }

  @Override
  public synchronized int update(
      TableCatalog.Table t, Map<String, Object> key, Map<String, Object> values) {
    var r = data.get(t.id()).stream().filter(x -> matches(t, x, key)).findFirst();
    r.ifPresent(x -> values.forEach((k, v) -> x.put(k, display(v))));
    return r.isPresent() ? 1 : 0;
  }

  @Override
  public synchronized int delete(TableCatalog.Table t, Map<String, Object> key) {
    return data.get(t.id()).removeIf(r -> matches(t, r, key)) ? 1 : 0;
  }
}
