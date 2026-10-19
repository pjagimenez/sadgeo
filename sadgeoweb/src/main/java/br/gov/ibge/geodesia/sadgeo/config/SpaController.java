package br.gov.ibge.geodesia.sadgeo.config;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class SpaController {
  @GetMapping({
    "/login",
    "/index",
    "/registros",
    "/planejamento/{page}",
    "/campo/{page}",
    "/homologacao/{page}",
    "/analise/{page}",
    "/administracao/{page}",
    "/tabelas/{page}",
    "/bdg/{page}",
    "/qualidade/{page}",
    "/ajuda/{page}"
  })
  public String spa() {
    return "forward:/index.html";
  }
}
