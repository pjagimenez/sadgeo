package br.gov.ibge.geodesia.sadgeo.dashboard.dto;

public record ResumoAnaliticoDTO(

	    Integer ano,

	    String campanha,

	    String projeto,

	    String uf,

	    String situacao,

	    Long contagem,

	    Double mediaDiasLevantamentoAteEntrada,

	    Double mediaDiasEntradaAteCritica,

	    Double mediaDiasEntradadiasAtePublicacao,

	    Double mediaDiasLevantamentoAteCalculoCoordenadas

	) {
	}