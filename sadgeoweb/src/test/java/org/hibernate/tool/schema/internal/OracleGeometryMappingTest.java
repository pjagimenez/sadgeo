package org.hibernate.tool.schema.internal;

import java.sql.Types;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.dialect.OracleDialect;
import org.hibernate.tool.schema.extract.spi.ColumnInformation;
import org.hibernate.type.SqlTypes;
import org.junit.jupiter.api.Test;
import br.gov.ibge.geodesia.sadgeo.dominio.registro.entity.ItemEstacaoCampanhaEntity;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/** Exercises Hibernate's actual schema type comparison without requiring an Oracle server. */
class OracleGeometryMappingTest {
    @Test void acceptsOracleStructMetadataAndKeepsSpatialBinding() {
        var registry = new StandardServiceRegistryBuilder()
            .applySetting("hibernate.dialect", "org.hibernate.dialect.OracleDialect")
            .applySetting("hibernate.boot.allow_jdbc_metadata_access", "false")
            .build();
        try {
            var metadata = new MetadataSources(registry).addAnnotatedClass(ItemEstacaoCampanhaEntity.class).buildMetadata();
            var entity = metadata.getEntityBinding(ItemEstacaoCampanhaEntity.class.getName());
            var column = entity.getProperty("geometria").getValue().getColumns().get(0);
            assertEquals(SqlTypes.GEOMETRY, column.getSqlTypeCode(metadata));
            var reported = mock(ColumnInformation.class);
            when(reported.getTypeCode()).thenReturn(Types.STRUCT);
            when(reported.getTypeName()).thenReturn("SDO_GEOMETRY");
            assertTrue(ColumnDefinitions.hasMatchingType(column, reported, metadata, new OracleDialect()));
            when(reported.getTypeCode()).thenReturn(Types.VARCHAR);
            when(reported.getTypeName()).thenReturn("VARCHAR2");
            assertFalse(ColumnDefinitions.hasMatchingType(column, reported, metadata, new OracleDialect()));
        } finally { StandardServiceRegistryBuilder.destroy(registry); }
    }
}
