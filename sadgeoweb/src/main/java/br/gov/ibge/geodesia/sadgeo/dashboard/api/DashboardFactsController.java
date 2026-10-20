package br.gov.ibge.geodesia.sadgeo.dashboard.api;

import br.gov.ibge.geodesia.sadgeo.dashboard.service.DashboardFactsQuery;
import java.util.*;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardFactsController {
  private final DashboardFactsQuery query;

  public DashboardFactsController(DashboardFactsQuery query) {
    this.query = query;
  }

  @GetMapping("/fatos-pagina")
  public DashboardFactsQuery.Result page(@RequestParam Map<String, String> parameters) {
    var filter = new DashboardFactsQuery.Filter(parameters);
    return query.page(
        filter, filter.number("page", 0, 0, 100000), filter.number("size", 25, 1, 100));
  }

  @GetMapping("/fatos-filtros")
  public Map<String, List<String>> options(@RequestParam Map<String, String> parameters) {
    return query.options(new DashboardFactsQuery.Filter(parameters));
  }
}
