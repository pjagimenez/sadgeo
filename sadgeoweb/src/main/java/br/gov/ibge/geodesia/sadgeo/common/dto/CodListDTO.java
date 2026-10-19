package br.gov.ibge.geodesia.sadgeo.common.dto;

public record CodListDTO(

		String codigo,

		String descricao

) {

	@Override
	public String toString() {
		return descricao;
	}
}