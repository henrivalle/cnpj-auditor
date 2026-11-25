# Como contribuir / Contributing

Comece pelas [tarefas para iniciantes](https://github.com/henrivalle/cnpj-auditor/contribute). Para relatar uma falha, inclua um arquivo sintético mínimo, o comando usado e o status esperado. Use somente dados fictícios em issues, PRs e testes.

Start with [beginner tasks](https://github.com/henrivalle/cnpj-auditor/contribute). For a reproduction, include a minimal synthetic input, the command, and the expected status. Use synthetic data in issues, PRs, and tests.

Rode os testes na raiz do repositório. Run the tests from the repository root.

```bash
python3 -m unittest discover -s tests -v
```

Para mudanças no cálculo, cite a referência oficial. Para mudanças na CLI, descreva o efeito no CSV de saída e nos códigos de saída.

For a check-digit change, cite the official reference. For a CLI change, describe its effect on the output CSV and exit codes.
