package br.gov.ibge.geodesia.sadgeo.config;

import br.gov.ibge.geodesia.sadgeo.auth.AuthDiagnostics;
import br.gov.ibge.geodesia.sadgeo.auth.DirectoryUserDetails;
import br.gov.ibge.geodesia.sadgeo.auth.DirectoryUserDetailsMapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.*;
import org.springframework.core.env.Environment;
import org.springframework.security.authentication.*;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.ldap.authentication.ad.ActiveDirectoryLdapAuthenticationProvider;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

@Configuration
@EnableConfigurationProperties(LdapProperties.class)
public class SecurityConfig {
  @Bean
  AuthenticationManager authenticationManager(LdapProperties settings, Environment environment) {
    AuthDiagnostics.configuration(settings, environment);
    settings.validate();
    if (settings.isConfigured()) {
      var provider =
          new ActiveDirectoryLdapAuthenticationProvider(
              settings.getDomain(),
              settings.effectiveUrl(),
              settings.getBaseDn().isBlank() ? null : settings.getBaseDn());
      provider.setUserDetailsContextMapper(new DirectoryUserDetailsMapper());
      provider.setConvertSubErrorCodesToExceptions(true);
      provider.setContextEnvironmentProperties(
          Map.of(
              "com.sun.jndi.ldap.connect.timeout", String.valueOf(settings.getConnectTimeoutMs()),
              "com.sun.jndi.ldap.read.timeout", String.valueOf(settings.getReadTimeoutMs()),
              "java.naming.referral", "ignore"));
      return new ProviderManager(provider);
    }
    return authentication -> {
      throw new AuthenticationServiceException("Autenticação institucional não configurada");
    };
  }

  @Bean
  HttpSessionSecurityContextRepository securityContextRepository() {
    return new HttpSessionSecurityContextRepository();
  }

  @Bean
  SecurityFilterChain security(
      HttpSecurity http,
      AuthenticationManager manager,
      HttpSessionSecurityContextRepository repository,
      ObjectMapper mapper,
      LdapProperties settings)
      throws Exception {
    http.authenticationManager(manager)
        .securityContext(c -> c.securityContextRepository(repository))
        .authorizeHttpRequests(
            auth ->
                auth.dispatcherTypeMatchers(jakarta.servlet.DispatcherType.ERROR)
                    .permitAll()
                    .requestMatchers(
                        org.springframework.http.HttpMethod.GET,
                        "/",
                        "/login",
                        "/index",
                        "/registros",
                        "/planejamento/**",
                        "/campo/**",
                        "/homologacao/**",
                        "/analise/**",
                        "/administracao/**",
                        "/tabelas/**",
                        "/bdg/**",
                        "/qualidade/**",
                        "/ajuda/**",
                        "/index.html",
                        "/assets/**",
                        "/api/dashboard/config",
                        "/api/dashboard/resumo",
                        "/api/dashboard/evolucao-anual",
                        "/api/dashboard/analitico",
                        "/api/dashboard/fatos",
                        "/api/dashboard/fatos-pagina",
                        "/api/dashboard/fatos-filtros",
                        "/api/dashboard/pivot",
                        "/api/auth/csrf",
                        "/actuator/health")
                    .permitAll()
                    .requestMatchers(
                        org.springframework.http.HttpMethod.POST,
                        "/api/auth/login",
                        "/api/auth/demo")
                    .permitAll()
                    .requestMatchers(
                        org.springframework.http.HttpMethod.GET,
                        "/api/dashboard/**",
                        "/api/registros/**",
                        "/api/tabelas/**",
                        "/api/auth/me")
                    .authenticated()
                    .requestMatchers(org.springframework.http.HttpMethod.POST, "/api/tabelas/*")
                    .authenticated()
                    .requestMatchers(org.springframework.http.HttpMethod.PUT, "/api/tabelas/*")
                    .authenticated()
                    .requestMatchers(org.springframework.http.HttpMethod.DELETE, "/api/tabelas/*")
                    .authenticated()
                    .anyRequest()
                    .denyAll())
        .exceptionHandling(
            e ->
                e.authenticationEntryPoint(
                    (req, res, ex) -> json(res, 401, "{\"message\":\"Sessão necessária\"}")))
        .formLogin(
            f ->
                f.loginProcessingUrl("/api/auth/login")
                    .successHandler(
                        (req, res, auth) -> {
                          String description = DirectoryUserDetails.descriptionOf(auth);
                          AuthDiagnostics.success(!description.isBlank());
                          json(
                              res,
                              200,
                              mapper.writeValueAsString(
                                  Map.of("authenticated", true, "description", description)));
                        })
                    .failureHandler(
                        (req, res, ex) -> {
                          var failure = AuthDiagnostics.failure(ex, settings.isConfigured());
                          json(
                              res,
                              failure.status(),
                              mapper.writeValueAsString(
                                  Map.of(
                                      "message",
                                      "Não foi possível autenticar. Consulte o diagnóstico no log.",
                                      "diagnosticId",
                                      failure.diagnosticId(),
                                      "reason",
                                      failure.reason())));
                        }))
        .logout(
            l ->
                l.logoutRequestMatcher(new AntPathRequestMatcher("/api/auth/logout", "POST"))
                    .logoutSuccessHandler((req, res, auth) -> res.setStatus(204)))
        .requestCache(c -> c.disable());
    return http.build();
  }

  private static void json(jakarta.servlet.http.HttpServletResponse res, int status, String body)
      throws java.io.IOException {
    res.setStatus(status);
    res.setContentType("application/json;charset=UTF-8");
    res.getWriter().write(body);
  }
}
