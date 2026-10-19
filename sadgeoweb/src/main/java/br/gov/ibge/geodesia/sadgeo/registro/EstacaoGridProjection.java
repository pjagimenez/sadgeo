package br.gov.ibge.geodesia.sadgeo.registro;

import java.time.LocalDate;

public interface EstacaoGridProjection {

	String getSeq();

	String getCodigoEstacao();

	String getMunicipio();

	String getUf();

	String getProjeto();

	String getCampanha();

	String getSituacaoMarcoPrincipal();

	LocalDate getDataEntrada();

}