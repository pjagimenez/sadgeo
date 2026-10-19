package br.gov.ibge.geodesia.sadgeo;

import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import br.gov.ibge.geodesia.sadgeo.dashboard.api.DashboardController;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.PainelResumoDTO;
import br.gov.ibge.geodesia.sadgeo.dashboard.service.DashboardService;
import br.gov.ibge.geodesia.sadgeo.olap.service.CubeProvider;
import br.gov.ibge.geodesia.sadgeo.config.SecurityConfig;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(DashboardController.class)
@Import(SecurityConfig.class)
class DashboardControllerTest {
    @Autowired MockMvc mvc;
    @MockitoBean DashboardService service;
    @MockitoBean CubeProvider cube;
    @Test void serializesRealServiceResultsAsJson() throws Exception {
        when(service.obterResumoAtual()).thenReturn(new PainelResumoDTO(42L,1L,2L,3L,4L,5L,6L,7L,8L,6L,LocalDate.of(2024,1,1),LocalDate.of(2026,10,1)));
        mvc.perform(get("/api/dashboard/resumo")).andExpect(status().isOk())
            .andExpect(content().contentTypeCompatibleWith("application/json"))
            .andExpect(jsonPath("$.total").value(42))
            .andExpect(jsonPath("$.dtPrimeiroLevantamento").value("2024-01-01"));
        verify(service).obterResumoAtual();
    }
}
