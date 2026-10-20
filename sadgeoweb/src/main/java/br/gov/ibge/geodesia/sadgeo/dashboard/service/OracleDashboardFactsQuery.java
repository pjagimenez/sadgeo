package br.gov.ibge.geodesia.sadgeo.dashboard.service;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.FatoPainelEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.FatoPainelRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.criteria.Predicate;
import java.util.*;
import org.springframework.context.annotation.Profile;
import org.springframework.data.domain.*;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Profile("!demo")
@Transactional(readOnly = true)
public class OracleDashboardFactsQuery implements DashboardFactsQuery {
  private final FatoPainelRepository repository;
  private final EntityManager em;

  public OracleDashboardFactsQuery(FatoPainelRepository repository, EntityManager em) {
    this.repository = repository;
    this.em = em;
  }

  private Specification<FatoPainelEntity> specification(Filter filter) {
    return (root, query, cb) -> {
      var predicates = new ArrayList<Predicate>();
      FIELDS.forEach(
          (key, field) -> {
            if (filter.get(key) != null)
              predicates.add(
                  cb.equal(
                      root.get(field),
                      key.equals("ano") || key.equals("mes")
                          ? Integer.valueOf(filter.get(key))
                          : filter.get(key)));
          });
      String q = filter.get("q");
      if (q != null && !q.isBlank()) {
        String term =
            "%"
                + q.toLowerCase(Locale.ROOT)
                    .replace("!", "!!")
                    .replace("%", "!%")
                    .replace("_", "!_")
                + "%";
        predicates.add(
            cb.or(
                java.util.stream.Stream.of(
                        "seq",
                        "campanha",
                        "projeto",
                        "uf",
                        "municipio",
                        "uorgOrigem",
                        "situacao",
                        "tipoLocal")
                    .map(field -> cb.like(cb.lower(root.get(field)), term, '!'))
                    .toArray(Predicate[]::new)));
      }
      return cb.and(predicates.toArray(Predicate[]::new));
    };
  }

  public Result page(Filter filter, int page, int size) {
    var result =
        repository.findAll(
            specification(filter),
            PageRequest.of(
                page,
                size,
                Sort.by(
                    Sort.Order.desc("anoLevantamento"),
                    Sort.Order.desc("mesLevantamento"),
                    Sort.Order.asc("seq"))));
    return new Result(
        result.getContent().stream().map(FatoPainelEntity::toDTO).toList(),
        result.getTotalElements(),
        page,
        size);
  }

  public Map<String, List<String>> options(Filter filter) {
    var result = new LinkedHashMap<String, List<String>>();
    FIELDS.forEach(
        (key, field) -> {
          var cb = em.getCriteriaBuilder();
          var query = cb.createQuery(Object.class);
          var root = query.from(FatoPainelEntity.class);
          query
              .select(root.get(field))
              .distinct(true)
              .where(specification(filter.facet(key)).toPredicate(root, query, cb));
          var values =
              em.createQuery(query).getResultList().stream()
                  .filter(Objects::nonNull)
                  .map(Object::toString)
                  .sorted()
                  .toList();
          result.put(key, values);
        });
    return result;
  }
}
