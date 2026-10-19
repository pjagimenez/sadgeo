package br.gov.ibge.geodesia.sadgeo.dashboard.dto;

import java.time.LocalDate;

public record PainelResumoDTO(

		Long total,

		Long naoCriticado,

		Long retidoCampo,

		Long liberadoCampo,

		Long criticadoCampo,

		Long retidoProjeto,

		Long liberadoProjeto,

		Long criticadoProjeto,

		Long atualizadoBdg,

		Long reservadoGabinete,

		LocalDate dtPrimeiroLevantamento,

		LocalDate dtUltimoLevantamento


) {
}