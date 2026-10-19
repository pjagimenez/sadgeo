package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.PainelResumoConsolidadoEntity;

public interface PainelResumoConsolidadoRepository extends JpaRepository<PainelResumoConsolidadoEntity, Long> {
}