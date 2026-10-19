package br.gov.ibge.geodesia.sadgeo.dashboard.api;

import java.util.List;
import org.springframework.context.annotation.Profile;
import org.springframework.web.bind.annotation.*;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.*;
import br.gov.ibge.geodesia.sadgeo.dashboard.service.DashboardService;
import br.gov.ibge.geodesia.sadgeo.olap.*;
import br.gov.ibge.geodesia.sadgeo.olap.service.CubeProvider;

@RestController
@Profile("!demo")
@RequestMapping("/api/dashboard")
public class DashboardController {
    private final DashboardService service;
    private final CubeProvider cube;
    public DashboardController(DashboardService service, CubeProvider cube) {
        this.service = service; this.cube = cube;
    }
    @GetMapping("/resumo") public PainelResumoDTO resumo() { return service.obterResumoAtual(); }
    @GetMapping("/evolucao-anual") public List<EvolucaoAnualDTO> anual() { return service.obterEvolucaoAnual(); }
    @GetMapping("/campanhas") public List<EvolucaoAnualCampanhaProjetoUfDTO> campanhas() { return service.obterEvolucaoCampanhaAnual(); }
    @GetMapping("/analitico") public List<ResumoAnaliticoDTO> analitico() { return service.obterResumoAnalitico(); }
    @GetMapping("/fatos") public List<FatoPainelDTO> fatos() { return service.obterFatoPainel(); }
    @GetMapping("/pivot") public PivotTable pivot() { return cube.getCube().pivot(Dimensao.ANO, Dimensao.CAMPANHA, Medida.CONTAGEM); }
}
