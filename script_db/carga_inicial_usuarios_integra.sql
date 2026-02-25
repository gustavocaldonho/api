INSERT INTO usuarios_integra (
    empresa_id,
    usuario,
    senha,
    vendedor_id,
    consultar_pessoas,
    consultar_itens,
    consultar_faturamentos,
    consultar_recebimentos,
    efetuar_pre_vendas,
    data_registro,
    consultar_pagamentos,
    desconto_maximo,
    digitar_preco_venda,
    gerar_gordura_precos,
    total_gordura
) VALUES
(
    '4', 'admin', 'Admin.', '1',
    '0', '0', '0', '0', '0',
    '2024-11-04 14:24:20',
    '0',
    '99.90',
    '',
    NULL,
    NULL
),
(
    '4', '1', '1', '1',
    '1', '1', '1', '1', '1',
    '2024-11-04 14:24:20',
    '1',
    '99.00',
    '1',
    NULL,
    NULL
),
(
    '4', 'master', 'Master1', '1',
    '1', '1', '1', '1', '1',
    '2024-11-04 14:24:20',
    '1',
    '99.99',
    '1',
    NULL,
    NULL
),
(
    '4', 'gleison', '3639', '4256',
    '1', '1', '1', '1', '1',
    '2024-11-04 14:24:20',
    '1',
    '99.99',
    '1',
    NULL,
    NULL
);