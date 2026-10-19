package br.gov.ibge.geodesia.sadgeo.registro.dto;

import java.time.LocalDate;

public record EstacaoGridDTO(

		String seq, String codigoEstacao, String municipio, String uf, String projeto, String campanha, String situacao,
		LocalDate dataEntrada) {
}
