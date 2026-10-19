package br.gov.ibge.geodesia.sadgeo.template.menu;

import java.util.ArrayList;
import java.util.List;

import com.vaadin.flow.component.Component;

public class MenuItem {

	private String titulo;
	private Class<? extends Component> view;
	private List<MenuItem> filhos;

	public MenuItem(String titulo, Class<? extends Component> view) {
		this.titulo = titulo;
		this.view = view;
		this.filhos = new ArrayList<>();
	}

	public MenuItem(String titulo) {
		this(titulo, null);
	}

	public void add(MenuItem filho) {
		filhos.add(filho);
	}

	public String getTitulo() {
		return titulo;
	}

	public Class<? extends Component> getView() {
		return view;
	}

	public List<MenuItem> getFilhos() {
		return filhos;
	}

}