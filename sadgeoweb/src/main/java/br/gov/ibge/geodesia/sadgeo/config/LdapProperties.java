package br.gov.ibge.geodesia.sadgeo.config;

import java.net.URI;
import java.net.URISyntaxException;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Getter;
import lombok.Setter;

/** Non-secret AD connection settings. User credentials are supplied only at login. */
@Getter
@Setter
@ConfigurationProperties(prefix = "sadgeo.auth.ldap")
public class LdapProperties {
    private String host = "";
    private int port = 636;
    private String domain = "";
    private String baseDn = "";
    private String url = "";
    private int connectTimeoutMs = 5000;
    private int readTimeoutMs = 10000;

    public boolean isConfigured() {
        return (!host.isBlank() || !url.isBlank()) && !domain.isBlank();
    }

    public void validate() {
        if (port < 1 || port > 65535) throw new IllegalArgumentException("SADGEO_LDAP_PORT deve estar entre 1 e 65535");
        if (connectTimeoutMs <= 0 || readTimeoutMs <= 0) throw new IllegalArgumentException("Timeouts LDAP devem ser positivos");
        boolean hasServer = !host.isBlank() || !url.isBlank();
        if (hasServer != !domain.isBlank()) throw new IllegalArgumentException("Configure servidor LDAP e SADGEO_LDAP_DOMAIN juntos");
        if (hasServer) effectiveUrl();
    }

    /** URL override keeps compatibility with existing deployments. Never allow plaintext LDAP. */
    public String effectiveUrl() {
        try {
            if (!url.isBlank()) {
                URI parsed = new URI(url);
                if (!"ldaps".equalsIgnoreCase(parsed.getScheme()) || parsed.getHost() == null
                        || parsed.getUserInfo() != null || parsed.getQuery() != null || parsed.getFragment() != null
                        || (parsed.getPath() != null && !parsed.getPath().isEmpty() && !parsed.getPath().equals("/"))
                        || parsed.getPort() == 0 || parsed.getPort() > 65535) {
                    throw new IllegalArgumentException("SADGEO_LDAP_URL deve ser ldaps://servidor:porta; use SADGEO_LDAP_BASE_DN para a base");
                }
                return parsed.toASCIIString();
            }
            if (host.isBlank() || host.contains("://") || host.contains("/") || host.contains(":")) {
                throw new IllegalArgumentException("SADGEO_LDAP_HOST deve conter somente o hostname/FQDN ou IPv4");
            }
            URI parsed = new URI("ldaps", null, host, port, null, null, null);
            if (parsed.getHost() == null) throw new IllegalArgumentException("Hostname LDAP inválido");
            return parsed.toASCIIString();
        } catch (URISyntaxException e) {
            throw new IllegalArgumentException("Endereço LDAPS inválido", e);
        }
    }
}
