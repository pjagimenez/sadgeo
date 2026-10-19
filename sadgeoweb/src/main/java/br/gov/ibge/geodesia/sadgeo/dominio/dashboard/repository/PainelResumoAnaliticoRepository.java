package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.PainelResumoAnaliticoEntity;

public interface PainelResumoAnaliticoRepository extends JpaRepository<PainelResumoAnaliticoEntity, Long> {
}