-- Script de criação integra_db

CREATE TABLE IF NOT EXISTS public.bairros
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    nome character varying(100) COLLATE pg_catalog."default",
    ativo boolean,
    cidade_id integer,
    valor_disk_entrega numeric(8,2),
    data_registro timestamp(0) without time zone,
    CONSTRAINT bairros_idx PRIMARY KEY (empresa_id, id)
)

CREATE TABLE IF NOT EXISTS public.cidades
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    nome character varying(100) COLLATE pg_catalog."default",
    ativo boolean,
    uf character varying(2) COLLATE pg_catalog."default",
    valor_disk_entrega numeric(8,2),
    data_registro timestamp(0) without time zone,
    CONSTRAINT cidades_idx PRIMARY KEY (empresa_id, id)
)

CREATE TABLE IF NOT EXISTS public.cliente_novos
(
    id integer NOT NULL DEFAULT nextval('cliente_novos_id_seq'::regclass),
    empresa_id integer,
    nome character varying(120) COLLATE pg_catalog."default",
    endereco character varying(120) COLLATE pg_catalog."default",
    bairro_id integer,
    cidade_id integer,
    cpf_cnpj character varying(20) COLLATE pg_catalog."default",
    rg_ie character varying(20) COLLATE pg_catalog."default",
    fone character varying(20) COLLATE pg_catalog."default",
    celular character varying(20) COLLATE pg_catalog."default",
    nome_fantasia character varying(120) COLLATE pg_catalog."default",
    email character varying(150) COLLATE pg_catalog."default",
    sexo numeric(1,0),
    data_nascimento date,
    limite_credito numeric(10,2),
    fisica_juridica numeric(1,0),
    numero character varying(10) COLLATE pg_catalog."default",
    cep character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT cliente_novo_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.condicoes_pagamentos
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    nome character varying(50) COLLATE pg_catalog."default",
    ativo boolean,
    tipo_id integer,
    dias numeric(3,0),
    vezes_max numeric(3,0),
    data_registro timestamp(0) without time zone,
    CONSTRAINT condicoes_pagamentos_idx PRIMARY KEY (empresa_id, id)
)

CREATE TABLE IF NOT EXISTS public.empresas
(
    id integer NOT NULL,
    empresa_cnpj character varying(20) COLLATE pg_catalog."default",
    nome character varying(100) COLLATE pg_catalog."default",
    data_vencimento date,
    data_registro timestamp without time zone,
    cpf_contabilista character varying(20) COLLATE pg_catalog."default",
    contador boolean DEFAULT false,
    senha character varying(30) COLLATE pg_catalog."default",
    razao_social character varying(100) COLLATE pg_catalog."default",
    celular_ativo boolean DEFAULT false,
    disk_entrega_item_id numeric(14,0),
    data_ultimo_acesso timestamp without time zone,
    qtd_bulas numeric(10,0) DEFAULT 0,
    qtd_imagens numeric(10,0) DEFAULT 0,
    CONSTRAINT empresas_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.enderecos
(
    empresa_id integer NOT NULL,
    pessoa_id integer NOT NULL,
    sequencia integer NOT NULL,
    nome character varying(100) COLLATE pg_catalog."default",
    ativo boolean,
    bairro_id integer,
    cidade_id integer,
    logradouro character varying(100) COLLATE pg_catalog."default",
    numero character varying(10) COLLATE pg_catalog."default",
    complemento character varying(20) COLLATE pg_catalog."default",
    cep character varying(10) COLLATE pg_catalog."default",
    tipo integer,
    padrao boolean,
    ponto_referencia character varying(100) COLLATE pg_catalog."default",
    data_registro timestamp(0) without time zone,
    CONSTRAINT enderecos_idx PRIMARY KEY (empresa_id, pessoa_id, sequencia)
)

CREATE TABLE IF NOT EXISTS public.faturamentos
(
    empresa_id integer NOT NULL,
    data_movimento date NOT NULL,
    condicao_pagamento_id integer NOT NULL,
    vendedor_id integer NOT NULL,
    valor_total numeric(14,4),
    data_registro timestamp(0) without time zone,
    CONSTRAINT faturamentos_idx PRIMARY KEY (empresa_id, data_movimento, condicao_pagamento_id, vendedor_id)
)

CREATE TABLE IF NOT EXISTS public.item_codigos
(
    empresa_id integer NOT NULL,
    item_id integer NOT NULL,
    ean_gtin character varying(32) COLLATE pg_catalog."default" NOT NULL,
    data_registro timestamp(0) without time zone,
    CONSTRAINT item_codigos_idx PRIMARY KEY (empresa_id, item_id, ean_gtin)
)

CREATE TABLE IF NOT EXISTS public.itens
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    nome character varying(100) COLLATE pg_catalog."default",
    ativo boolean,
    permitir_desconto boolean,
    nome_grupo character varying(40) COLLATE pg_catalog."default",
    nome_subgrupo character varying(40) COLLATE pg_catalog."default",
    nome_classe character varying(40) COLLATE pg_catalog."default",
    sigla character varying(10) COLLATE pg_catalog."default",
    preco_custo numeric(14,4),
    preco_zero numeric(14,4),
    preco_venda numeric(14,4),
    preco_promocao numeric(14,4),
    preco_pmc numeric(14,4),
    saldo_estoque numeric(14,4),
    desconto_maximo numeric(4,2),
    data_fim_promocao date,
    data_inicio_promocao date,
    data_registro timestamp(0) without time zone,
    CONSTRAINT itens_idx PRIMARY KEY (empresa_id, id)
)

