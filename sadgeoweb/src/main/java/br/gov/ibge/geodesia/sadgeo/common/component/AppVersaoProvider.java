package br.gov.ibge.geodesia.sadgeo.common.component;

import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import org.springframework.boot.info.BuildProperties;
import org.springframework.stereotype.Component;

@Component
public class AppVersaoProvider {
    private static final DateTimeFormatter BUILD_FORMAT = DateTimeFormatter
        .ofPattern("yyyyMMdd-HH").withZone(ZoneId.of("America/Sao_Paulo"));
    private final BuildProperties buildProperties;

    public AppVersaoProvider(BuildProperties buildProperties) { this.buildProperties = buildProperties; }

    public String getVersion() {
        // Use the immutable build timestamp, never the current request/startup time.
        if (buildProperties.getTime() == null) return "0.1.sem-build";
        return "0.1." + BUILD_FORMAT.format(buildProperties.getTime());
    }
}
