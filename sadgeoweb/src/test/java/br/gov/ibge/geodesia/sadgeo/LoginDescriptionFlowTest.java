package br.gov.ibge.geodesia.sadgeo;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import br.gov.ibge.geodesia.sadgeo.auth.*;
import br.gov.ibge.geodesia.sadgeo.config.SecurityConfig;
import java.util.List;
import javax.naming.ldap.LdapName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.ldap.core.DirContextAdapter;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.authentication.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(AuthController.class)
@Import(SecurityConfig.class)
class LoginDescriptionFlowTest {
  @Autowired MockMvc mvc;

  @MockitoBean(name = "authenticationManager")
  AuthenticationManager manager;

  @Test
  void returnsDescriptionAfterValidLoginAndKeepsItInTheSession() throws Exception {
    var context = new DirContextAdapter();
    context.setDn(new LdapName("CN=usuario,DC=example,DC=org"));
    String description = "Equipe \"Campo\"\nGeodésia";
    context.setAttributeValue("description", description);
    var user =
        new DirectoryUserDetailsMapper()
            .mapUserFromContext(
                context,
                "usuario@example.org",
                List.of(new SimpleGrantedAuthority("ROLE_CONSULTA")));
    when(manager.authenticate(any(Authentication.class)))
        .thenReturn(
            UsernamePasswordAuthenticationToken.authenticated(user, null, user.getAuthorities()));
    var login =
        mvc.perform(
                post("/api/auth/login")
                    .with(csrf())
                    .param("username", "usuario@example.org")
                    .param("password", "unit-test-only"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.authenticated").value(true))
            .andExpect(jsonPath("$.description").value(description))
            .andExpect(jsonPath("$.password").doesNotExist())
            .andReturn();
    var session = (MockHttpSession) login.getRequest().getSession(false);
    mvc.perform(get("/api/auth/me").session(session))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.description").value(description))
        .andExpect(jsonPath("$.login").value("usuario@example.org"))
        .andExpect(jsonPath("$.nome").value("usuario@example.org"))
        .andExpect(jsonPath("$.perfil").value("Consulta"))
        .andExpect(jsonPath("$.password").doesNotExist())
        .andExpect(jsonPath("$.dn").doesNotExist());
    mvc.perform(post("/api/auth/logout").session(session).with(csrf()))
        .andExpect(status().isNoContent());
    mvc.perform(get("/api/auth/me")).andExpect(status().isUnauthorized());
  }

  @Test
  void failedLoginDoesNotReturnDirectoryAttributes() throws Exception {
    when(manager.authenticate(any(Authentication.class)))
        .thenThrow(new BadCredentialsException("Credenciais invalidas"));
    mvc.perform(
            post("/api/auth/login")
                .with(csrf())
                .param("username", "usuario")
                .param("password", "invalid-test-password"))
        .andExpect(status().isUnauthorized())
        .andExpect(jsonPath("$.description").doesNotExist());
    mvc.perform(get("/api/auth/me")).andExpect(status().isUnauthorized());
  }
}
