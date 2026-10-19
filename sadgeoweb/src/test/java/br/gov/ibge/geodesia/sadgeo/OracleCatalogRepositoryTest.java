package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;

import br.gov.ibge.geodesia.sadgeo.catalogo.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.*;
import org.junit.jupiter.api.Test;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.mock.env.MockEnvironment;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.server.ResponseStatusException;

/**
 * JDBC SQL and metadata regression in isolated H2 Oracle mode; does not substitute real Oracle
 * validation.
 */
class OracleCatalogRepositoryTest {
  @Test
  void discoversActualPrimaryKeysAndExecutesBoundCrud() throws Exception {
    var ds =
        new DriverManagerDataSource(
            "jdbc:h2:mem:catalogtest;MODE=Oracle;DB_CLOSE_DELAY=-1", "sa", "");
    var jdbc = new NamedParameterJdbcTemplate(ds);
    jdbc.getJdbcTemplate().execute("CREATE SCHEMA BDG_VALIDA");
    jdbc.getJdbcTemplate()
        .execute(
            "CREATE TABLE BDG_VALIDA.T_LOCALIZACAO (DESCRICAO VARCHAR2(100), TIPO_LOCAL CHAR(2)"
                + " PRIMARY KEY)");
    jdbc.getJdbcTemplate()
        .execute(
            "CREATE TABLE BDG_VALIDA.T_CAMPANHA (COD_CAMPANHA VARCHAR2(2), COD_PROJETO VARCHAR2(8),"
                + " COD_INSTITUICAO VARCHAR2(4), PRIMARY"
                + " KEY(COD_CAMPANHA,COD_PROJETO,COD_INSTITUICAO))");
    var env = new MockEnvironment().withProperty("sadgeo.catalog.writers", "writer");
    var catalog = new TableCatalog(new ObjectMapper());
    var repo = new OracleCatalogRepository(jdbc, env);
    var service = new CatalogService(repo, catalog, env);
    var writer = UsernamePasswordAuthenticationToken.authenticated("writer", null, List.of());
    var reader = UsernamePasswordAuthenticationToken.authenticated("reader", null, List.of());
    assertEquals(List.of("TIPO_LOCAL"), repo.keys(catalog.get("localizacao")));
    assertEquals(
        Set.of("COD_CAMPANHA", "COD_PROJETO", "COD_INSTITUICAO"),
        new HashSet<>(repo.keys(catalog.get("campanha"))));
    assertFalse(service.canWrite(reader));
    assertThrows(
        ResponseStatusException.class,
        () -> service.create("localizacao", Map.of("TIPO_LOCAL", "ZX"), reader));
    service.create(
        "localizacao", Map.of("TIPO_LOCAL", "ZX", "DESCRICAO", "Literal ' OR 1=1 --"), writer);
    assertEquals(1L, repo.count(catalog.get("localizacao"), "' OR 1=1 --"));
    assertEquals(1, repo.list(catalog.get("localizacao"), 0, 25, "").size());
    service.update(
        "localizacao", Map.of("TIPO_LOCAL", "ZX"), Map.of("DESCRICAO", "Atualizado"), writer);
    assertEquals(
        "Atualizado", service.find("localizacao", Map.of("TIPO_LOCAL", "ZX")).get("DESCRICAO"));
    service.delete("localizacao", Map.of("TIPO_LOCAL", "ZX"), writer);
    assertEquals(0L, repo.count(catalog.get("localizacao"), ""));
    // Fixed CHAR keys must still match after JDBC trims their padding for the API.
    service.create(
        "localizacao", Map.of("TIPO_LOCAL", "A", "DESCRICAO", "Código CHAR curto"), writer);
    assertEquals("A", service.find("localizacao", Map.of("TIPO_LOCAL", "A")).get("TIPO_LOCAL"));
    service.delete("localizacao", Map.of("TIPO_LOCAL", "A"), writer);
  }
}
