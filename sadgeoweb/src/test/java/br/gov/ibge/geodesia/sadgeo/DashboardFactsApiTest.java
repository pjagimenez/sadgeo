package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("demo")
class DashboardFactsApiTest {
  @Autowired MockMvc mvc;
  @Autowired ObjectMapper mapper;

  @Test
  void anonymousFactsArePagedOrderedAndFiltered() throws Exception {
    var result =
        mvc.perform(get("/api/dashboard/fatos-pagina").param("size", "2"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.size").value(2))
            .andExpect(jsonPath("$.items.length()").value(2))
            .andReturn();
    var data = mapper.readTree(result.getResponse().getContentAsString());
    assertTrue(data.get("total").asInt() > 2);
    var first = data.get("items").get(0);
    mvc.perform(
            get("/api/dashboard/fatos-pagina")
                .param("ano", first.get("anoLevantamento").asText())
                .param("campanha", first.get("campanha").asText())
                .param("uf", first.get("uf").asText()))
        .andExpect(status().isOk())
        .andExpect(
            jsonPath("$.items[0].anoLevantamento").value(first.get("anoLevantamento").asInt()));
    mvc.perform(get("/api/dashboard/fatos-pagina").param("q", "inexistente-zzzz"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.total").value(0));
    var page2 =
        mvc.perform(get("/api/dashboard/fatos-pagina").param("size", "2").param("page", "1"))
            .andExpect(status().isOk())
            .andReturn();
    assertNotEquals(
        first.get("seq"),
        mapper.readTree(page2.getResponse().getContentAsString()).get("items").get(0).get("seq"));
  }

  @Test
  void validatesBoundsAndKeepsOperationalDataProtected() throws Exception {
    for (String invalid : new String[] {"0", "101", "abc"})
      mvc.perform(get("/api/dashboard/fatos-pagina").param("size", invalid))
          .andExpect(status().isBadRequest());
    mvc.perform(get("/api/dashboard/fatos-pagina").param("mes", "13"))
        .andExpect(status().isBadRequest());
    mvc.perform(get("/api/dashboard/fatos-pagina").param("ano", "2026 or 1=1"))
        .andExpect(status().isBadRequest());
    mvc.perform(get("/api/registros/critica")).andExpect(status().isUnauthorized());
  }

  @Test
  void facetOptionsRespectYearCampaignAndUfDependencies() throws Exception {
    var result =
        mvc.perform(
                get("/api/dashboard/fatos-filtros")
                    .param("ano", "2026")
                    .param("campanha", "medA")
                    .param("uf", "RJ"))
            .andExpect(status().isOk())
            .andReturn();
    var options = mapper.readTree(result.getResponse().getContentAsString());
    assertTrue(options.get("ano").size() > 1);
    var rows =
        mapper
            .readTree(
                mvc.perform(
                        get("/api/dashboard/fatos-pagina")
                            .param("ano", "2026")
                            .param("campanha", "medA")
                            .param("size", "100"))
                    .andReturn()
                    .getResponse()
                    .getContentAsString())
            .get("items");
    for (var row : rows)
      assertTrue(options.get("projeto").toString().contains(row.get("projeto").asText()));
    assertTrue(options.has("mes"));
    assertTrue(options.has("municipio"));
  }
}
