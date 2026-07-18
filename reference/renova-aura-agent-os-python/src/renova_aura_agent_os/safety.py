"""Deterministic detection of natural-language actions that require a human gate."""

from __future__ import annotations

import re
import unicodedata

from .models import CriticalAction


def _normalized_text(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value.casefold())
    return "".join(
        character for character in folded if not unicodedata.combining(character)
    )


def critical_actions_from_objective(
    objective: str,
    *,
    external_provider_allowed: bool,
) -> tuple[CriticalAction, ...]:
    normalized = _normalized_text(objective)
    tokens = set(re.findall(r"[a-z0-9]+", normalized))
    actions: list[CriticalAction] = []

    provider_requested = bool(
        tokens & {"openai", "provider", "provedor", "meta"}
        and tokens
        & {
            "chame",
            "chamar",
            "execute",
            "executar",
            "integre",
            "integrar",
            "use",
            "usar",
        }
    )
    if provider_requested and not external_provider_allowed:
        actions.append(CriticalAction.EXTERNAL_PROVIDER)

    message_requested = bool(
        tokens & {"mensagem", "whatsapp", "email", "sms"}
        and tokens
        & {
            "dispare",
            "disparar",
            "envie",
            "enviar",
            "mande",
            "mandar",
            "notifique",
            "notificar",
        }
    )
    if message_requested:
        actions.append(CriticalAction.REAL_MESSAGE)

    payment_requested = bool(
        tokens & {"pagamento", "cobranca", "cartao", "cobrar", "pagar"}
        and tokens
        & {
            "cobre",
            "cobrar",
            "execute",
            "executar",
            "faca",
            "pague",
            "pagar",
            "processe",
            "processar",
        }
    )
    if payment_requested:
        actions.append(CriticalAction.PAYMENT)

    destructive_requested = bool(
        tokens
        & {"apague", "apagar", "delete", "deletar", "exclua", "excluir", "remova"}
        and tokens
        & {
            "arquivo",
            "banco",
            "branch",
            "conta",
            "dados",
            "repositorio",
            "tabela",
        }
    )
    if destructive_requested:
        actions.append(CriticalAction.DESTRUCTIVE_ACTION)

    private_context = any(
        phrase in normalized
        for phrase in (
            "api key",
            "credencial",
            "dados clinicos",
            "dados de cliente",
            "dados do cliente",
            "dados dos clientes",
            "dados juridicos",
            "dados pessoais",
            "segredo",
            "token de acesso",
            "token de autenticacao",
        )
    )
    private_action = bool(
        tokens
        & {
            "acesse",
            "acessar",
            "apague",
            "apagar",
            "armazene",
            "armazenar",
            "copie",
            "copiar",
            "envie",
            "enviar",
            "exponha",
            "expor",
            "importe",
            "importar",
            "processe",
            "processar",
            "publique",
            "publicar",
            "retenha",
            "reter",
            "use",
            "usar",
        }
    )
    if private_context and private_action:
        actions.append(CriticalAction.PRIVATE_DATA)
    if "producao" in tokens and tokens & {"banco", "dados", "database"}:
        actions.append(CriticalAction.REAL_DATABASE)
    return tuple(dict.fromkeys(actions))
