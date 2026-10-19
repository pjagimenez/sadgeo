package br.gov.ibge.geodesia.sadgeo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {
    @Bean
    SecurityFilterChain security(HttpSecurity http) throws Exception {
        // 0.1 exposes read-only dashboard data. Add institutional authentication before public deployment.
        http.authorizeHttpRequests(auth -> auth
            .requestMatchers(org.springframework.http.HttpMethod.GET, "/", "/index.html", "/assets/**", "/api/dashboard/**", "/actuator/health").permitAll()
            .anyRequest().denyAll());
        return http.build();
    }
}
