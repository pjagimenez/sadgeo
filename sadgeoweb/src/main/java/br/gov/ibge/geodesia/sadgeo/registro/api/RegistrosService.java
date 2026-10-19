package br.gov.ibge.geodesia.sadgeo.registro.api;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.FatoPainelRepository;
import java.util.*;
import org.springframework.context.annotation.Profile;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
@Profile("!demo")
public class RegistrosService {
  private final FatoPainelRepository repository;

  public RegistrosService(FatoPainelRepository repository) {
    this.repository = repository;
  }

  public Map<String, Object> list(String context, int page, int size, String q, String projeto) {
    RegistroContexts.page(page, size);
    String campanha = RegistroContexts.campanha(context);
    String search =
        q.isBlank()
            ? null
            : "%"
                + q.toLowerCase(Locale.ROOT)
                    .replace("!", "!!")
                    .replace("%", "!%")
                    .replace("_", "!_")
                + "%";
    var result =
        repository.pesquisarPainel(
            campanha,
            projeto.isBlank() ? null : projeto,
            search,
            PageRequest.of(page, size, Sort.by("seq")));
    return Map.of(
        "items",
        result.getContent().stream().map(e -> e.toDTO()).toList(),
        "page",
        page,
        "size",
        size,
        "total",
        result.getTotalElements(),
        "totalPages",
        result.getTotalPages(),
        "campanha",
        campanha == null ? "" : campanha);
  }
}
