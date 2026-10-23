--delete from bdg_Valida.t_sadgeo where  cod_estacao  in ('99920','99921','99922','99923');

select *
--cod_estacao, municipio, uf, datum, ue_anotador,  unidade_alocada, COD_FONTE_COORD, nom_arq, status_vrf, anotador, critico, etapa_pta, agencia_anotador, critico, status_vrf,  disponivel_ggc, disponivel_proj
from bdg_valida.t_sadgeo where cod_estacao  in ('99919','99920','99921','99922','99923');

select * from bdg_Valida.t_estacao where  cod_estacao  in ('99919','99920','99921','99922','99923');

select * from BDG_VALIDA.usuario_sadgeoweb where dat_desativacao is null order by 2;

select * from bdg_valida.t_sadgeo where status_vrf = 3;
select * from bdg.t_portal_usuario;

SELECT  distinct	'S',u.*
			FROM	bdg.t_portal_usuario u, bdg.t_portal_usuario_perfil up, 
					bdg.t_portal_perfil_acao pa, bdg.t_portal_acao a
			WHERE	--u.nm_login = 'mairalima'
			--AND	
            u.id_usuario = up.id_usuario
			AND		up.dt_ini <= sysdate AND (up.dt_fim > sysdate or up.dt_fim IS NULL)
			AND		up.id_perfil = pa.id_perfil
			AND		pa.dt_ini <= sysdate AND (pa.dt_fim > sysdate or pa.dt_fim IS NULL)
			AND		pa.id_acao = a.id_acao
			AND 	a.nm_acao = 'carregar_gps';

*/

	SELECT 'S' INTO v_existe FROM bdg_valida.t_projeto WHERE cod_projeto = registro_sadgeo.projeto;
  
  
 
select * from bdg_valida.t_manager_mviews_pub;

 -- Sinalizar a pendência para REFRESH
UPDATE 	bdg_valida.t_manager_mviews_pub     SET	st_controle = 1;
    
execute "BDG_VALIDA"."P_MANAGER_MVIEWS_PUB";

