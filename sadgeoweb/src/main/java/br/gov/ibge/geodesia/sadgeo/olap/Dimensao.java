package br.gov.ibge.geodesia.sadgeo.olap;

public enum Dimensao {

	ANO("ano"), MES("mes"),

	CAMPANHA("campanha"), PROJETO("projeto"),

	UF("uf"), MUNICIPIO("municipio"),

	TIPO_LOCAL("tipoLocal"), UORG("uorgOrigem"),

	SITUACAO("situacao");

	private final String coluna;

	Dimensao(String coluna) {
		this.coluna = coluna;
	}

	public String coluna() {
		return coluna;
	}
}