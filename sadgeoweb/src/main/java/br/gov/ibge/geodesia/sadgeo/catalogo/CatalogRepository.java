package br.gov.ibge.geodesia.sadgeo.catalogo;

import java.util.*;

public interface CatalogRepository {
  List<String> keys(TableCatalog.Table table);

  List<Map<String, Object>> list(TableCatalog.Table table, int offset, int size, String q);

  long count(TableCatalog.Table table, String q);

  Map<String, Object> find(TableCatalog.Table table, Map<String, Object> key);

  void insert(TableCatalog.Table table, Map<String, Object> values);

  int update(TableCatalog.Table table, Map<String, Object> key, Map<String, Object> values);

  int delete(TableCatalog.Table table, Map<String, Object> key);
}
