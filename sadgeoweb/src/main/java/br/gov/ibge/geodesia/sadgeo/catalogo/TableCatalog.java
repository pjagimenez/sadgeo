package br.gov.ibge.geodesia.sadgeo.catalogo;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.util.*;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

@Component
public class TableCatalog {
  public record Field(
      String name, String label, String type, int maxLength, boolean nullable, boolean fixed) {}

  public record Table(
      String id, String title, String table, List<String> demoKeys, List<Field> fields) {
    public List<String> columns() {
      return fields.stream().map(Field::name).toList();
    }
  }

  private final List<Table> tables;

  public TableCatalog(ObjectMapper mapper) throws IOException {
    try (var in = new ClassPathResource("catalogo.json").getInputStream()) {
      tables = mapper.readValue(in, new TypeReference<>() {});
    }
  }

  public List<Table> all() {
    return tables;
  }

  public Table get(String id) {
    return tables.stream()
        .filter(t -> t.id().equals(id))
        .findFirst()
        .orElseThrow(
            () -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Tabela não cadastrada"));
  }
}
