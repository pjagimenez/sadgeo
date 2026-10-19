package br.gov.ibge.geodesia.sadgeo.registro;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;

import br.gov.ibge.geodesia.sadgeo.dominio.registro.entity.ItemEstacaoCampanhaEntity;
import br.gov.ibge.geodesia.sadgeo.registro.component.EstacaoDrawer;
import br.gov.ibge.geodesia.sadgeo.registro.dto.EstacaoGridDTO;
import br.gov.ibge.geodesia.sadgeo.registro.service.EstacaoItemCampanhaService;

@Route("registro-campanha")
@PageTitle("Registros de Campanha")
public class EstacaoItemCampanhaView extends VerticalLayout {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private final EstacaoItemCampanhaService service;

	private Grid<EstacaoGridDTO> grid;

	private ComboBox<String> campanha;
	private ComboBox<String> situacao;
	private ComboBox<String> projeto;
	private ComboBox<String> uf;
	private ComboBox<String> municipio;

	private EstacaoDrawer editorDrawer;

	public EstacaoItemCampanhaView(EstacaoItemCampanhaService service) {

		this.service = service;

		setSizeFull();
		setPadding(false);
		setSpacing(false);

		// editorDrawer = new EstacaoDrawer();

		add(criarPainelFiltros(), criarToolbar(), criarGrid());
	}

	private Component criarPainelFiltros() {

		campanha = new ComboBox<>("Campanha *");
		situacao = new ComboBox<>("Situação *");

		projeto = new ComboBox<>("Projeto");

		uf = new ComboBox<>("UF");
		municipio = new ComboBox<>("Município");

		Button pesquisar = new Button("Pesquisar", VaadinIcon.SEARCH.create());

		Button limpar = new Button("Limpar", VaadinIcon.ERASER.create());

		FormLayout filtros = new FormLayout();

		filtros.add(campanha, situacao, projeto, uf, municipio, pesquisar, limpar);

		filtros.setResponsiveSteps(new FormLayout.ResponsiveStep("0", 1), new FormLayout.ResponsiveStep("900px", 3),
				new FormLayout.ResponsiveStep("1300px", 6));

		pesquisar.addClickListener(e -> pesquisar());

		limpar.addClickListener(e -> limpar());

		return filtros;
	}

	private Component criarToolbar() {

		Button novo = new Button("Nova Estação", VaadinIcon.PLUS.create());

		// novo.addClickListener(event -> editorDrawer.novaEstacao());

		HorizontalLayout layout = new HorizontalLayout(novo);

		layout.setWidthFull();

		return layout;
	}

	private Component criarGrid() {

		grid = new Grid<>(EstacaoGridDTO.class, false);

		grid.addColumn(EstacaoGridDTO::codigoEstacao).setHeader("Estação");

		grid.addColumn(EstacaoGridDTO::municipio).setHeader("Município");

		grid.addColumn(EstacaoGridDTO::uf).setHeader("UF");

		grid.addColumn(EstacaoGridDTO::projeto).setHeader("Projeto");

		grid.addColumn(EstacaoGridDTO::campanha).setHeader("Campanha");

		grid.addColumn(EstacaoGridDTO::situacao).setHeader("Situação");

		grid.addComponentColumn(dto -> {

			Button editar = new Button(VaadinIcon.EDIT.create());

			editar.addClickListener(event -> abrirDrawer(dto.seq()));

			return editar;
		});

		grid.addItemDoubleClickListener(event -> abrirDrawer(event.getItem().seq()));

		grid.setSizeFull();

		return grid;
	}

	private void limpar() {

	    campanha.clear();
	    situacao.clear();
	    projeto.clear();
	    uf.clear();
	    municipio.clear();

	    grid.setItems(List.of());
	}
	
	private void pesquisar() {

		if (campanha.isEmpty()) {

			Notification.show("Informe a campanha");

			return;
		}

		if (situacao.isEmpty()) {

			Notification.show("Informe a situação");

			return;
		}

		PageRequest page =
	            PageRequest.of(
	                    0,
	                    25,
	                    Sort.by("codigoEstacao"));

	    Page<EstacaoGridDTO> resultado =
	            service.pesquisar(
	                    campanha.getValue(),
	                    situacao.getValue(),
	                    page);

	    grid.setItems(
	            resultado.getContent());
	}

	private void abrirDrawer(String seq) {

		ItemEstacaoCampanhaEntity entity = service.buscar(seq);

		//editorDrawer.editar(entity);

		//editorDrawer.open();
	}

}