package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.PainelResumoAnualEntity;

public interface PainelResumoAnualRepository extends JpaRepository<PainelResumoAnualEntity, Integer> {

	List<PainelResumoAnualEntity> findAllByOrderByAno();

	PainelResumoAnualEntity findTopByOrderByAnoDesc();

}