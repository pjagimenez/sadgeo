package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity.FatoPainelEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface FatoPainelRepository extends JpaRepository<FatoPainelEntity, String> {

  @Query(
      """
      select f from FatoPainelEntity f
      where (:campanha is null or f.campanha = :campanha)
        and (:projeto is null or f.projeto = :projeto)
        and (:q is null or lower(f.seq) like :q escape '!'
          or lower(f.campanha) like :q escape '!'
          or lower(f.projeto) like :q escape '!'
          or lower(f.municipio) like :q escape '!'
          or lower(f.uf) like :q escape '!'
          or lower(f.situacao) like :q escape '!')
      """)
  Page<FatoPainelEntity> pesquisarPainel(
      String campanha, String projeto, String q, Pageable pageable);
}
