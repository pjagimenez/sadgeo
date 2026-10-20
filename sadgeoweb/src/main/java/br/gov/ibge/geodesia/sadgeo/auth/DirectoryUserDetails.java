package br.gov.ibge.geodesia.sadgeo.auth;

import java.io.Serial;
import org.springframework.security.core.Authentication;
import org.springframework.security.ldap.ppolicy.PasswordPolicyData;
import org.springframework.security.ldap.userdetails.LdapUserDetails;
import org.springframework.security.ldap.userdetails.LdapUserDetailsImpl;

/** Session principal containing only the additional directory attribute used by the UI. */
public final class DirectoryUserDetails extends LdapUserDetailsImpl {
  @Serial private static final long serialVersionUID = 1L;
  private String description = "";

  private DirectoryUserDetails() {}

  public String getDescription() {
    return description;
  }

  public static DirectoryUserDetails from(LdapUserDetails original, String description) {
    var essence =
        new LdapUserDetailsImpl.Essence(original) {
          @Override
          protected LdapUserDetailsImpl createTarget() {
            return new DirectoryUserDetails();
          }
        };
    // The standard copy constructor does not copy password-policy information.
    if (original instanceof PasswordPolicyData policy) {
      essence.setTimeBeforeExpiration(policy.getTimeBeforeExpiration());
      essence.setGraceLoginsRemaining(policy.getGraceLoginsRemaining());
    }
    var result = (DirectoryUserDetails) essence.createUserDetails();
    result.description = description == null ? "" : description;
    return result;
  }

  public static String descriptionOf(Authentication authentication) {
    return authentication.getPrincipal() instanceof DirectoryUserDetails user
        ? user.getDescription()
        : "";
  }
}
