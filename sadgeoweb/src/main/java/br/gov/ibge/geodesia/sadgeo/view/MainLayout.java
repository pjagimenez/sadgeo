package br.gov.ibge.geodesia.sadgeo.view;

import java.util.List;

import com.vaadin.flow.component.applayout.AppLayout;
import com.vaadin.flow.component.applayout.DrawerToggle;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.sidenav.SideNav;
import com.vaadin.flow.component.sidenav.SideNavItem;

import br.gov.ibge.geodesia.sadgeo.common.component.AppVersaoProvider;
import br.gov.ibge.geodesia.sadgeo.template.menu.MenuBuilder;
import br.gov.ibge.geodesia.sadgeo.template.menu.MenuItem;

public class MainLayout extends AppLayout {

	private static final long serialVersionUID = 3533574209888642755L;

	/*
	 * ┌─────────────────────────────┐ │ SADGeo │ ├───────┬─────────────────────┤ │*
	 * Menu │ Dashboard │ │ │ CRUD │ │ │ Relatórios │
	 * └───────┴─────────────────────┘
	 */
	public MainLayout(AppVersaoProvider versionProvider) {

		addToNavbar(new DrawerToggle(), new H2("SADGeo"));

		SideNav nav = new SideNav();

		// Menu
		this.montarMenu(nav, MenuBuilder.build());

		Span rodape = this.montarRodape(versionProvider);

		VerticalLayout drawer = new VerticalLayout();

		drawer.setSizeFull();

		drawer.add(nav);

		drawer.expand(nav);

		drawer.add(rodape);

		addToDrawer(drawer);

	}

	private Span montarRodape(AppVersaoProvider versaoProvider) {

		Span versao = new Span("Versão " + versaoProvider.getVersion());

		versao.getStyle().set("font-size", "var(--lumo-font-size-s)").set("color", "gray");

		return versao;
	}

	private void montarMenu(SideNav nav, List<MenuItem> menus) {

		for (MenuItem item : menus) {

			SideNavItem navItem = new SideNavItem(item.getTitulo());

			if (item.getView() != null) {

				navItem = new SideNavItem(item.getTitulo(), item.getView());
			}

			for (MenuItem filho : item.getFilhos()) {

				if (filho.getView() != null) {
					navItem.addItem(new SideNavItem(filho.getTitulo(), filho.getView()));
				}
			}

			nav.addItem(navItem);
		}
	}
}