package br.gov.ibge.geodesia.sadgeo.common.component;

import com.vaadin.flow.component.combobox.ComboBox;

import br.gov.ibge.geodesia.sadgeo.common.dto.CodListDTO;

public class CodigoDescricaoComboBox extends ComboBox<CodListDTO> {

	private static final long serialVersionUID = 1L;

	public CodigoDescricaoComboBox(String label) {

		super(label);

		setItemLabelGenerator(CodListDTO::descricao);
	}

	public String getCodigoSelecionado() {

		return getValue() == null ? null : getValue().codigo();
	}
}