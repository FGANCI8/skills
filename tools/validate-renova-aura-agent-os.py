from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - explicit environment blocker
    raise SystemExit("BLOCKED: PyYAML is required for Agent OS YAML validation") from exc


STOP_REASONS = {
    "PASS",
    "MAX_ROUNDS",
    "TIMEOUT",
    "BUDGET_LIMIT",
    "HUMAN_APPROVAL_REQUIRED",
    "SECURITY_BLOCK",
    "ENVIRONMENT_BLOCK",
    "MISSING_EVIDENCE",
    "SCOPE_CHANGE",
}

REQUIRED_PROMPTS = {
    "construir-funcionalidade-completa.md",
    "polir-frontend-premium.md",
    "criar-backend.md",
    "criar-projeto-python.md",
    "revisar-banco.md",
    "revisar-seguranca-saas.md",
    "corrigir-bug.md",
    "refatorar.md",
    "criar-automacao.md",
    "criar-agente-ia.md",
    "continuar-trabalho.md",
    "revisao-independente.md",
    "preparar-release.md",
    "investigar-incidente.md",
    "melhorar-desempenho.md",
    "formar-equipe-multiagente.md",
    "executar-loop-qualidade.md",
}

NEW_AGENT_OS_SKILLS = {
    "renova-aura-agent-orchestrator",
    "renova-aura-backend-api-engineer",
    "renova-aura-database-reliability",
    "renova-aura-independent-reviewer",
    "renova-aura-performance-engineering",
    "renova-aura-python-engineering",
}

LOOP_NAMES = {
    "implementacao",
    "front-end premium",
    "seguranca",
    "qualidade",
    "desempenho",
    "agente/automacao",
    "documentacao/handoff",
}

PROMPT_MARKERS = {
    "routing": ("roteador", "roteie", "roteamento"),
    "inspection": (
        "leia",
        "inspecione",
        "confirme",
        "mapeie",
        "audite",
        "revise",
        "analise",
        "verifique",
        "diagnostique",
    ),
    "gate": (
        "pare",
        "aprovacao",
        "gate",
        "nao modifique",
        "nao faca",
        "nao execute",
        "nao adicione",
        "nao aprove",
        "sem autorizacao",
    ),
    "report": ("entregue", "reporte", "relatorio", "resultado", "ao final", "informe"),
}


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def literal_value(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"unsupported catalog expression: {ast.dump(node)}") from exc


