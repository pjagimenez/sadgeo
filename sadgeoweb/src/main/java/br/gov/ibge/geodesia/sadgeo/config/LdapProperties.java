package br.gov.ibge.geodesia.sadgeo.config;

import java.net.URI;
import java.net.URISyntaxException;
import org.springframework.boot.context.properties.ConfigurationProperties;

/** Non-secret AD connection settings. User credentials are supplied only at login. */
@ConfigurationProperties(prefix = "sadgeo.auth.ldap")
public class LdapProperties {
	private String protocol = "";
    private String host = "";
    private int port = 0;
    private String domain = "";
    private String baseDn = "";
    private String url = "";
    private int connectTimeoutMs = 5000;
    private int readTimeoutMs = 10000;

	public String getProtocol() {
		return protocol;
	}

	public void setProtocol(String protocol) {
		this.protocol = protocol;
	}
    // Explicit JavaBean accessors also support Spring binding without annotation processing.
    public String getHost() { return host; }
    public void setHost(String host) { this.host = host; }

    public int getPort() { return port; }
    public void setPort(int port) { this.port = port; }

    public String getDomain() { return domain; }
    public void setDomain(String domain) { this.domain = domain; }

    public String getBaseDn() { return baseDn; }
    public void setBaseDn(String baseDn) { this.baseDn = baseDn; }

    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }

    public int getConnectTimeoutMs() { return connectTimeoutMs; }
    public void setConnectTimeoutMs(int connectTimeoutMs) { this.connectTimeoutMs = connectTimeoutMs; }

    public int getReadTimeoutMs() { return readTimeoutMs; }
    public void setReadTimeoutMs(int readTimeoutMs) { this.readTimeoutMs = readTimeoutMs; }

    public boolean isConfigured() {
        return (!host.isBlank() || !url.isBlank()) && !domain.isBlank() 
        && !protocol.isBlank() && port > 0;
    }

    public void validate() {
		if (protocol.isBlank()) {
			throw new IllegalArgumentException(
			"SADGEO_LDAP_PROTOCOL nao configurado");
		}
		
		boolean usingUrl = !url.isBlank();
		boolean usingHost = !host.isBlank();
		if (!usingHost && !usingUrl) {
			throw new IllegalArgumentException(
				"Configure SADGEO_LDAP_HOST ou SADGEO_LDAP_URL");
		}

		if (usingHost) {

			if (port == 0) {
				throw new IllegalArgumentException(
					"SADGEO_LDAP_PORT nao configurado");
			}

			if (port < 1 || port > 65535) {
				throw new IllegalArgumentException(
					"SADGEO_LDAP_PORT deve estar entre 1 e 65535");
			}
		}
	
		if (!protocol.equalsIgnoreCase("ldap")  && !protocol.equalsIgnoreCase("ldaps")) {
			throw new IllegalArgumentException( "SADGEO_LDAP_PROTOCOL deve ser ldap ou ldaps");
		}
		
		if (connectTimeoutMs <= 0 || readTimeoutMs <= 0) 
			throw new IllegalArgumentException("Timeouts LDAP devem ser positivos");
        boolean hasServer = !host.isBlank() || !url.isBlank();
        if (hasServer != !domain.isBlank()) 
			throw new IllegalArgumentException("Configure servidor LDAP e SADGEO_LDAP_DOMAIN juntos");
        if (hasServer) effectiveUrl();
    }

    /** URL override keeps compatibility with existing deployments. Never allow plaintext LDAP. */
    public String effectiveUrl() {
        try {
            if (!url.isBlank()) {
                URI parsed = new URI(url);

				if (!"ldap".equalsIgnoreCase(parsed.getScheme())
					&& !"ldaps".equalsIgnoreCase(parsed.getScheme())) {
					throw new IllegalArgumentException( "SADGEO_LDAP_URL deve ser ldap:// ou ldaps://");
				}
                if (parsed.getHost() == null
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
            URI parsed = new URI(protocol, null, host, port, null, null, null);
            if (parsed.getHost() == null) throw new IllegalArgumentException("Hostname LDAP inválido");
            return parsed.toASCIIString();
        } catch (URISyntaxException e) {
            throw new IllegalArgumentException("Endereço LDAP inválido", e);
        }
    }
}
