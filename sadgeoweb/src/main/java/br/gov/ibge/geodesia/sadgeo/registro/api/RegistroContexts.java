package br.gov.ibge.geodesia.sadgeo.registro.api;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public final class RegistroContexts {
  private RegistroContexts() {}

  public static final Map<String, String> CAMPANHAS =
      Map.of(
          "altimetria",
          "medA",
          "gravimetria",
          "medG",
          "planimetria",
          "medP",
          "vrf",
          "vrf",
          "veg",
          "veg",
          "ogr",
          "ogr",
          "gabinete",
          "gab");

  public static String campanha(String context) {
    if ("critica".equals(context)) return null;
    if (!CAMPANHAS.containsKey(context))
      throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Contexto desconhecido");
    return CAMPANHAS.get(context);
  }

  public static void page(int page, int size) {
    if (page < 0 || page > 100000 || size < 1 || size > 100)
      throw new ResponseStatusException(
          HttpStatus.BAD_REQUEST, "Página/tamanho inválidos (size: 1 a 100)");
  }
}
