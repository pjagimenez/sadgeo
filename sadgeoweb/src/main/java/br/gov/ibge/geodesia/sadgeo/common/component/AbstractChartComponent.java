package br.gov.ibge.geodesia.sadgeo.common.component;

import java.util.List;

public abstract class AbstractChartComponent<T>
        extends EchartsComponent {

    private static final long serialVersionUID = 1L;

    protected AbstractChartComponent(
            List<T> dados) {

        super("");
        atualizar(dados);
    }

    public void atualizar(
            List<T> dados) {

        setOption(
                montarOption(dados));
    }

    protected abstract String montarOption(
            List<T> dados);
}