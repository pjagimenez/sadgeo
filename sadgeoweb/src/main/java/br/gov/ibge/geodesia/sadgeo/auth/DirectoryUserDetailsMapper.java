package br.gov.ibge.geodesia.sadgeo.auth;

import java.util.Arrays;
import java.util.Collection;
import java.util.Objects;
import java.util.stream.Collectors;
import org.springframework.ldap.core.DirContextOperations;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.ldap.userdetails.LdapUserDetails;
import org.springframework.security.ldap.userdetails.LdapUserDetailsMapper;

/** Maps attributes from the authenticated AD search result, without a second bind. */
public final class DirectoryUserDetailsMapper extends LdapUserDetailsMapper {
  @Override
  public UserDetails mapUserFromContext(
      DirContextOperations context,
      String username,
      Collection<? extends GrantedAuthority> authorities) {
    var original = (LdapUserDetails) super.mapUserFromContext(context, username, authorities);
    var values = context.getStringAttributes("description");
    String description =
        values == null
            ? ""
            : Arrays.stream(values)
                .filter(Objects::nonNull)
                .map(String::trim)
                .filter(value -> !value.isEmpty())
                .collect(Collectors.joining("; "));
    return DirectoryUserDetails.from(original, description);
  }
}
