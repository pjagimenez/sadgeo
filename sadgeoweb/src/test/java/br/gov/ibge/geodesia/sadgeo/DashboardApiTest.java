package br.gov.ibge.geodesia.sadgeo;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("demo")
@org.springframework.security.test.context.support.WithMockUser
class DashboardApiTest {
    @Autowired MockMvc mvc;
    @Test void demoStartsWithoutOracleAndReturnsDashboardContracts() throws Exception {
        mvc.perform(get("/api/dashboard/config")).andExpect(status().isOk()).andExpect(jsonPath("$.demo").value(true));
        mvc.perform(get("/api/dashboard/resumo")).andExpect(status().isOk()).andExpect(jsonPath("$.total").isNumber());
        mvc.perform(get("/api/dashboard/evolucao-anual")).andExpect(status().isOk()).andExpect(jsonPath("$[0].ano").isNumber());
        mvc.perform(get("/api/dashboard/fatos")).andExpect(status().isOk()).andExpect(jsonPath("$[0].campanha").isString());
        mvc.perform(get("/api/dashboard/analitico")).andExpect(status().isOk()).andExpect(jsonPath("$[0].contagem").isNumber());
        mvc.perform(get("/api/dashboard/pivot")).andExpect(status().isOk()).andExpect(jsonPath("$.categorias").isArray()).andExpect(jsonPath("$.series").isMap());
    }
    @Test void rejectsUnknownSectionsAndWrites() throws Exception {
        mvc.perform(get("/api/dashboard/inexistente")).andExpect(status().isNotFound());
        mvc.perform(post("/api/dashboard/resumo")).andExpect(status().isForbidden());
    }
}
