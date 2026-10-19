package br.gov.ibge.geodesia.sadgeo.config;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
@Controller
public class SpaController {
    @GetMapping({"/login", "/index", "/registros"}) public String spa() { return "forward:/index.html"; }
}