CREATE TABLE IF NOT EXISTS public.pagamentos
(
    empresa_id integer NOT NULL,
    data_movimento date NOT NULL,
    nome character varying(50) COLLATE pg_catalog."default" NOT NULL,
    valor numeric(14,2),
    CONSTRAINT pagamentos_idx PRIMARY KEY (empresa_id, data_movimento, nome)
)

CREATE TABLE IF NOT EXISTS public.pessoa_contatos
(
    empresa_id integer NOT NULL,
    pessoa_id integer NOT NULL,
    sequencia integer NOT NULL,
    nome character varying(30) COLLATE pg_catalog."default",
    tipo integer,
    contato character varying(20) COLLATE pg_catalog."default",
    data_registro timestamp(0) without time zone,
    CONSTRAINT pessoa_contatos_idx PRIMARY KEY (empresa_id, pessoa_id, sequencia)
)

CREATE TABLE IF NOT EXISTS public.pessoas
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    nome character varying(100) COLLATE pg_catalog."default",
    ativo boolean,
    fisica_juridica numeric(1,0),
    cpf_cnpj character varying(20) COLLATE pg_catalog."default",
    data_nascimento date,
    data_cadastro date,
    limite_credito numeric(12,2),
    rg_ie character varying(20) COLLATE pg_catalog."default",
    sexo numeric(1,0),
    credito_encerrado boolean,
    mae character varying(100) COLLATE pg_catalog."default",
    vendedor_codigo integer,
    data_registro timestamp(0) without time zone,
    qtd_dupl_pagas numeric(8,0),
    qtd_dupl_atrasadas numeric(8,0),
    qtd_dupl_avencer numeric(8,0),
    total_pago numeric(10,2),
    total_atrasado numeric(10,2),
    total_avencer numeric(10,2),
    dias_maior_atraso numeric(8,0),
    dias_maior_avencer numeric(8,0),
    CONSTRAINT pessoas_idx PRIMARY KEY (empresa_id, id)
)

CREATE TABLE IF NOT EXISTS public.pre_venda_itens
(
    empresa_id integer NOT NULL,
    pre_venda_id integer NOT NULL,
    sequencia integer NOT NULL,
    item_id integer,
    quantidade numeric(12,4),
    valor_venda numeric(12,4),
    valor_promocao numeric(12,4),
    valor_desconto numeric(12,4),
    CONSTRAINT pre_venda_itens_idx PRIMARY KEY (empresa_id, pre_venda_id, sequencia)
)

CREATE TABLE IF NOT EXISTS public.pre_vendas
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    destinatario_id integer,
    vendedor_id integer,
    condicao_pagamento_id integer,
    data_registro timestamp(0) without time zone,
    data_movimento timestamp(0) without time zone,
    numero integer,
    disk_entrega boolean,
    enviado boolean,
    observacao character varying(100) COLLATE pg_catalog."default",
    ide_mobile character varying(50) COLLATE pg_catalog."default",
    qtd_vezes numeric(2,0) DEFAULT 0,
    CONSTRAINT pre_vendas_idx PRIMARY KEY (empresa_id, id)
)

CREATE TABLE IF NOT EXISTS public.recebimentos
(
    empresa_id integer NOT NULL,
    data_movimento date NOT NULL,
    nome character varying(50) COLLATE pg_catalog."default" NOT NULL,
    valor numeric(14,2),
    CONSTRAINT recebimentos_idx PRIMARY KEY (empresa_id, data_movimento, nome)
)

CREATE TABLE IF NOT EXISTS public.usuarios
(
    empresa_id integer NOT NULL,
    #usuario character varying(50) COLLATE pg_catalog."default" NOT NULL,
    #senha character varying(50) COLLATE pg_catalog."default",
    vendedor_id integer NOT NULL,
    consultar_pessoas character varying(1) COLLATE pg_catalog."default",
    consultar_itens character varying(1) COLLATE pg_catalog."default",
    consultar_faturamentos character varying(1) COLLATE pg_catalog."default",
    consultar_recebimentos character varying(1) COLLATE pg_catalog."default",
    efetuar_pre_vendas character varying(1) COLLATE pg_catalog."default",
    data_registro timestamp(0) without time zone,
    consultar_pagamentos character varying(1) COLLATE pg_catalog."default",
    #desconto_maximo numeric(4,2),
    digitar_preco_venda character varying(1) COLLATE pg_catalog."default",
    gerar_gordura_precos character varying(1) COLLATE pg_catalog."default",
    #total_gordura numeric(10,2),
    CONSTRAINT usuarios_idx PRIMARY KEY (empresa_id, usuario)
)

CREATE TABLE IF NOT EXISTS public.xmls
(
    empresa_id integer NOT NULL,
    id integer NOT NULL,
    modelo numeric(2,0),
    serie numeric(2,0),
    numero numeric(12,0),
    chave_xml character varying(44) COLLATE pg_catalog."default",
    xml text COLLATE pg_catalog."default",
    data_registro timestamp without time zone,
    data_movimento timestamp without time zone,
    entrada_saida numeric(1,0) DEFAULT 1,
    CONSTRAINT xmls_idx PRIMARY KEY (empresa_id, id)
)