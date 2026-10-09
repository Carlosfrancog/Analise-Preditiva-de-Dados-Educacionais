# Adapter: Windows / Docker Desktop / WSL2

- Confirmar Docker context e integração WSL2; Windows host, distribuição Ubuntu e daemon do Docker Desktop são camadas diferentes.
- Em bind mounts, verificar diferenças CRLF/LF, case-sensitivity, permissões, performance de filesystem `/mnt/c` vs filesystem Linux e caminhos relativos.
- Confirmar mapeamento de portas entre namespaces e firewall/antivírus/VPN sem presumir networking fixo.
- Não assumir que comandos PowerShell e Bash têm sintaxe equivalente.
- Evitar apagar dados da distro, imagens compartilhadas ou caches do Docker Desktop para solucionar problemas sem diagnóstico.
