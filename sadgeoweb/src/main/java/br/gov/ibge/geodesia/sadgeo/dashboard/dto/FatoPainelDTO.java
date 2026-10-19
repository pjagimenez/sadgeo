package br.gov.ibge.geodesia.sadgeo.dashboard.dto;

import java.time.LocalDate;

public record FatoPainelDTO(

		String seq,

		Integer anoLevantamento,

		Integer mesLevantamento,

		LocalDate dataLevantamento,

		String campanha,

		String projeto,

		String uf,

		String municipio,

		String tipoLocal,

		String uorgOrigem,

		String situacao,

		Integer contagem,

		Integer diasAteEntrada,

		Integer diasAteCritica,

		Integer diasAtePublicacao,

		Integer diasAteCalculoCoord

) {
}