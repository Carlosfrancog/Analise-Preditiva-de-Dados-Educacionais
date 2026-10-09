# Skill: segurança da containerização

**Quando ativar:** CVE, imagem insegura, permissões excessivas, secrets, supply chain, auditoria e exposição de portas.

## Matriz de análise

- Origem: imagem, tag/digest, vendor, assinatura/procedência, SBOM.
- Build: dependências, contexto, secrets, cache, scripts de terceiros.
- Runtime: usuário, capabilities, mounts, `privileged`, socket daemon, `no-new-privileges`, namespaces e rootless se aplicável.
- Exposição: portas, interfaces, redes, proxy, TLS, certificados.
- Ciclo: patches, scan com data/fonte, política de severidade e compensações.

## Regras

Scan aponta potenciais riscos; validar relevância para imagem/runtime, não inventar explorabilidade. Nunca publicar segredos coletados. Um usuário não-root pode ainda ter acesso excessivo a mounts. Alterações de política de segurança requerem avaliação funcional para evitar regressões.

## Critérios de aceite

Achados classificados com evidência, correções proporcionais, controles demonstrados, exceções explicitadas e histórico rastreável. Encaminhar auditoria aprofundada ao Nestor Claws quando necessário.
