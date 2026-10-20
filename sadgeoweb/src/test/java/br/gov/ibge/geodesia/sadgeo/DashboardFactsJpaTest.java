package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;

import br.gov.ibge.geodesia.sadgeo.dashboard.service.*;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.FatoPainelEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.FatoPainelRepository;
import java.util.Map;
import org.h2.jdbcx.JdbcDataSource;
import org.junit.jupiter.api.Test;
import org.springframework.data.jpa.repository.support.JpaRepositoryFactory;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.persistenceunit.PersistenceManagedTypes;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;

class DashboardFactsJpaTest {
  @Test
  void criteriaPaginationSearchEscapingAndFacetDependenciesUseDatabaseQueries() {
    var datasource = new JdbcDataSource();
    datasource.setURL(
        "jdbc:h2:mem:dashboardfacts;MODE=Oracle;DB_CLOSE_DELAY=-1;INIT=CREATE SCHEMA IF NOT EXISTS"
            + " BDG_VALIDA");
    var factory = new LocalContainerEntityManagerFactoryBean();
    factory.setDataSource(datasource);
    factory.setManagedTypes(PersistenceManagedTypes.of(FatoPainelEntity.class.getName()));
    factory.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
    factory.setJpaPropertyMap(Map.of("hibernate.hbm2ddl.auto", "create-drop"));
    factory.afterPropertiesSet();
    var em = factory.getObject().createEntityManager();
    try {
      em.getTransaction().begin();
      for (int i = 0; i < 4; i++) {
        var row = new FatoPainelEntity();
        row.setSeq(i == 0 ? "literal_%!" : String.valueOf(i));
        row.setAnoLevantamento(i == 3 ? 2025 : 2026);
        row.setMesLevantamento(i == 0 ? 2 : 1);
        row.setCampanha(i == 1 ? "medG" : "medA");
        row.setProjeto(i == 1 ? "G" : "A");
        row.setUf(i == 1 ? "SP" : "RJ");
        row.setMunicipio(i == 1 ? "São Paulo" : "Rio");
        row.setUorgOrigem("DGC");
        em.persist(row);
      }
      em.getTransaction().commit();
      var repository = new JpaRepositoryFactory(em).getRepository(FatoPainelRepository.class);
      var service = new OracleDashboardFactsQuery(repository, em);
      var year = new DashboardFactsQuery.Filter(Map.of("ano", "2026"));
      var first = service.page(year, 0, 1);
      assertEquals(3, first.total());
      assertEquals("literal_%!", first.items().get(0).seq());
      assertNotEquals(first.items().get(0).seq(), service.page(year, 1, 1).items().get(0).seq());
      assertEquals(
          2025,
          service
              .page(
                  new DashboardFactsQuery.Filter(
                      Map.of("sort", "anoLevantamento", "direction", "asc")),
                  0,
                  1)
              .items()
              .get(0)
              .anoLevantamento());
      assertEquals(
          "G",
          service
              .page(
                  new DashboardFactsQuery.Filter(Map.of("sort", "projeto", "direction", "desc")),
                  0,
                  1)
              .items()
              .get(0)
              .projeto());
      var filtered =
          new DashboardFactsQuery.Filter(
              Map.of("ano", "2026", "campanha", "medA", "uf", "RJ", "mes", "2", "q", "_%!"));
      assertEquals(1, service.page(filtered, 0, 25).total());
      assertEquals(
          0,
          service.page(new DashboardFactsQuery.Filter(Map.of("q", "' OR 1=1 --")), 0, 25).total());
      var options = service.options(filtered);
      assertEquals(java.util.List.of("A"), options.get("projeto"));
      assertEquals(java.util.List.of("Rio"), options.get("municipio"));
      assertEquals(2, options.get("ano").size());
    } finally {
      em.close();
      factory.destroy();
    }
  }
}
