package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.FatoPainelEntity;

@Repository
public interface FatoPainelRepository
        extends JpaRepository<FatoPainelEntity, String> {

}