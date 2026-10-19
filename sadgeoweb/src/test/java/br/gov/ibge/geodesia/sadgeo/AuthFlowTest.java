package br.gov.ibge.geodesia.sadgeo;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.*;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("demo")
class AuthFlowTest {
  @Autowired MockMvc mvc;

  @Test
  void sessionProtectsDataAndLogoutRevokesAccess() throws Exception {
    mvc.perform(get("/api/dashboard/resumo")).andExpect(status().isUnauthorized());
    mvc.perform(post("/api/auth/demo")).andExpect(status().isForbidden());
    var result =
        mvc.perform(post("/api/auth/demo").with(csrf())).andExpect(status().isOk()).andReturn();
    var session = (MockHttpSession) result.getRequest().getSession(false);
    mvc.perform(get("/api/auth/me").session(session))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.demo").value(true));
    mvc.perform(get("/api/dashboard/resumo").session(session)).andExpect(status().isOk());
    mvc.perform(post("/api/auth/logout").session(session).with(csrf()))
        .andExpect(status().isNoContent());
    mvc.perform(get("/api/auth/me")).andExpect(status().isUnauthorized());
  }

  @Test
  void noInventedCredentialsAreAccepted() throws Exception {
    mvc.perform(
            post("/api/auth/login")
                .with(csrf())
                .param("username", "inventado")
                .param("password", "incorreta"))
        .andExpect(status().isServiceUnavailable());
  }

  @Test
  void spaRoutesAreForwarded() throws Exception {
    for (String path :
        new String[] {
          "/bdg/aguardando", "/qualidade/producao", "/administracao/integracoes", "/ajuda/guia"
        }) mvc.perform(get(path)).andExpect(status().isOk()).andExpect(forwardedUrl("/index.html"));
    mvc.perform(get("/login")).andExpect(status().isOk()).andExpect(forwardedUrl("/index.html"));
    mvc.perform(get("/registros"))
        .andExpect(status().isOk())
        .andExpect(forwardedUrl("/index.html"));
  }
}
