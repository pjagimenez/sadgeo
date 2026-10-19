package br.gov.ibge.geodesia.sadgeo.catalogo;

import java.math.BigDecimal;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
import org.springframework.core.env.*;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class CatalogService {
  private final CatalogRepository repository;
  private final TableCatalog catalog;
  private final Environment env;

  public CatalogService(CatalogRepository repository, TableCatalog catalog, Environment env) {
    this.repository = repository;
    this.catalog = catalog;
    this.env = env;
  }

  public boolean canWrite(Authentication auth) {
    if (auth == null || !auth.isAuthenticated() || "anonymousUser".equals(auth.getName()))
      return false;
    if (env.acceptsProfiles(Profiles.of("demo"))) return true;
    return Arrays.stream(env.getProperty("sadgeo.catalog.writers", "").split(","))
        .map(String::strip)
        .filter(s -> !s.isBlank())
        .anyMatch(s -> s.equalsIgnoreCase(auth.getName()));
  }

  private void writer(Authentication auth) {
    if (!canWrite(auth))
      throw new ResponseStatusException(
          HttpStatus.FORBIDDEN, "Usuário sem permissão de manutenção das tabelas básicas");
  }

  private List<String> keys(TableCatalog.Table t) {
    return repository.keys(t);
  }

  private void requireKeys(List<String> keys) {
    if (keys.isEmpty())
      throw new ResponseStatusException(
          HttpStatus.CONFLICT, "Tabela sem chave primária confirmada; manutenção indisponível");
  }

  public Map<String, Object> metadata(String id, Authentication auth) {
    var t = catalog.get(id);
    var pk = keys(t);
    return Map.of(
        "id",
        t.id(),
        "title",
        t.title(),
        "table",
        t.table(),
        "fields",
        t.fields(),
        "keys",
        pk,
        "canWrite",
        canWrite(auth) && !pk.isEmpty());
  }

  public Map<String, Object> list(String id, int page, int size, String q, Authentication auth) {
    if (page < 0 || page > 100000 || size < 1 || size > 100)
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Página/tamanho inválidos");
    var t = catalog.get(id);
    return Map.of(
        "meta",
        metadata(id, auth),
        "items",
        repository.list(t, page * size, size, q),
        "total",
        repository.count(t, q),
        "page",
        page,
        "size",
        size);
  }

  private Map<String, Object> normalize(
      TableCatalog.Table t, Map<String, Object> input, boolean create) {
    if (input == null)
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Informe os campos");
    if (!t.columns().containsAll(input.keySet()))
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Campo desconhecido");
    var result = new LinkedHashMap<String, Object>();
    for (var f : t.fields()) {
      if (!input.containsKey(f.name())) {
        if (create && !f.nullable())
          throw new ResponseStatusException(
              HttpStatus.BAD_REQUEST, "Campo obrigatório: " + f.name());
        continue;
      }
      Object raw = input.get(f.name());
      String text = raw == null ? "" : raw.toString();
      if (f.fixed()) text = text.stripTrailing();
      if (text.isBlank()) {
        if (!f.nullable())
          throw new ResponseStatusException(
              HttpStatus.BAD_REQUEST, "Campo obrigatório: " + f.name());
        result.put(f.name(), null);
        continue;
      }
      try {
        Object value =
            switch (f.type()) {
              case "date" ->
                  Timestamp.valueOf(
                      text.length() == 10
                          ? LocalDate.parse(text).atStartOfDay()
                          : LocalDateTime.parse(text));
              case "integer", "number", "money" -> {
                var number = new BigDecimal(text);
                if (f.type().equals("integer") && number.stripTrailingZeros().scale() > 0)
                  throw new IllegalArgumentException();
                if (f.type().equals("money")
                    && (number.stripTrailingZeros().scale() > 2
                        || number.abs().compareTo(new BigDecimal("100000")) >= 0))
                  throw new IllegalArgumentException();
                if (f.type().equals("integer")
                    && number.abs().compareTo(BigDecimal.TEN.pow(38)) >= 0)
                  throw new IllegalArgumentException();
                yield number;
              }
              default -> {
                if (f.name().equals("CD_FONTE_COORDENADA") && text.matches("[0-9]"))
                  text = "0" + text;
                if (f.maxLength() > 0
                    && text.getBytes(java.nio.charset.StandardCharsets.UTF_8).length
                        > f.maxLength()) throw new IllegalArgumentException();
                yield text;
              }
            };
        result.put(f.name(), value);
      } catch (RuntimeException ex) {
        throw new ResponseStatusException(
            HttpStatus.BAD_REQUEST, "Valor inválido para " + f.name());
      }
    }
    return result;
  }

  private Map<String, Object> key(TableCatalog.Table t, Map<String, Object> input) {
    var pk = keys(t);
    requireKeys(pk);
    if (input == null || !input.keySet().equals(new HashSet<>(pk)))
      throw new ResponseStatusException(
          HttpStatus.BAD_REQUEST, "Informe a chave completa: " + String.join(", ", pk));
    var normalized = normalize(t, input, false);
    if (normalized.values().stream().anyMatch(Objects::isNull))
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Chave não pode ser nula");
    return normalized;
  }

  public Map<String, Object> find(String id, Map<String, Object> input) {
    var t = catalog.get(id);
    return found(repository.find(t, key(t, input)));
  }

  private Map<String, Object> found(Map<String, Object> row) {
    if (row == null)
      throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Registro não encontrado");
    return row;
  }

  public Map<String, Object> create(String id, Map<String, Object> values, Authentication auth) {
    writer(auth);
    var t = catalog.get(id);
    var pk = keys(t);
    requireKeys(pk);
    var normalized = normalize(t, values, true);
    var key = new LinkedHashMap<String, Object>();
    for (String k : pk) {
      if (!normalized.containsKey(k) || normalized.get(k) == null)
        throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Informe " + k);
      key.put(k, normalized.get(k));
    }
    repository.insert(t, normalized);
    return found(repository.find(t, key));
  }

  public Map<String, Object> update(
      String id, Map<String, Object> inputKey, Map<String, Object> values, Authentication auth) {
    writer(auth);
    var t = catalog.get(id);
    var key = key(t, inputKey);
    var normalized = normalize(t, values, false);
    if (normalized.keySet().stream().anyMatch(key::containsKey))
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "A chave não pode ser alterada");
    if (repository.update(t, key, normalized) != 1)
      throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Registro não encontrado");
    return found(repository.find(t, key));
  }

  public void delete(String id, Map<String, Object> inputKey, Authentication auth) {
    writer(auth);
    var t = catalog.get(id);
    if (repository.delete(t, key(t, inputKey)) != 1)
      throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Registro não encontrado");
  }
}
