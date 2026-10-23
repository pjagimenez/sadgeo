package br.gov.ibge.geodesia.sadgeo.auth;

import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
import java.net.*;
import java.nio.file.Path;
import java.util.UUID;
import javax.net.ssl.SSLException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.env.Environment;
import org.springframework.security.authentication.*;
import org.springframework.security.core.AuthenticationException;

/**
 * Safe diagnostics: records presence and failure categories, never credentials or directory values.
 */
public final class AuthDiagnostics {
  private static final Logger LOG = LoggerFactory.getLogger(AuthDiagnostics.class);

  private AuthDiagnostics() {}

  public record Failure(String diagnosticId, String reason, int status) {}

  public static void configuration(LdapProperties ldap, Environment environment) {
    LOG.info(
        "AUTH_CONFIG configurada={} servidorInformado={} dominioInformado={} urlAlternativa={}"
            + " portaHost={} baseInformada={} connectTimeoutMs={} readTimeoutMs={}",
        ldap.isConfigured(),		
		ldap.getProtocol(),
        !ldap.getHost().isBlank(),
        !ldap.getDomain().isBlank(),
        !ldap.getUrl().isBlank(),
        ldap.getPort(),
        !ldap.getBaseDn().isBlank(),
        ldap.getConnectTimeoutMs(),
        ldap.getReadTimeoutMs());
    LOG.info(
        "AUTH_LOG arquivo={}",
        Path.of(environment.getProperty("logging.file.name", "logs/sadgeo.log"))
            .toAbsolutePath()
            .normalize());
    if (!ldap.isConfigured()
        && !environment.acceptsProfiles(org.springframework.core.env.Profiles.of("demo")))
      LOG.warn(
          "AUTH_CONFIG_INCOMPLETA: configure SADGEO_LDAP_HOST (ou SADGEO_LDAP_URL) e"
              + " SADGEO_LDAP_DOMAIN no processo Java. Arquivos .env nao sao carregados"
              + " automaticamente. Reinicie o backend apos alterar ENVVARs.");
    for (String name : new String[] {"LDAP_HOST", "LDAP_DOMAIN"}) {
      if (!environment.getProperty(name, "").isBlank())
        LOG.warn(
            "AUTH_VARIAVEL: {} foi detectada; o nome usado pelo SADGEO e SADGEO_{}.", name, name);
    }
  }

  public static String reason(Throwable error, boolean configured) {
    if (!configured) return "LDAP_NAO_CONFIGURADO";
    boolean connection = false, base = false;
    Throwable current = error;
    for (int depth = 0; current != null && depth < 20; depth++, current = current.getCause()) {
      if (current instanceof SSLException
          || current instanceof java.security.cert.CertificateException
          || current instanceof java.security.cert.CertPathBuilderException)
        return "LDAP_CERTIFICADO_TLS";
      if (current instanceof UnknownHostException) return "LDAP_DNS";
      if (current instanceof SocketTimeoutException) return "LDAP_TIMEOUT";
      if (current instanceof ConnectException
          || current instanceof org.springframework.ldap.CommunicationException
          || current instanceof javax.naming.CommunicationException) connection = true;
      if (current instanceof DisabledException) return "LDAP_CONTA_DESABILITADA";
      if (current instanceof LockedException) return "LDAP_CONTA_BLOQUEADA";
      if (current instanceof CredentialsExpiredException) return "LDAP_SENHA_EXPIRADA";
      if (current instanceof AccountExpiredException) return "LDAP_CONTA_EXPIRADA";
      if (current instanceof org.springframework.ldap.NameNotFoundException
          || current instanceof javax.naming.NameNotFoundException) base = true;
    }
    if (base) return "LDAP_BASE_BUSCA";
    if (connection) return "LDAP_CONEXAO";
    return error instanceof BadCredentialsException ? "LDAP_CREDENCIAIS" : "LDAP_SERVICO";
  }

  public static Failure failure(AuthenticationException error, boolean configured) {
    String id = UUID.randomUUID().toString(), reason = reason(error, configured);
    LOG.warn(
        "AUTH_LOGIN_FALHA referencia={} motivo={} tipo={}",
        id,
        reason,
        error.getClass().getSimpleName());
    return new Failure(id, reason, error instanceof AuthenticationServiceException ? 503 : 401);
  }

  public static void success(boolean descriptionPresent) {
    LOG.info(
        "AUTH_LOGIN_SUCESSO referencia={} descriptionPresente={}",
        UUID.randomUUID(),
        descriptionPresent);
  }
}
