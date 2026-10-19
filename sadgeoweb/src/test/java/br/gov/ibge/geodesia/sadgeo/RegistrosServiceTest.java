package br.gov.ibge.geodesia.sadgeo;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import br.gov.ibge.geodesia.sadgeo.dominio.dashboard.repository.FatoPainelRepository;
import br.gov.ibge.geodesia.sadgeo.registro.api.RegistrosService;
import org.junit.jupiter.api.Test;
import org.springframework.data.domain.Page;

class RegistrosServiceTest {
  @Test
  void realRepositoryReceivesFixedCampaignAndEscapedSearch() {
    var repository = mock(FatoPainelRepository.class);
    when(repository.pesquisarPainel(any(), any(), any(), any())).thenReturn(Page.empty());
    var result = new RegistrosService(repository).list("altimetria", 0, 25, "X%_", "P");
    verify(repository).pesquisarPainel(eq("medA"), eq("P"), eq("%x!%!_%"), any());
    assertEquals("medA", result.get("campanha"));
  }
}
