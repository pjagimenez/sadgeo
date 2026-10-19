package br.gov.ibge.geodesia.sadgeo.olap.service;

import org.springframework.stereotype.Service;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.FatoPainelEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.FatoPainelRepository;

@org.springframework.context.annotation.Profile("!demo")
@Service
public class CubeProvider {

	private final SadgeoCube cube;

	public CubeProvider(FatoPainelRepository repository) {

		this.cube = new SadgeoCube(repository.findAll().stream().map(FatoPainelEntity::toDTO).toList());
	}

	public SadgeoCube getCube() {
		return cube;
	}
}