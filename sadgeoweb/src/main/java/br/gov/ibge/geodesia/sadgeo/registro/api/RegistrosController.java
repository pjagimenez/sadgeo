package br.gov.ibge.geodesia.sadgeo.registro.api;

import java.util.Map;
import org.springframework.context.annotation.Profile;
import org.springframework.web.bind.annotation.*;

@RestController
@Profile("!demo")
@RequestMapping("/api/registros")
public class RegistrosController {
  private final RegistrosService service;

  public RegistrosController(RegistrosService service) {
    this.service = service;
  }

  @GetMapping("/{context}")
  public Map<String, Object> list(
      @PathVariable String context,
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "25") int size,
      @RequestParam(defaultValue = "") String q,
      @RequestParam(defaultValue = "") String projeto) {
    return service.list(context, page, size, q, projeto);
  }
}
