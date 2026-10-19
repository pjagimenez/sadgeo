package br.gov.ibge.geodesia.sadgeo.common.component;

import org.springframework.boot.info.BuildProperties;
import org.springframework.stereotype.Component;

@Component

public class AppVersaoProvider {
	private final BuildProperties buildProperties;

	public AppVersaoProvider(BuildProperties buildProperties) {

		this.buildProperties = buildProperties;
	}

	public String getVersion() {

		return buildProperties.getVersion();
	}
}