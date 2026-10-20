package br.gov.ibge.geodesia.sadgeo.auth;

import jakarta.servlet.http.*;
import java.util.List;
import java.util.Map;
import org.springframework.core.env.*;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
  private final Environment env;
  private final HttpSessionSecurityContextRepository repository;

  public AuthController(Environment env, HttpSessionSecurityContextRepository repository) {
    this.env = env;
    this.repository = repository;
  }

  @GetMapping("/csrf")
  public Map<String, String> csrf(CsrfToken token) {
    return Map.of("token", token.getToken(), "headerName", token.getHeaderName());
  }

  @GetMapping("/me")
  public Map<String, Object> me(Authentication authentication) {
    return Map.of(
        "login",
        authentication.getName(),
        "nome",
        authentication.getName(),
        "description",
        DirectoryUserDetails.descriptionOf(authentication),
        "perfil",
        isDemo() ? "Demonstração" : "Consulta",
        "demo",
        isDemo());
  }

  @PostMapping("/demo")
  public Map<String, Object> demo(HttpServletRequest request, HttpServletResponse response) {
    if (!isDemo()) throw new ResponseStatusException(HttpStatus.NOT_FOUND);
    request.getSession();
    request.changeSessionId();
    var context = SecurityContextHolder.createEmptyContext();
    context.setAuthentication(
        UsernamePasswordAuthenticationToken.authenticated(
            "Visitante demo", null, List.of(new SimpleGrantedAuthority("ROLE_DEMO"))));
    SecurityContextHolder.setContext(context);
    repository.saveContext(context, request, response);
    return Map.of("authenticated", true, "demo", true);
  }

  private boolean isDemo() {
    return env.acceptsProfiles(Profiles.of("demo"));
  }
}
