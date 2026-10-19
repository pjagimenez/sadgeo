package br.gov.ibge.geodesia.sadgeo.dominio.registro.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import br.gov.ibge.geodesia.sadgeo.dominio.registro.entity.ItemEstacaoCampanhaEntity;
import br.gov.ibge.geodesia.sadgeo.registro.EstacaoGridProjection;

@Repository
public interface ItemEstacaoCampanhaRepository extends JpaRepository<ItemEstacaoCampanhaEntity, String> {
	@Query("""
			select
			    s.seq as seq,
			    s.codigoEstacao as codigoEstacao,
			    s.municipio as municipio,
			    s.uf as uf,
			    s.projeto as projeto,
			    s.campanha as campanha,
			    s.situacaoMarcoPrincipal as situacaoMarcoPrincipal,
			    s.dataEntrada as dataEntrada
			from SadgeoEntity s
			where s.campanha = :campanha
			  and s.situacaoMarcoPrincipal = :situacao
			""")
	Page<EstacaoGridProjection> pesquisar(String campanha, String situacao, Pageable pageable);

}
