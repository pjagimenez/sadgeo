package br.gov.ibge.geodesia.sadgeo.common.component;

import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import org.springframework.boot.info.BuildProperties;
import org.springframework.stereotype.Component;

@Component
public class AppVersaoProvider {
  private static final DateTimeFormatter BUILD_FORMAT =
      DateTimeFormatter.ofPattern("yyyyMMdd-HH").withZone(ZoneId.of("America/Sao_Paulo"));
  private final BuildProperties buildProperties;

  public AppVersaoProvider(BuildProperties buildProperties) {
    this.buildProperties = buildProperties;
  }

  public String getVersion() {
    // Use the immutable build timestamp, never the current request/startup time.
    String release = buildProperties.getVersion();
    String line = release == null ? "0.2" : release.replaceFirst("^(\\d+\\.\\d+).*", "$1");
    if (buildProperties.getTime() == null) return line + ".sem-build";
    return line + "." + BUILD_FORMAT.format(buildProperties.getTime());
  }
}
