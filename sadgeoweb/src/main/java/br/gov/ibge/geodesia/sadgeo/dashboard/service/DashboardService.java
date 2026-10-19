package br.gov.ibge.geodesia.sadgeo.dashboard.service;

import java.util.List;
import java.util.Objects;

import org.springframework.stereotype.Service;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.EvolucaoAnualCampanhaProjetoUfDTO;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.EvolucaoAnualDTO;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.FatoPainelDTO;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.PainelResumoDTO;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.ResumoAnaliticoDTO;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.FatoPainelEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.PainelResumoAnaliticoEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.PainelResumoAnualEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.PainelResumoCampanhaAnualEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.FatoPainelRepository;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.PainelResumoAnaliticoRepository;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.PainelResumoAnualRepository;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.PainelResumoCampanhaAnualRepository;
import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.PainelResumoConsolidadoRepository;

@org.springframework.context.annotation.Profile("!demo")
@Service

public class DashboardService {

	private final PainelResumoConsolidadoRepository resumoRepository;

	private final PainelResumoAnualRepository anualRepository;

	private final FatoPainelRepository fatoPainelRepository;

	private final PainelResumoCampanhaAnualRepository campanhaAnualRepository;

	private final PainelResumoAnaliticoRepository analiticoRepository;

	public DashboardService(PainelResumoConsolidadoRepository resumoRepository,
			PainelResumoAnualRepository anualRepository, FatoPainelRepository fatoPainelRepository,
			PainelResumoCampanhaAnualRepository campanhaAnualRepository,
			PainelResumoAnaliticoRepository analiticoRepository) {

		this.resumoRepository = resumoRepository;
		this.anualRepository = anualRepository;
		this.fatoPainelRepository = fatoPainelRepository;
		this.campanhaAnualRepository = campanhaAnualRepository;
		this.analiticoRepository = analiticoRepository;
	}

	public PainelResumoDTO obterResumoAtual() {
		return resumoRepository.findAll().stream().findFirst().orElseThrow().toDTO();
	}

	public List<EvolucaoAnualDTO> obterEvolucaoAnual() {
		return anualRepository.findAllByOrderByAno().stream().map(PainelResumoAnualEntity::toDTO).toList();
	}

	public List<FatoPainelDTO> obterFatoPainel() {
		return fatoPainelRepository.findAll().stream().map(FatoPainelEntity::toDTO).toList();
	}

	public List<EvolucaoAnualCampanhaProjetoUfDTO> obterEvolucaoCampanhaAnual() {
		var lista = campanhaAnualRepository.findAll();

	    System.out.println("Qtd registros: " + lista.size());

	    lista.forEach(item -> {

	        if (item == null) {

	            System.out.println("ACHOU ITEM NULL");
	        }
	    });

	    return lista.stream()
	            .filter(Objects::nonNull)
	            .map(PainelResumoCampanhaAnualEntity::toDTO)
	            .toList();
	}

	public List<ResumoAnaliticoDTO> obterResumoAnalitico() {

		return analiticoRepository.findAll().stream().map(PainelResumoAnaliticoEntity::toDTO).toList();
	}
}