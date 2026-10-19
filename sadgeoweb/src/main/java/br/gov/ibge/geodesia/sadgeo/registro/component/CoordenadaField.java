package br.gov.ibge.geodesia.sadgeo.registro.component;

import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.textfield.IntegerField;
import com.vaadin.flow.component.textfield.NumberField;
import com.vaadin.flow.component.textfield.TextField;

public class CoordenadaField
extends HorizontalLayout {

	private static final long serialVersionUID = 1L;
TextField sinal = new TextField();
IntegerField graus = new IntegerField();
IntegerField minutos = new IntegerField();
NumberField segundos = new NumberField();

public CoordenadaField(String titulo){

add(
    new Span(titulo),
    sinal,
    graus,
    minutos,
    segundos
);
}
}