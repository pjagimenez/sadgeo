package br.gov.ibge.geodesia.sadgeo.config;

import org.springframework.context.annotation.*;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import java.util.Map;
import org.springframework.security.authentication.*;
import org.springframework.security.ldap.authentication.ad.ActiveDirectoryLdapAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

@Configuration
@EnableConfigurationProperties(LdapProperties.class)
public class SecurityConfig {
    @Bean
    AuthenticationManager authenticationManager(LdapProperties settings) {
        settings.validate();
        if (settings.isConfigured()) {
            var provider = new ActiveDirectoryLdapAuthenticationProvider(
                settings.getDomain(), settings.effectiveUrl(),
                settings.getBaseDn().isBlank() ? null : settings.getBaseDn());
            provider.setConvertSubErrorCodesToExceptions(true);
            provider.setContextEnvironmentProperties(Map.of(
                "com.sun.jndi.ldap.connect.timeout", String.valueOf(settings.getConnectTimeoutMs()),
                "com.sun.jndi.ldap.read.timeout", String.valueOf(settings.getReadTimeoutMs()),
                "java.naming.referral", "ignore"));
            return new ProviderManager(provider);
        }
        return authentication -> { throw new AuthenticationServiceException("Autenticação institucional não configurada"); };
    }
    @Bean
    HttpSessionSecurityContextRepository securityContextRepository() { return new HttpSessionSecurityContextRepository(); }
    @Bean
    SecurityFilterChain security(HttpSecurity http, AuthenticationManager manager,
            HttpSessionSecurityContextRepository repository) throws Exception {
        http.authenticationManager(manager)
            .securityContext(c -> c.securityContextRepository(repository))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(org.springframework.http.HttpMethod.GET, "/", "/login", "/index", "/registros", "/index.html", "/assets/**", "/api/dashboard/config", "/api/auth/csrf", "/actuator/health").permitAll()
                .requestMatchers(org.springframework.http.HttpMethod.POST, "/api/auth/login", "/api/auth/demo").permitAll()
                .requestMatchers(org.springframework.http.HttpMethod.GET, "/api/dashboard/**", "/api/auth/me").authenticated()
                .anyRequest().denyAll())
            .exceptionHandling(e -> e.authenticationEntryPoint((req,res,ex) -> json(res,401,"{\"message\":\"Sessão necessária\"}")))
            .formLogin(f -> f.loginProcessingUrl("/api/auth/login")
                .successHandler((req,res,auth) -> json(res,200,"{\"authenticated\":true}"))
                .failureHandler((req,res,ex) -> json(res,ex instanceof AuthenticationServiceException ? 503 : 401,"{\"message\":\"Não foi possível autenticar. Verifique as credenciais ou a configuração institucional.\"}")))
            .logout(l -> l.logoutRequestMatcher(new AntPathRequestMatcher("/api/auth/logout", "POST"))
                .logoutSuccessHandler((req,res,auth) -> res.setStatus(204)))
            .requestCache(c -> c.disable());
        return http.build();
    }
    private static void json(jakarta.servlet.http.HttpServletResponse res, int status, String body) throws java.io.IOException {
        res.setStatus(status); res.setContentType("application/json;charset=UTF-8"); res.getWriter().write(body);
    }
}
