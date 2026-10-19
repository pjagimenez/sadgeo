package br.gov.ibge.geodesia.sadgeo.dominio.registro.entity;

import org.locationtech.jts.geom.Point;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "T_SADGEO", schema = "BDG_VALIDA")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ItemEstacaoCampanhaEntity {

    // Base

    @Id
    @Column(name = "SEQ", nullable = false, length = 15)
    private String seq;

    @Column(name = "COD_ESTACAO", length = 9)
    private String codigoEstacao;

    @Column(name = "DSC_ESTACAO", length = 2000)
    private String descricaoEstacao;

    @Column(name = "MUNICIPIO", length = 60)
    private String municipio;

    @Column(name = "UF", length = 60)
    private String uf;

    @Column(name = "PROJETO", length = 8)
    private String projeto;

    @Column(name = "CAMPANHA", length = 6)
    private String campanha;

    @Column(name = "COD_CAMPANHA", length = 2)
    private String codigoCampanha;

    @Column(name = "DAT_ENTRADA")
    private LocalDateTime dataEntrada;

    @Column(name = "DAT_FIM_LEVANTAMENTO")
    private LocalDateTime dataFimLevantamento;

    @Column(name = "DAT_CRITICA")
    private LocalDateTime dataCritica;

    @Column(name = "DAT_ATUALIZACAO_BDG")
    private LocalDateTime dataAtualizacaoBDG;

    @Column(name = "COD_ATIVIDADE", length = 3)
    private String codigoAtividade;

    @Column(name = "TIPO_LOCAL", length = 2)
    private String tipoLocal;

    @Column(name = "DSC_LOCALIZACAO", length = 2000)
    private String descricaoLocalizacao;

    @Column(name = "DSC_ITINERARIO", length = 2000)
    private String descricaoItinerario;

    @Column(name = "DSC_OBSERVACAO", length = 2000)
    private String descricaoObservacao;

    @Column(name = "COD_SITUACAO_MARCO_PRINCIPAL", length = 2)
    private String situacaoMarcoPrincipal;

    @Column(name = "COD_SITUACAO_MARCO_AZIMUTE", length = 2)
    private String situacaoMarcoAzimute;

    @Column(name = "TIPO_MONUMENTACAO", length = 1)
    private String tipoMonumentacao;

    @Column(name = "INSCRICAO_CHAPA", length = 40)
    private String inscricaoChapa;

    @Column(name = "TIPO_CONEXAO", length = 12)
    private String tipoConexao;

    @Column(name = "NOMENCLAT_CONEX", length = 9)
    private String nomenclaturaConexao;

    @Column(name = "LINHA", length = 6)
    private String linha;

    @Column(name = "DSC_TRECHO", length = 60)
    private String descricaoTrecho;

    @Column(name = "CADERNETA", length = 5)
    private String caderneta;

    @Column(name = "RN_ANTERIOR", length = 9)
    private String rnAnterior;

    @Column(name = "CRITICO", length = 30)
    private String critico;

    @Column(name = "TP_SITUACAO_PAINEL", length = 30)
    private String tipoSituacaoPainel;

    @Column(name = "TP_UORG_ORIGEM", length = 30)
    private String tipoUorgOrigem;

    @Column(name = "STATUS_VRF", precision = 38, scale = 0)
    private BigInteger statusVrf;

    @Column(name = "STATUS_PENDENCIA", length = 2)
    private String statusPendencia;

    @Column(name = "PENDENCIA", length = 50)
    private String pendencia;

    @Column(name = "PENDENCIA_ATUAL", length = 50)
    private String pendenciaAtual;

    @Column(name = "INF_PEND_GGC", length = 1000)
    private String informacaoPendenciaGgc;

    @Column(name = "INF_PEND_PROJ", length = 1000)
    private String informacaoPendenciaProjeto;

    @Column(name = "EMAIL_CRITICO_GGC", length = 50)
    private String emailCriticoGgc;

    @Column(name = "INFORMANTE_DIGEO", length = 30)
    private String informanteDigeo;

    @Column(name = "IRREGULARIDADES", length = 2000)
    private String irregularidades;

    @Column(name = "CAMPO_ATUALIZAD", length = 33)
    private String campoAtualizado;

    @Column(name = "UNIDADE_ALOCADA", length = 20)
    private String unidadeAlocada;

    @Column(name = "DISPONIVEL_GGC", length = 1)
    private String disponivelGgc;

    @Column(name = "DISPONIVEL_PROJ", length = 1)
    private String disponivelProjeto;

    @Column(name = "ID_RESPOSTA_VEG", precision = 38, scale = 0)
    private BigInteger idRespostaVeg;

    // Anotador

    @Column(name = "ANOTADOR", length = 40)
    private String anotador;

    @Column(name = "UE_ANOTADOR", length = 2)
    private String ueAnotador;

    @Column(name = "AGENCIA_ANOTADOR", length = 50)
    private String agenciaAnotador;

    @Column(name = "SIAPE_ANOTADOR", length = 7)
    private String siapeAnotador;

    // Coordenadas

    @Column(name = "SINAL_LAT", length = 1)
    private String sinalLatitude;

    @Column(name = "GRAU_LAT", precision = 2, scale = 0)
    private Integer grauLatitude;

    @Column(name = "MIN_LAT", precision = 2, scale = 0)
    private Integer minutoLatitude;

    @Column(name = "SEG_LAT", precision = 8, scale = 6)
    private BigDecimal segundoLatitude;

    @Column(name = "SIGMA_LAT", precision = 6, scale = 4)
    private BigDecimal sigmaLatitude;

    @Column(name = "SINAL_LON", length = 1)
    private String sinalLongitude;

    @Column(name = "GRAU_LON", precision = 2, scale = 0)
    private Integer grauLongitude;

    @Column(name = "MIN_LON", precision = 2, scale = 0)
    private Integer minutoLongitude;

    @Column(name = "SEG_LON", precision = 8, scale = 6)
    private BigDecimal segundoLongitude;

    @Column(name = "SIGMA_LON", precision = 6, scale = 4)
    private BigDecimal sigmaLongitude;

    @Column(name = "DATUM", length = 2)
    private String datum;

    @Column(name = "COD_FONTE_COORD", length = 2)
    private String codigoFonteCoordenada;

    @Column(name = "OK_COORD", length = 1)
    private String coordenadaValidada;

    // GEOM: incluir o mapeamento de MDSYS.SDO_GEOMETRY
    // conforme a biblioteca espacial e a versão do Hibernate do projeto.

    // Ocupações

    @Column(name = "I_OCUPACAO_GPS", length = 1)
    private String ocupacaoGps;

    @Column(name = "I_OCUPACAO_GRAVIMETRO", length = 1)
    private String ocupacaoGravimetro;

    @Column(name = "I_OCUPACAO_NIVEL", length = 1)
    private String ocupacaoNivel;

    // Arquivos

    @Column(name = "NOM_ARQ", length = 50)
    private String nomeArquivo;

    @Column(name = "DAT_ARQ", length = 20)
    private String dataArquivo;

    @Column(name = "ARQSIR_FILENAME", length = 256)
    private String arquivoSirgas;

    @Column(name = "ARQSIR_CARREGADO", nullable = false, length = 1)
    private String arquivoSirgasCarregado;

    @Column(name = "ARQSIR_VAL_ALTITUDE_GEO", precision = 8, scale = 4)
    private BigDecimal arquivoSirgasValorAltitudeGeo;

    @Column(name = "ARQSIR_SIGMA_ALTITUDE", precision = 6, scale = 4)
    private BigDecimal arquivoSirgasSigmaAltitude;

    @Column(name = "ARQSIR_DAT_CALCULO")
    private LocalDateTime arquivoSirgasDataCalculo;

    // Fotos

    @Column(name = "TEM_FOTO", length = 1)
    private String possuiFoto;

    @Column(name = "TEM_FOTO_CHAPA", length = 1)
    private String possuiFotoChapa;

    @Column(name = "TEM_FOTO_SITUACAO", length = 1, columnDefinition = "CHAR(1)")
    private String possuiFotoSituacao;

    // Homologação

    @Column(name = "COD_APROVACAO", length = 1, columnDefinition = "CHAR(1)")
    private String codigoAprovacao;

    @Column(name = "DSC_REPROVACAO", length = 1000)
    private String descricaoReprovacao;

    @Column(name = "PROTOCOLO_HOMOLOG", length = 19)
    private String protocoloHomologacao;

    @Column(name = "ETAPA_PTA", length = 8)
    private String etapaPta;
    
    // Oracle JDBC reports the unqualified UDT name in DatabaseMetaData.
    // Keep Hibernate Spatial/JTS binding; match that name during schema validation.
    @Column(name = "GEOM", columnDefinition = "SDO_GEOMETRY")
    private Point geometria;
}