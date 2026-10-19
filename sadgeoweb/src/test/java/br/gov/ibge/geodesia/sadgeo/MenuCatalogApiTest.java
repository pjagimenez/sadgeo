package br.gov.ibge.geodesia.sadgeo;

import static org.hamcrest.Matchers.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import br.gov.ibge.geodesia.sadgeo.registro.api.RegistroContexts;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("demo")
class MenuCatalogApiTest {
  @Autowired MockMvc mvc;

  private org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder json(
      String method, String path, String body) {
    return request(org.springframework.http.HttpMethod.valueOf(method), path)
        .with(user("tester"))
        .with(csrf())
        .contentType("application/json")
        .content(body);
  }

  @Test
  void allAnalysisContextsEnforceTheirImplicitCampaign() throws Exception {
    for (var context : RegistroContexts.CAMPANHAS.entrySet()) {
      mvc.perform(
              get("/api/registros/" + context.getKey())
                  .param("campanha", "tentativa-de-troca")
                  .with(user("tester")))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.campanha").value(context.getValue()))
          .andExpect(jsonPath("$.total", greaterThan(0)))
          .andExpect(jsonPath("$.items[*].campanha", everyItem(is(context.getValue()))));
    }
    mvc.perform(get("/api/registros/critica").param("size", "5").with(user("tester")))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.items", hasSize(5)))
        .andExpect(jsonPath("$.campanha").value(""));
    mvc.perform(get("/api/registros/altimetria").param("q", "inexistente").with(user("tester")))
        .andExpect(jsonPath("$.total").value(0));
    mvc.perform(get("/api/registros/critica").param("size", "999").with(user("tester")))
        .andExpect(status().isBadRequest());
    mvc.perform(get("/api/registros/desconhecido").with(user("tester")))
        .andExpect(status().isNotFound());
  }

  @Test
  void localizacaoCrudAndValidation() throws Exception {
    mvc.perform(
            json(
                "POST",
                "/api/tabelas/localizacao",
                "{\"TIPO_LOCAL\":\"ZX\",\"DESCRICAO\":\"Teste\"}"))
        .andExpect(status().isCreated());
    try {
      mvc.perform(json("POST", "/api/tabelas/localizacao", "{\"TIPO_LOCAL\":\"ZX\"}"))
          .andExpect(status().isConflict());
      mvc.perform(
              json(
                  "PUT",
                  "/api/tabelas/localizacao",
                  "{\"key\":{\"TIPO_LOCAL\":\"ZX\"},\"values\":{\"DESCRICAO\":\"Atualizado\"}}"))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.DESCRICAO").value("Atualizado"));
      mvc.perform(
              get("/api/tabelas/localizacao/item").param("TIPO_LOCAL", "ZX").with(user("tester")))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.DESCRICAO").value("Atualizado"));
      mvc.perform(
              json(
                  "PUT",
                  "/api/tabelas/localizacao",
                  "{\"key\":{\"TIPO_LOCAL\":\"ZX\"},\"values\":{\"TIPO_LOCAL\":\"ZY\"}}"))
          .andExpect(status().isBadRequest());
    } finally {
      mvc.perform(json("DELETE", "/api/tabelas/localizacao", "{\"key\":{\"TIPO_LOCAL\":\"ZX\"}}"))
          .andExpect(status().isNoContent());
    }
    mvc.perform(get("/api/tabelas/localizacao/item").param("TIPO_LOCAL", "ZX").with(user("tester")))
        .andExpect(status().isNotFound());
    mvc.perform(json("POST", "/api/tabelas/localizacao", "{\"TIPO_LOCAL\":\"MUITO\"}"))
        .andExpect(status().isBadRequest());
    mvc.perform(json("POST", "/api/tabelas/localizacao", "{\"DESCRICAO\":\"Sem chave\"}"))
        .andExpect(status().isBadRequest());
    mvc.perform(
            json(
                "POST",
                "/api/tabelas/localizacao",
                "{\"TIPO_LOCAL\":\"ZX\",\"CAMPO_INVENTADO\":1}"))
        .andExpect(status().isBadRequest());
  }

