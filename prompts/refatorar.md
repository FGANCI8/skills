# Refatorar com segurança

Refatore: **[módulo e objetivo mensurável]**.

Inspecione arquitetura, contratos, testes, dependências, desempenho e Git antes de propor abstrações. Roteie para o menor conjunto e prove qual acoplamento, duplicidade, risco ou dificuldade de teste será reduzido. Preserve comportamento público salvo autorização explícita.

Faça slices pequenos e reversíveis, sem misturar feature, upgrade ou limpeza alheia. Valide equivalência e negativos, peça revisão independente e pare em gates de schema, auth, produção ou escopo novo. Entregue antes/depois, arquivos, evidência e rollback.
