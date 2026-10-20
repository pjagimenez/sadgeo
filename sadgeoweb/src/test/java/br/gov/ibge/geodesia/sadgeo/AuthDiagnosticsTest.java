package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;

import br.gov.ibge.geodesia.sadgeo.auth.AuthDiagnostics;
import br.gov.ibge.geodesia.sadgeo.config.LdapProperties;
import java.net.*;
import javax.net.ssl.SSLHandshakeException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import org.springframework.mock.env.MockEnvironment;
import org.springframework.security.authentication.*;

@ExtendWith(OutputCaptureExtension.class)
class AuthDiagnosticsTest {
  @Test
  void distinguishesNestedTlsDnsTimeoutAndAccountFailures() {
    var communication = new javax.naming.CommunicationException("do-not-log-server");
    communication.setRootCause(new UnknownHostException("do-not-log-server"));
    assertEquals(
        "LDAP_DNS",
        AuthDiagnostics.reason(new AuthenticationServiceException("private", communication), true));
    communication.setRootCause(new SSLHandshakeException("private certificate message"));
    assertEquals(
        "LDAP_CERTIFICADO_TLS",
        AuthDiagnostics.reason(new AuthenticationServiceException("private", communication), true));
    assertEquals(
        "LDAP_TIMEOUT",
        AuthDiagnostics.reason(
            new AuthenticationServiceException("private", new SocketTimeoutException()), true));
    assertEquals(
        "LDAP_CONTA_BLOQUEADA", AuthDiagnostics.reason(new LockedException("private"), true));
    assertEquals(
        "LDAP_CREDENCIAIS", AuthDiagnostics.reason(new BadCredentialsException("private"), true));
    assertEquals(
        "LDAP_NAO_CONFIGURADO",
        AuthDiagnostics.reason(new AuthenticationServiceException("private"), false));
  }

  @Test
  void logsReferencesAndPresenceWithoutValuesOrExceptionMessages(CapturedOutput output) {
    var ldap = new LdapProperties();
    ldap.setHost("private-host-value");
    ldap.setDomain("private-domain-value");
    AuthDiagnostics.configuration(
        ldap, new MockEnvironment().withProperty("LDAP_HOST", "private-alias-value"));
    var failure =
        AuthDiagnostics.failure(
            new AuthenticationServiceException(
                "private-password-value", new SSLHandshakeException("private-token-value")),
            true);
    assertEquals(503, failure.status());
    assertEquals("LDAP_CERTIFICADO_TLS", failure.reason());
    assertTrue(output.getAll().contains(failure.diagnosticId()));
    assertTrue(output.getAll().contains("AUTH_CONFIG"));
    for (String value :
        new String[] {
          "private-host-value",
          "private-domain-value",
          "private-alias-value",
          "private-password-value",
          "private-token-value"
        }) assertFalse(output.getAll().contains(value));
  }
}