  @Test
  void campanhaUsesCompleteCompositeKey() throws Exception {
    String body =
        "{\"COD_CAMPANHA\":\"ZT\",\"COD_PROJETO\":\"TESTE\",\"COD_INSTITUICAO\":\"9999\",\"VAL_DIARIA\":\"123.45\"}";
    mvc.perform(json("POST", "/api/tabelas/campanha", body))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.VAL_DIARIA").value("123.45"));
    try {
      mvc.perform(
              get("/api/tabelas/campanha/item").param("COD_CAMPANHA", "ZT").with(user("tester")))
          .andExpect(status().isBadRequest());
      mvc.perform(
              get("/api/tabelas/campanha/item")
                  .param("COD_CAMPANHA", "ZT")
                  .param("COD_PROJETO", "TESTE")
                  .param("COD_INSTITUICAO", "9999")
                  .with(user("tester")))
          .andExpect(status().isOk());
      mvc.perform(
              json(
                  "PUT",
                  "/api/tabelas/campanha",
                  "{\"key\":{\"COD_CAMPANHA\":\"ZT\",\"COD_PROJETO\":\"TESTE\",\"COD_INSTITUICAO\":\"9999\"},\"values\":{\"VAL_DIARIA\":\"123456.78\"}}"))
          .andExpect(status().isBadRequest());
    } finally {
      mvc.perform(
              json(
                  "DELETE",
                  "/api/tabelas/campanha",
                  "{\"key\":{\"COD_CAMPANHA\":\"ZT\",\"COD_PROJETO\":\"TESTE\",\"COD_INSTITUICAO\":\"9999\"}}"))
          .andExpect(status().isNoContent());
    }
  }

  @Test
  void pendenciasAndNumericPrecision() throws Exception {
    mvc.perform(
            json(
                "POST",
                "/api/tabelas/pendencia",
                "{\"COD_PEND\":\"ZX\",\"DSC_PENDENCIA\":\"Pendência de teste\"}"))
        .andExpect(status().isCreated());
    mvc.perform(json("DELETE", "/api/tabelas/pendencia", "{\"key\":{\"COD_PEND\":\"ZX\"}}"))
        .andExpect(status().isNoContent());
    mvc.perform(
            json(
                "POST",
                "/api/tabelas/fonte-coordenada",
                "{\"CD_FONTE_COORDENADA\":\"9\",\"DS_FONTE_COORDENADA\":\"Teste\",\"RK_PRECISAO_TIPICA\":\"12345678901234567890123456789012345678\"}"))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.CD_FONTE_COORDENADA").value("09"))
        .andExpect(
            jsonPath("$.RK_PRECISAO_TIPICA").value("12345678901234567890123456789012345678"));
    mvc.perform(
            json(
                "DELETE",
                "/api/tabelas/fonte-coordenada",
                "{\"key\":{\"CD_FONTE_COORDENADA\":\"09\"}}"))
        .andExpect(status().isNoContent());
  }

  @Test
  void protectedRoutesAndAllCatalogs() throws Exception {
    mvc.perform(get("/actuator/health"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("UP"));
    mvc.perform(get("/api/tabelas/localizacao")).andExpect(status().isUnauthorized());
    mvc.perform(get("/api/registros/critica")).andExpect(status().isUnauthorized());
    mvc.perform(
            post("/api/tabelas/localizacao")
                .with(user("tester"))
                .contentType("application/json")
                .content("{}"))
        .andExpect(status().isForbidden());
    mvc.perform(get("/api/tabelas").with(user("tester")))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$", hasSize(11)));
    for (String table :
        new String[] {
          "localizacao",
          "tipo-projeto",
          "situacao-marco",
          "metodo-calculo",
          "fonte-coordenada",
          "equipamento",
          "campanha",
          "atividade",
          "status",
          "municipio",
          "pendencia"
        })
      mvc.perform(get("/api/tabelas/" + table).with(user("tester")))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.meta.keys", not(empty())));
    mvc.perform(get("/api/tabelas/inventada").with(user("tester")))
        .andExpect(status().isNotFound());
    mvc.perform(get("/analise/altimetria"))
        .andExpect(status().isOk())
        .andExpect(forwardedUrl("/index.html"));
  }
}
