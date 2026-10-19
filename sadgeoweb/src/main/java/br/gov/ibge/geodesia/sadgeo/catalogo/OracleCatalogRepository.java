package br.gov.ibge.geodesia.sadgeo.catalogo;

import java.math.BigDecimal;
import java.sql.*;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.ConnectionCallback;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;
import org.springframework.web.server.ResponseStatusException;

@Repository
@Profile("!demo")
public class OracleCatalogRepository implements CatalogRepository {
  private final NamedParameterJdbcTemplate jdbc;
  private final String schema;

  public OracleCatalogRepository(NamedParameterJdbcTemplate jdbc, Environment env) {
    this.jdbc = jdbc;
    schema =
        env.getProperty("spring.jpa.properties.hibernate.default_schema", "BDG_VALIDA")
            .toUpperCase(Locale.ROOT);
    if (!schema.matches("[A-Z][A-Z0-9_]*"))
      throw new IllegalArgumentException("Schema Oracle inválido");
  }

  private String table(TableCatalog.Table t) {
    return schema + "." + t.table();
  }

  @Override
  public List<String> keys(TableCatalog.Table t) {
    return jdbc.getJdbcTemplate()
        .execute(
            (ConnectionCallback<List<String>>)
                connection -> {
                  var result = new TreeMap<Short, String>();
                  try (var rs = connection.getMetaData().getPrimaryKeys(null, schema, t.table())) {
                    while (rs.next())
                      result.put(rs.getShort("KEY_SEQ"), rs.getString("COLUMN_NAME"));
                  }
                  var keys = new ArrayList<>(result.values());
                  if (keys.stream().anyMatch(k -> !t.columns().contains(k)))
                    throw new ResponseStatusException(
                        HttpStatus.CONFLICT,
                        "Chave do Oracle contém colunas não descritas no catálogo");
                  if (t.id().equals("campanha")
                      && !new HashSet<>(keys).equals(new HashSet<>(t.demoKeys())))
                    throw new ResponseStatusException(
                        HttpStatus.CONFLICT,
                        "A PK de T_CAMPANHA difere de COD_CAMPANHA/COD_PROJETO/COD_INSTITUICAO");
                  return keys;
                });
  }

  private String search(TableCatalog.Table t, String q) {
    if (q.isBlank()) return "";
    return " WHERE ("
        + t.fields().stream()
            .filter(f -> f.type().equals("text"))
            .map(f -> "LOWER(" + f.name() + ") LIKE :search ESCAPE '!'")
            .collect(Collectors.joining(" OR "))
        + ")";
  }

  private Map<String, Object> searchParams(String q) {
    return new HashMap<>(
        Map.of(
            "search",
            "%"
                + q.toLowerCase(Locale.ROOT)
                    .replace("!", "!!")
                    .replace("%", "!%")
                    .replace("_", "!_")
                + "%"));
  }

  private Map<String, Object> row(ResultSet rs, int i) throws SQLException {
    var result = new LinkedHashMap<String, Object>();
    var meta = rs.getMetaData();
    for (int c = 1; c <= meta.getColumnCount(); c++) {
      Object value = rs.getObject(c);
      if (value instanceof BigDecimal n) value = n.toPlainString();
      else if (value instanceof Timestamp d) value = d.toLocalDateTime().toString();
      else if (value instanceof java.sql.Date d) value = d.toLocalDate().toString();
      else if (value instanceof String s && meta.getColumnType(c) == Types.CHAR)
        value = s.stripTrailing();
      result.put(meta.getColumnLabel(c).toUpperCase(Locale.ROOT), value);
    }
    return result;
  }

  @Override
  public List<Map<String, Object>> list(TableCatalog.Table t, int offset, int size, String q) {
    var p = searchParams(q);
    p.put("offset", offset);
    p.put("size", size);
    var pk = keys(t);
    String order = String.join(",", pk.isEmpty() ? t.columns() : pk);
    return jdbc.query(
        "SELECT "
            + String.join(",", t.columns())
            + " FROM "
            + table(t)
            + search(t, q)
            + " ORDER BY "
            + order
            + " OFFSET :offset ROWS FETCH NEXT :size ROWS ONLY",
        p,
        this::row);
  }

  @Override
  public long count(TableCatalog.Table t, String q) {
    return jdbc.queryForObject(
        "SELECT COUNT(*) FROM " + table(t) + search(t, q), searchParams(q), Long.class);
  }

  private String where(TableCatalog.Table t, Map<String, Object> key) {
    return key.keySet().stream()
        .map(
            k ->
                (t.fields().stream().anyMatch(f -> f.name().equals(k) && f.fixed())
                        ? "RTRIM(" + k + ")"
                        : k)
                    + " = :k_"
                    + k)
        .collect(Collectors.joining(" AND "));
  }

  private Map<String, Object> keyParams(Map<String, Object> key) {
    var p = new HashMap<String, Object>();
    key.forEach((k, v) -> p.put("k_" + k, v));
    return p;
  }

  @Override
  public Map<String, Object> find(TableCatalog.Table t, Map<String, Object> key) {
    var rows =
        jdbc.query(
            "SELECT "
                + String.join(",", t.columns())
                + " FROM "
                + table(t)
                + " WHERE "
                + where(t, key),
            keyParams(key),
            this::row);
    return rows.isEmpty() ? null : rows.get(0);
  }

  @org.springframework.transaction.annotation.Transactional
  @Override
  public void insert(TableCatalog.Table t, Map<String, Object> values) {
    jdbc.update(
        "INSERT INTO "
            + table(t)
            + " ("
            + String.join(",", values.keySet())
            + ") VALUES ("
            + values.keySet().stream().map(k -> ":" + k).collect(Collectors.joining(","))
            + ")",
        values);
  }

  @org.springframework.transaction.annotation.Transactional
  @Override
  public int update(TableCatalog.Table t, Map<String, Object> key, Map<String, Object> values) {
    if (values.isEmpty()) return find(t, key) == null ? 0 : 1;
    var params = keyParams(key);
    params.putAll(values);
    return jdbc.update(
        "UPDATE "
            + table(t)
            + " SET "
            + values.keySet().stream().map(k -> k + " = :" + k).collect(Collectors.joining(","))
            + " WHERE "
            + where(t, key),
        params);
  }

  @org.springframework.transaction.annotation.Transactional
  @Override
  public int delete(TableCatalog.Table t, Map<String, Object> key) {
    return jdbc.update("DELETE FROM " + table(t) + " WHERE " + where(t, key), keyParams(key));
  }
}
