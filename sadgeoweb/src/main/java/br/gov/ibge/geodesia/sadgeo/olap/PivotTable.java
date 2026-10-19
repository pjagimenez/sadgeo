package br.gov.ibge.geodesia.sadgeo.olap;

import java.util.List;
import java.util.Map;

public record PivotTable(

        List<String> categorias,

        Map<String, List<Double>> series

) {
}