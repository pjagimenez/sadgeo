package br.gov.ibge.geodesia.sadgeo;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;
import br.gov.ibge.geodesia.sadgeo.auth.AuthController;
import br.gov.ibge.geodesia.sadgeo.config.SecurityConfig;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
@WebMvcTest(AuthController.class)
@Import(SecurityConfig.class)
class ProductionAuthTest {
    @Autowired MockMvc mvc;
    @Test void demoEntryIsUnavailableOutsideDemoProfile() throws Exception {
        mvc.perform(post("/api/auth/demo").with(csrf())).andExpect(status().isNotFound());
        mvc.perform(get("/api/auth/me")).andExpect(status().isUnauthorized());
    }
}
