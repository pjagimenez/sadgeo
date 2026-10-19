package br.gov.ibge.geodesia.sadgeo.registro.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import br.gov.ibge.geodesia.sadgeo.dominio.registro.entity.ItemEstacaoCampanhaEntity;
import br.gov.ibge.geodesia.sadgeo.dominio.registro.repository.ItemEstacaoCampanhaRepository;
import br.gov.ibge.geodesia.sadgeo.registro.EstacaoGridProjection;
import br.gov.ibge.geodesia.sadgeo.registro.dto.EstacaoGridDTO;

@org.springframework.context.annotation.Profile("!demo")
@Service
public class EstacaoItemCampanhaService {

	    public EstacaoItemCampanhaService(ItemEstacaoCampanhaRepository repository) {
		super();
		this.repository = repository;
	}

		private final ItemEstacaoCampanhaRepository repository;

	    public Page<EstacaoGridDTO> pesquisar(
	            String campanha,
	            String situacao,
	            Pageable pageable) {

	        validarFiltros(campanha, situacao);

	       
	        Page<EstacaoGridProjection> resultado =
	                repository.pesquisar(
	                        campanha,
	                        situacao,
	                        pageable);

	        return resultado.map(this::converter);
	    }

	    private EstacaoGridDTO converter(
	            EstacaoGridProjection p) {

	        return new EstacaoGridDTO(
	                p.getSeq(),
	                p.getCodigoEstacao(),
	                p.getMunicipio(),
	                p.getUf(),
	                p.getProjeto(),
	                p.getCampanha(),
	                p.getSituacaoMarcoPrincipal(),
	                p.getDataEntrada()
	        );
	    }

	    private void validarFiltros(
	            String campanha,
	            String situacao) {

	        if (campanha == null || campanha.isBlank()) {
	            throw new IllegalArgumentException(
	                    "Campanha é obrigatória.");
	        }

	        if (situacao == null || situacao.isBlank()) {
	            throw new IllegalArgumentException(
	                    "Situação é obrigatória.");
	        }
	    }

		public ItemEstacaoCampanhaEntity buscar(String seq) {
			// TODO Auto-generated method stub
			return null;
		}
	}