def load_python_catalog_projection(path: Path) -> dict[str, dict[str, Any]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    projection: dict[str, dict[str, Any]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "_agent":
            continue
        if len(node.args) < 5:
            raise ValueError("catalog _agent call has fewer than five positional arguments")
        agent_id = literal_value(node.args[0])
        risk_node = node.args[4]
        if not (
            isinstance(risk_node, ast.Attribute)
            and isinstance(risk_node.value, ast.Name)
            and risk_node.value.id == "RiskLevel"
        ):
            raise ValueError(f"{agent_id}: risk must be a RiskLevel attribute")
        keywords = {keyword.arg: literal_value(keyword.value) for keyword in node.keywords}
        if agent_id in projection:
            raise ValueError(f"duplicate Python catalog agent id: {agent_id}")
        projection[agent_id] = {
            "name": literal_value(node.args[1]),
            "skills": list(literal_value(node.args[3])),
            "risk_level": risk_node.attr.casefold(),
            "max_rounds": keywords.get("max_rounds", 3),
            "can_write": keywords.get("can_author", True),
            "can_evaluate": keywords.get("can_evaluate", False),
            "can_integrate": keywords.get("can_integrate", False),
        }
    return projection


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported external schema ref: {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    if not isinstance(node, dict):
        raise ValueError(f"schema ref is not an object: {ref}")
    return node


def validate_schema(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> list[str]:
    if "$ref" in schema:
        return validate_schema(value, resolve_ref(root, schema["$ref"]), root, path)

    if "oneOf" in schema:
        attempts = [validate_schema(value, branch, root, path) for branch in schema["oneOf"]]
        if sum(not errors for errors in attempts) != 1:
            return [f"{path}: expected exactly one oneOf branch"]
        return []

    errors: list[str] = []
    expected = schema.get("type")
    type_ok = True
    if expected == "object":
        type_ok = isinstance(value, dict)
    elif expected == "array":
        type_ok = isinstance(value, list)
    elif expected == "string":
        type_ok = isinstance(value, str)
    elif expected == "integer":
        type_ok = isinstance(value, int) and not isinstance(value, bool)
    elif expected == "boolean":
        type_ok = isinstance(value, bool)
    if expected and not type_ok:
        return [f"{path}: expected {expected}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, value) is None:
            errors.append(f"{path}: value does not match {pattern}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value above maximum")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: duplicate array items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(validate_schema(item, item_schema, root, f"{path}[{index}]"))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_schema(value[key], child_schema, root, f"{path}.{key}"))
    return errors


def detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> list[str] | None:
        if node in visiting:
            start = visiting.index(node)
            return visiting[start:] + [node]
        if node in visited:
            return None
        visiting.append(node)
        for dependency in graph[node]:
            cycle = visit(dependency)
            if cycle:
                return cycle
        visiting.pop()
        visited.add(node)
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.repo_root.resolve()
    errors: list[str] = []

    schema_path = root / "agents" / "agent-team.schema.json"
    team_path = root / "agents" / "renova-aura-team.yaml"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    team = load_yaml(team_path)
    errors.extend(validate_schema(team, schema, schema, "team"))

    refs = team.get("agents", []) if isinstance(team, dict) else []
    if len(refs) != 18:
        errors.append(f"team: expected 18 agents, found {len(refs)}")

    agents: dict[str, dict[str, Any]] = {}
    for ref in refs:
        definition_path = root / "agents" / ref["file"]
        if not definition_path.is_file():
            errors.append(f"missing agent definition: {ref['file']}")
            continue
        definition = load_yaml(definition_path)
        errors.extend(validate_schema(definition, schema, schema, ref["file"]))
        agent_id = definition.get("id")
        if agent_id != ref["id"]:
            errors.append(f"{ref['file']}: id differs from team registry")
        if agent_id in agents:
            errors.append(f"duplicate agent id: {agent_id}")
        agents[agent_id] = definition

    registry_ids = [entry["id"] for entry in refs]
    if len(registry_ids) != len(set(registry_ids)):
        errors.append("team: duplicate agent registry id")

    integrators = [agent_id for agent_id, agent in agents.items() if agent.get("accountable_integrator")]
    if integrators != [team.get("accountable_integrator")]:
        errors.append(f"team: expected exactly the accountable integrator, got {integrators}")

    skill_ids = {path.name for path in (root / "skills").glob("renova-aura-*") if path.is_dir()}
    for agent_id, agent in agents.items():
        for skill in agent.get("skills", []):
            if skill not in skill_ids:
                errors.append(f"{agent_id}: missing skill reference {skill}")
        for dependency in agent.get("dependencies", []):
            if dependency not in agents:
                errors.append(f"{agent_id}: missing agent dependency {dependency}")
        capabilities = agent.get("capabilities", {})
        if capabilities.get("can_integrate") != agent.get("accountable_integrator"):
            errors.append(f"{agent_id}: can_integrate must match accountable_integrator")
        if capabilities.get("can_evaluate") and not capabilities.get("must_be_independent_from_author"):
            errors.append(f"{agent_id}: evaluator must be independent from author")
        if agent.get("max_rounds", 99) > team.get("default_limits", {}).get("max_rounds", 0):
            errors.append(f"{agent_id}: max_rounds exceeds team default")

    graph = {agent_id: list(agent.get("dependencies", [])) for agent_id, agent in agents.items()}
    cycle = detect_cycle(graph)
    if cycle:
        errors.append("agent dependency cycle: " + " -> ".join(cycle))

    catalog_path = (
        root
        / "reference"
        / "renova-aura-agent-os-python"
        / "src"
        / "renova_aura_agent_os"
        / "catalog.py"
    )
    try:
        python_catalog = load_python_catalog_projection(catalog_path)
    except (OSError, SyntaxError, ValueError) as exc:
        errors.append(f"Python catalog projection is invalid: {exc}")
        python_catalog = {}
    if set(python_catalog) != set(agents):
        errors.append("Python catalog agent ids differ from canonical YAML definitions")
    for agent_id in sorted(set(python_catalog) & set(agents)):
        yaml_agent = agents[agent_id]
        yaml_capabilities = yaml_agent.get("capabilities", {})
        expected_projection = {
            "name": yaml_agent.get("name"),
            "skills": yaml_agent.get("skills", []),
            "risk_level": yaml_agent.get("risk_level"),
            "max_rounds": yaml_agent.get("max_rounds"),
            "can_write": yaml_capabilities.get("can_write"),
            "can_evaluate": yaml_capabilities.get("can_evaluate"),
            "can_integrate": yaml_capabilities.get("can_integrate"),
        }
        for field, expected in expected_projection.items():
            actual = python_catalog[agent_id].get(field)
            if actual != expected:
                errors.append(
                    f"{agent_id}: Python catalog {field}={actual!r} "
                    f"differs from YAML {expected!r}"
                )

    mode_ids = [mode["id"] for mode in team.get("orchestration_modes", [])]
    if len(mode_ids) != 9 or len(set(mode_ids)) != 9:
        errors.append("team: expected 9 unique orchestration modes")
    if set(team.get("stop_reasons", [])) != STOP_REASONS:
        errors.append("team: stop reasons differ from canonical set")

    loop_text = (root / "agents" / "LOOP_PROTOCOLS.md").read_text(encoding="utf-8")
    normalized_loop_text = normalize_text(loop_text)
    for loop_name in LOOP_NAMES:
        if loop_name not in normalized_loop_text:
            errors.append(f"loop protocols: missing loop {loop_name}")
    for reason in STOP_REASONS:
        if reason not in loop_text:
            errors.append(f"loop protocols: missing stop reason {reason}")
    if "tres rodadas" not in normalized_loop_text and "three rounds" not in normalized_loop_text:
        errors.append("loop protocols: missing default three-round limit")
    loop_contract_markers = (
        "estado inicial",
        "criterio de aprovacao",
        "rubrica",
        "autor",
        "avaliador",
        "artefatos",
        "maximo de rodadas",
        "timeout",
        "orcamento",
        "limite de ferramentas",
        "gates",
        "motivo de bloqueio",
        "aprovacao humana aplicavel",
        "stop reason",
    )
    for marker in loop_contract_markers:
        if marker not in normalized_loop_text:
            errors.append(f"loop protocols: missing contract marker {marker}")

    eval_text = (root / "RENOVA_AURA_AGENT_OS_EVALS.md").read_text(encoding="utf-8")
    eval_ids = set(re.findall(r"\| (A\d{2}) \|", eval_text))
    expected_evals = {f"A{index:02d}" for index in range(1, 31)}
    if eval_ids != expected_evals:
        errors.append("Agent OS eval matrix must contain A01 through A30")
    passed_eval_ids = set(
        re.findall(r"^\| (A\d{2}) \|.*\| PASS \|$", eval_text, flags=re.MULTILINE)
    )
    if passed_eval_ids != expected_evals:
        errors.append("Agent OS eval matrix must record individual PASS evidence for A01-A30")

    prompt_files = [path for path in (root / "prompts").glob("*.md") if path.name != "README.md"]
    if len(prompt_files) != 20:
        errors.append(f"prompts: expected 20 reusable prompts, found {len(prompt_files)}")
    prompt_names = {path.name for path in prompt_files}
    missing_prompts = sorted(REQUIRED_PROMPTS - prompt_names)
    if missing_prompts:
        errors.append("prompts: missing required natural prompts: " + ", ".join(missing_prompts))
    for prompt_name in sorted(REQUIRED_PROMPTS & prompt_names):
        prompt_text = normalize_text((root / "prompts" / prompt_name).read_text(encoding="utf-8"))
        for contract, markers in PROMPT_MARKERS.items():
            if not any(marker in prompt_text for marker in markers):
                errors.append(f"{prompt_name}: missing {contract} contract marker")

    for skill in sorted(skill_ids):
        skill_path = root / "skills" / skill / "SKILL.md"
        skill_text = normalize_text(skill_path.read_text(encoding="utf-8"))
        if skill in NEW_AGENT_OS_SKILLS:
            required_sections = {
                "when-not-to-use": ("when not to use", "do not use"),
                "workflow": ("workflow",),
                "validation": ("validation",),
                "output": ("output",),
                "human-gate": ("approval", "human gate"),
                "eval-reference": ("references/evals.md",),
            }
            for contract, markers in required_sections.items():
                if not any(marker in skill_text for marker in markers):
                    errors.append(f"{skill}: missing {contract} contract")
        interface_path = root / "skills" / skill / "agents" / "openai.yaml"
        if not interface_path.is_file():
            errors.append(f"{skill}: missing agents/openai.yaml")
            continue
        interface = load_yaml(interface_path)
        if not isinstance(interface, dict) or "interface" not in interface:
            errors.append(f"{skill}: invalid agents/openai.yaml")
            continue
        default_prompt = interface["interface"].get("default_prompt", "")
        if f"${skill}" not in default_prompt:
            errors.append(f"{skill}: default_prompt does not mention the skill")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps({
        "status": "PASS",
        "agents": len(agents),
        "skills": len(skill_ids),
        "prompts": len(prompt_files),
        "modes": len(mode_ids),
        "evals": len(eval_ids),
        "schema": schema_path.name,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
