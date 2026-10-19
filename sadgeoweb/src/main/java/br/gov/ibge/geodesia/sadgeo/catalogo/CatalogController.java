package br.gov.ibge.geodesia.sadgeo.catalogo;

import java.util.*;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tabelas")
public class CatalogController {
  private final CatalogService service;
  private final TableCatalog catalog;

  public CatalogController(CatalogService service, TableCatalog catalog) {
    this.service = service;
    this.catalog = catalog;
  }

  public record Edit(Map<String, Object> key, Map<String, Object> values) {}

  @GetMapping
  public List<Map<String, String>> tables() {
    return catalog.all().stream()
        .map(t -> Map.of("id", t.id(), "title", t.title(), "table", t.table()))
        .toList();
  }

  @GetMapping("/{id}")
  public Map<String, Object> list(
      @PathVariable String id,
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "25") int size,
      @RequestParam(defaultValue = "") String q,
      Authentication auth) {
    return service.list(id, page, size, q, auth);
  }

  @GetMapping("/{id}/meta")
  public Map<String, Object> meta(@PathVariable String id, Authentication auth) {
    return service.metadata(id, auth);
  }

  @GetMapping("/{id}/item")
  public Map<String, Object> find(@PathVariable String id, @RequestParam Map<String, Object> key) {
    return service.find(id, key);
  }

  @PostMapping("/{id}")
  @ResponseStatus(HttpStatus.CREATED)
  public Map<String, Object> create(
      @PathVariable String id, @RequestBody Map<String, Object> values, Authentication auth) {
    return service.create(id, values, auth);
  }

  @PutMapping("/{id}")
  public Map<String, Object> update(
      @PathVariable String id, @RequestBody Edit edit, Authentication auth) {
    return service.update(id, edit.key(), edit.values(), auth);
  }

  @DeleteMapping("/{id}")
  @ResponseStatus(HttpStatus.NO_CONTENT)
  public void delete(@PathVariable String id, @RequestBody Edit edit, Authentication auth) {
    service.delete(id, edit.key(), auth);
  }
}