/*
 
set SERVEROUTPUT ON
DECLARE
    v_login   VARCHAR2(50) := 'fernanda.torres';  -- Defina o login apropriado
    v_seq     VARCHAR2(15) := '180880-25';            -- Defina a sequência correspondente
    v_retorno varchar2(200);  -- Variável para armazenar o retorno da procedure
BEGIN
    -- Chamada da procedure
    BDG_VALIDA.K_SADGEO_GPS_2023.P_EFETIVAR_CARGA_BDG(
        v_login,
        v_seq,
        v_retorno
    );

    -- Exibir o retorno para debug
    DBMS_OUTPUT.PUT_LINE('Retorno da procedure: ' || v_retorno);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Erro ao executar a procedure: ' || SQLERRM);
END;
/

update bdg_Valida.t_sadgeo set tipo_monumentacao = 'M' where  cod_estacao  in ('99920','99921','99922','99923');


RESULTADOS FINAIS EM SIRGAS2000
PROJETO GYN04_GO
DATA DE CALCULO 17/02/2025


 IDENTIFI.     LATITUDE        DESVIO     LONGITUDE       DESVIO   ALTITUDE  ONDULA.  ALTITUDE  DESVIO    DATA DA
                               PADRÃO                     PADRÃO   ORTOMETR. GEOIDAL  GEOMETR.  PADRÃO    MEDIÇÃO  PROJETO
              (GG MM SS.SSSS)  (METROS)  (GG MM SS.SSSS)  (METROS) (METROS)  (METROS) (METROS)  (METROS)
--------------------------------------------------------------------------------------------------------------------------
  99920      S 16 27 45.259239   0.0026M   W 49 12  5.955388   0.0046M  0000.00   0000.00   801.3020   0.0137M  24/01/2025  GYN04_GO
  99921      S 16 44 12.387724   0.0025M   W 49 09 54.042969   0.0046M  0000.00   0000.00   732.2611   0.0136M  24/01/2025  GYN04_GO
  99922      S 16 40 56.317392   0.0031M   W 49 19 56.779446   0.0056M  0000.00   0000.00   723.9414   0.0166M  24/01/2025  GYN04_GO
  99923      S 16 47 18.706181   0.0033M   W 49 22 30.905870   0.0057M  0000.00   0000.00   848.2076   0.0171M  24/01/2025  GYN04_GO





update bdg_valida.t_sadgeo set dat_critica = to_date('06/03/2025','DD/MM/YYYY'), status_vrf =3, ok_coord=2, disponivel_proj='S',protocolo_homolog = 'GYN04_GO', arqsir_carregado = 'S', arqsir_filename = 'b_dados.sir', 
        arqsir_dat_calculo = to_date('17/02/2025','DD/MM/YYYY'), sigma_lat = 0.0033, sigma_lon= 0.0057, arqsir_val_altitude_geo= 848.2076, arqsir_sigma_altitude=0.0171
    where cod_estacao = '99923';

update bdg_valida.t_sadgeo set dat_critica = to_date('06/03/2025','DD/MM/YYYY'), status_vrf =3, ok_coord=2, disponivel_proj='S',protocolo_homolog = 'GYN04_GO', arqsir_carregado = 'S', arqsir_filename = 'b_dados.sir', 
        arqsir_dat_calculo = to_date('17/02/2025','DD/MM/YYYY'), sigma_lat = 0.0031, sigma_lon= 0.0056, arqsir_val_altitude_geo= 723.9414, arqsir_sigma_altitude=0.0166
    where cod_estacao = '99922';


update bdg_valida.t_sadgeo set dat_critica = to_date('06/03/2025','DD/MM/YYYY'), status_vrf =3, ok_coord=2, disponivel_proj='S',protocolo_homolog = 'GYN04_GO', arqsir_carregado = 'S', arqsir_filename = 'b_dados.sir', 
        arqsir_dat_calculo = to_date('17/02/2025','DD/MM/YYYY'), sigma_lat = 0.0025, sigma_lon= 0.0046, arqsir_val_altitude_geo= 732.2611, arqsir_sigma_altitude=0.0136
    where cod_estacao = '99921';

update bdg_valida.t_sadgeo set dat_critica = to_date('06/03/2025','DD/MM/YYYY'), status_vrf =3, ok_coord=2, disponivel_proj='S',protocolo_homolog = 'GYN04_GO', arqsir_carregado = 'S', arqsir_filename = 'b_dados.sir', 
        arqsir_dat_calculo = to_date('17/02/2025','DD/MM/YYYY'), sigma_lat = 0.0026, sigma_lon= 0.0046, arqsir_val_altitude_geo= 801.3020, arqsir_sigma_altitude=0.0137
    where cod_estacao = '99920';
        
/*

set SERVEROUTPUT ON
DECLARE
    -- Variáveis para armazenar os dados do CSV
    v_cod_estacao                 VARCHAR2(9);
    v_munic                       VARCHAR2(60);
    v_uf                          VARCHAR2(2);
    v_dsc_estacao                 VARCHAR2(2000);
    v_tipo_local                  VARCHAR2(2);
    v_tipo_monumentacao           VARCHAR2(1);
    v_i_ocupacao_gps              VARCHAR2(1);
    v_i_ocupacao_gravim           VARCHAR2(1);
    v_i_ocupacao_nivel            VARCHAR2(1);
    v_inscricao                   VARCHAR2(40);
    v_sinal_lat                   VARCHAR2(1);
    v_grau_lat                    NUMBER(2,0);
    v_min_lat                     NUMBER(2,0);
    v_seg_lat                     NUMBER(8,6);
    v_grau_lon                    NUMBER(2,0);
    v_min_lon                     NUMBER(2,0);
    v_seg_lon                     NUMBER(8,6);
    v_datum                       VARCHAR2(2);
    v_dsc_localizacao             VARCHAR2(2000);
    v_dsc_itinerario              VARCHAR2(2000);
    v_dsc_observacao              VARCHAR2(2000);
    v_data_lev                    DATE;
    v_anotador                    VARCHAR2(40);
    v_siape                       VARCHAR2(7);
    v_ue_anotador                 VARCHAR2(2);
    v_unidade                     VARCHAR2(20);
    v_irregularidades             VARCHAR2(2000);
    v_projeto                     VARCHAR2(8);
    v_campanha                    VARCHAR2(6);
    v_cod_situacao_marco_principal VARCHAR2(2);
    v_tipo_conexao                VARCHAR2(12);
    v_nomenclat_conex             VARCHAR2(9);
    v_caderneta                   VARCHAR2(5);
    v_linha                       VARCHAR2(6);
    v_rn_anterior                 VARCHAR2(9);
    v_fonte                       VARCHAR2(2);
    v_nom_arq                     VARCHAR2(50);
    v_status                      NUMBER(38,0);
    v_login                       VARCHAR2(50);
    v_etapa_comp                  VARCHAR2(8);

    -- Cursor para simular a leitura do CSV (SUBSTITUA PELO CURSOR REAL)
    CURSOR c_dados IS
        
        select * from
        (
select '99920' as codEstacao,'T' as monumentacao, 'OU' as tipo_local, 'GYN-001' as inscrChapa,'10' as situacao, null as conexao,null as tipo_conexao, null as rn_anterior,'medP' as campanha,
to_date('24/01/2025','DD/MM/YYYY') as data_levantamento, to_date('06/03/2025','DD/MM/YYYY') as data_critica, 'P2000017' as projeto, '20249999' as nue, null as linha, null as caderneta,
'Fernanda Magri Torres' as informante, '2334986' as siape,
'-' as lat_sinal,16  as lat_grau,27 as lat_min,45.259239 as lat_seg,'-' as lon_sinal,49 as lon_grau,12 as lon_min,5.955388 as lon_seg,'S' as is_ocup_gps, 'N' as is_ocup_mira, 'N' as is_ocup_gravimetro,
'Marco de concreto na forma de tronco piramidal com altura de 40cm e base quadrangular de 30 cm e topo quadrangular de 18cm, com uma chapa de alumínio cravada no topo contendo a inscrição:  GYN-001 - P. M. GOIÂNIA - TOPOCART - PROTEGIDO POR LEI?.' as descricao,
'O marco fica localizado no Distrito de Vila Rica à  331 m de distância da Escola Municipal José Carlos Pimenta, implantado próximo à  GO-466 em frente ao Residencial Tatyane.' as localizacao,
'' as itinerario,'Homologação de marco' as observacao
from dual
union all
select '99921','T','RO','GYN-006','10',null, null, null,'medP',to_date('24/01/2025','DD/MM/YYYY'),to_date('06/03/2025','DD/MM/YYYY'),'P2000017','20249999',null,null,'Fernanda Magri Torres','2334986',
'-',16,44,12.387724,'-',49,9,54.042969,'S','N','N',
'Marco de concreto na forma de tronco piramidal com altura de 40cm e base quadrangular de 30 cm e topo quadrangular de 18cm, com uma chapa de alumínio cravada no topo contendo a inscrição:  GYN-006 - P. M. GOIÂNIA - TOPOCART - PROTEGIDO POR LEI.',
'O marco fica localizado proximo Ã  BR-352 na entrada do Portal do Sol Golfe Residence.',null,'Homologação de marco'
from dual 
union all
select '99922','T','PU','GYN-015','10',null,null,null,'medP',to_date('24/01/2025','DD/MM/YYYY'),to_date('06/03/2025','DD/MM/YYYY'),'P2000017','20249999',null,null,'Fernanda Magri Torres','2334986',
'-',16,40,56.317392,'-',49,19,56.779446,'S','N','N',
'Marco de concreto na forma de tronco piramidal com altura de 40cm e base quadrangular de 30 cm e topo quadrangular de 18cm, com uma chapa de alumínio cravada no topo contendo a inscrição:  GYN-015 - P. M. GOIÂNIA - TOPOCART - PROTEGIDO POR LEI?.',
'O marco fica localizado no canteiro central entre a Av. Leste Oeste e Rua Félix de Bulhões, próximo ao Condomínio Morada Goiás I e está à  560 m de distância do Bretas Atacarejo - Bairro Goiás.',null,'Homologação de marco'
from dual 
union all
select '99923','T','PU','GYN-019','10',null,null,null,'medP',to_date('24/01/2025','DD/MM/YYYY'),to_date('06/03/2025','DD/MM/YYYY'),'P2000017','20249999',null,null,'Fernanda Magri Torres','2334986',
'-',16,47,18.706181,'-',49,22,30.905870,'S','N','N',
'Marco de concreto na forma de tronco piramidal com altura de 40cm e base quadrangular de 30 cm e topo quadrangular de 18cm, com uma chapa de alumínio cravada no topo contendo a inscrição:  GYN-019 - P. M. GOIÂNIA - TOPOCART - PROTEGIDO POR LEI?.',
'O marco fica localizado no Residencial Itaipú, próximo à Rua Ri 15 na praça Ri 16.',null,'Homologação de marco'
from dual
) t;
/*
data_critica
observacao
*/
BEGIN
            DBMS_OUTPUT.PUT_LINE('Inicio...');
   
    FOR rec IN c_dados LOOP
    
        
        -- Atribuir valores do CSV às variáveis
        v_cod_estacao                 := rec.codEstacao;
        
        
             DBMS_OUTPUT.PUT_LINE('Registro analise: ' || v_cod_estacao);
   
        v_munic                       := 'Goiânia'; --rec. munic
        v_uf                          := 'GO'; --rec.uf
        v_dsc_estacao                 := rec.descricao;
        v_tipo_local                  := rec.tipo_local;
        v_tipo_monumentacao           := rec.monumentacao;
        v_i_ocupacao_gps              := rec.is_ocup_gps;
        v_i_ocupacao_gravim           := rec.is_ocup_gravimetro;
        v_i_ocupacao_nivel            := rec.is_ocup_mira;
        v_inscricao                   := rec.inscrChapa;
        v_sinal_lat                   := rec.lat_sinal;
        v_grau_lat                    := rec.lat_grau;
        v_min_lat                     := rec.lat_min;
        v_seg_lat                     := rec.lat_seg;
        v_grau_lon                    := rec.lon_grau;
        v_min_lon                     := rec.lon_min;
        v_seg_lon                     := rec.lon_seg;
        v_datum                       := '06'; --rec. datum
        v_dsc_localizacao             := rec.localizacao;
        v_dsc_itinerario              := rec.itinerario;
        v_dsc_observacao              := rec.observacao;
        v_data_lev                    := rec.data_levantamento;
        v_anotador                    := rec.informante;
        v_siape                       := rec.siape;
        v_ue_anotador                 := 'GO'; --rec. ue_anotador
        v_unidade                     := 'GGC-GO'; --rec. unidade
        v_irregularidades             := null; --rec. irregularidades
        v_projeto                     := rec.projeto;
        v_campanha                    := rec.campanha;
        v_cod_situacao_marco_principal := rec.situacao;
        v_tipo_conexao                := rec.tipo_conexao;
        v_nomenclat_conex             := rec.conexao;
        v_caderneta                   := rec.caderneta;
        v_linha                       := rec.linha;
        v_rn_anterior                 := rec.rn_anterior;
        v_fonte                       := 22; --rec. fonte
        v_nom_arq                     := 'G_PLA_20249999'; --rec. nom_arq
        v_status                      := '2'; --rec.situacao
        v_login                       := 'fernanda.torres'; --rec. login
        v_etapa_comp                  := rec.nue;

        -- Chamando a procedure para inserir os dados
        BEGIN
            BDG_VALIDA.PCKG_SADGEO_PUT.CARREGA_ARQ_SIDGEO_3(
                v_cod_estacao, v_munic, v_uf, v_dsc_estacao, v_tipo_local, 
                v_tipo_monumentacao, v_i_ocupacao_gps, v_i_ocupacao_gravim, v_i_ocupacao_nivel, v_inscricao,
                v_sinal_lat, v_grau_lat, v_min_lat, v_seg_lat, v_grau_lon, v_min_lon, v_seg_lon, v_datum,
                v_dsc_localizacao, v_dsc_itinerario, v_dsc_observacao, v_data_lev, '',
                v_anotador, v_siape, v_ue_anotador, v_unidade, v_irregularidades, v_projeto, v_campanha,
                v_cod_situacao_marco_principal, v_tipo_conexao, v_nomenclat_conex, v_caderneta, v_linha,
                v_rn_anterior, v_fonte, v_nom_arq, v_status, v_login, v_etapa_comp
            );
            DBMS_OUTPUT.PUT_LINE('Registro inserido: ' || v_cod_estacao);
        EXCEPTION
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('Erro ao inserir ' || v_cod_estacao || ': ' || SQLERRM);
        END;
    END LOOP;
END;
/

