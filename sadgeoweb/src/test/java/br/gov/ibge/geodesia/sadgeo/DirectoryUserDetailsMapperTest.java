package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;

import br.gov.ibge.geodesia.sadgeo.auth.*;
import java.io.*;
import java.util.List;
import javax.naming.ldap.LdapName;
import org.junit.jupiter.api.Test;
import org.springframework.ldap.core.DirContextAdapter;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.ldap.userdetails.LdapUserDetailsImpl;

class DirectoryUserDetailsMapperTest {
  private DirContextAdapter context() throws Exception {
    var context = new DirContextAdapter();
    context.setDn(new LdapName("CN=usuario,DC=example,DC=org"));
    return context;
  }

  @Test
  void readsDescriptionWithoutReplacingUsernameOrAuthorities() throws Exception {
    var context = context();
    context.setAttributeValue("description", "Equipe de Geodésia — Campo");
    context.setAttributeValue("userPassword", "only-a-unit-test-password");
    var mapper = new DirectoryUserDetailsMapper();
    mapper.setPasswordAttributeName("userPassword");
    var authorities = List.of(new SimpleGrantedAuthority("ROLE_CONSULTA"));
    var user =
        (DirectoryUserDetails)
            mapper.mapUserFromContext(context, "usuario@example.org", authorities);
    assertEquals("Equipe de Geodésia — Campo", user.getDescription());
    assertEquals("usuario@example.org", user.getUsername());
    assertEquals(authorities, List.copyOf(user.getAuthorities()));
    assertEquals(context.getDn().toString(), user.getDn());
    assertNotNull(user.getPassword());
    user.eraseCredentials();
    assertNull(user.getPassword());
    assertEquals("Equipe de Geodésia — Campo", user.getDescription());
  }

  @Test
  void missingBlankAndMultivaluedDescriptionsDoNotBreakAuthentication() throws Exception {
    var context = context();
    var mapper = new DirectoryUserDetailsMapper();
    var authorities = List.of(new SimpleGrantedAuthority("ROLE_CONSULTA"));
    assertEquals(
        "",
        ((DirectoryUserDetails) mapper.mapUserFromContext(context, "usuario", authorities))
            .getDescription());
    context.setAttributeValues("description", new String[] {"  ", "Equipe A", "Geodésia B"});
    assertEquals(
        "Equipe A; Geodésia B",
        ((DirectoryUserDetails) mapper.mapUserFromContext(context, "usuario", authorities))
            .getDescription());
  }

  @Test
  void preservesFlagsPasswordPolicyAndDescriptionAcrossSessionSerialization() throws Exception {
    var source = new LdapUserDetailsImpl.Essence();
    source.setDn("CN=usuario,DC=example,DC=org");
    source.setUsername("usuario");
    source.setEnabled(false);
    source.setAccountNonExpired(false);
    source.setAccountNonLocked(false);
    source.setCredentialsNonExpired(false);
    source.addAuthority(new SimpleGrantedAuthority("ROLE_CONSULTA"));
    source.setTimeBeforeExpiration(120);
    source.setGraceLoginsRemaining(2);
    var user = DirectoryUserDetails.from(source.createUserDetails(), "Equipe de Geodésia");
    var bytes = new ByteArrayOutputStream();
    try (var out = new ObjectOutputStream(bytes)) {
      out.writeObject(user);
    }
    DirectoryUserDetails restored;
    try (var in = new ObjectInputStream(new ByteArrayInputStream(bytes.toByteArray()))) {
      restored = (DirectoryUserDetails) in.readObject();
    }
    assertEquals("Equipe de Geodésia", restored.getDescription());
    assertFalse(restored.isEnabled());
    assertFalse(restored.isAccountNonExpired());
    assertFalse(restored.isAccountNonLocked());
    assertFalse(restored.isCredentialsNonExpired());
    assertEquals(120, restored.getTimeBeforeExpiration());
    assertEquals(2, restored.getGraceLoginsRemaining());
    assertEquals(user.getAuthorities(), restored.getAuthorities());
  }
}
