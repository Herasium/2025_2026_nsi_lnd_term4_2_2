# modules/simulation/integration.py
# -*- coding: utf-8 -*-
"""
Integration unique : simulateur + logique portes + injection dans Gate/Path.

Remplace entièrement l'ancien fichier par celui-ci.
Importer ce module (ex: `import modules.simulation.integration as sim_integration`)
effectuera l'injection si les classes Gate/Path sont disponibles.
"""

from collections import deque
from typing import List, Tuple, Any

MAX_ITERATIONS = 2000  # sécurité anti-boucle

# -----------------------
# Helpers logique
# -----------------------
def gate_compute_outputs(name: str, inputs: List[bool]) -> List[bool]:
    """
    Calcule les sorties d'une porte selon son nom.
    Retourne une liste de bools (1 valeur par sortie).
    Nom lumineux : AND, OR, NOT, XOR, NAND, NOR, XNOR
    """
    n = (name or "AND").strip().upper()
    vals = [bool(v) for v in inputs]

    if n == "AND":
        return [all(vals)]
    if n == "OR":
        return [any(vals)]
    if n == "NOT":
        return [not vals[0]] if vals else [True]
    if n == "XOR":
        return [sum(1 for v in vals if v) % 2 == 1]
    if n == "NAND":
        return [not all(vals)]
    if n == "NOR":
        return [not any(vals)]
    if n == "XNOR":
        return [not (sum(1 for v in vals if v) % 2 == 1)]
    # fallback : passthrough du premier input
    return [vals[0] if vals else False]

# -----------------------
# Méthodes à injecter dans Gate
# -----------------------
def gate_receive_input(self, index: int, value: bool):
    """Reçoit une valeur sur une entrée et marque la gate dirty si changement."""
    if index is None:
        return
    if index < 0:
        return
    # étend la liste d'inputs si nécessaire
    if index >= len(self.inputs):
        self.inputs.extend([False] * (index - len(self.inputs) + 1))
    v = bool(value)
    if self.inputs[index] != v:
        self.inputs[index] = v
        self._dirty = True

def gate__compute_outputs(self) -> List[bool]:
    """Wrapper appelé sur l'instance Gate pour calculer les sorties."""
    name = getattr(self, "_name", "AND")
    return gate_compute_outputs(name, list(self.inputs))

def gate_evaluate(self) -> List[Tuple[int, bool]]:
    """
    Si la gate est marquée _dirty, calcule les sorties, met à jour self.outputs
    et renvoie la liste des sorties modifiées [(index,new_val), ...].
    """
    if not getattr(self, "_dirty", False):
        return []

    try:
        new_outs = gate__compute_outputs(self)
    except Exception as e:
        # fallback plus tolérant
        try:
            new_outs = gate_compute_outputs(getattr(self, "_name", "AND"), list(self.inputs))
        except Exception:
            new_outs = [False]

    changed = []

    if len(new_outs) > len(self.outputs):
        self.outputs.extend([False] * (len(new_outs) - len(self.outputs)))

    for i, nv in enumerate(new_outs):
        if i >= len(self.outputs) or self.outputs[i] != nv:
            if i < len(self.outputs):
                self.outputs[i] = nv
            else:
                self.outputs.append(nv)
            changed.append((i, nv))

    self._dirty = False
    return changed

def gate_force_propagate(self, editor):
    """
    Utilitaire : force la propagation des sorties de cette gate vers les paths
    connectés dans l'editor (ne déclenche pas la boucle complète du simulateur).
    """
    for out_index, out_val in enumerate(self.outputs):
        for path in list(getattr(editor, "paths", {}).values()):
            updated = False
            for conn in (getattr(path, "inputs", []) + getattr(path, "outputs", [])):
                if not isinstance(conn, (list, tuple)):
                    continue
                if len(conn) > 2 and conn[1] == self.id and conn[2] == out_index:
                    if path.set_value(out_val, source_gate_id=self.id, source_gate_port=out_index):
                        updated = True
            if updated:
                path._dirty = True

def path_set_value(self, value: bool, source_gate_id=None, source_gate_port=None) -> bool:
    """
    Définit la valeur du path. Retourne True si la valeur a changé.
    """
    v = bool(value)
    if getattr(self, "current_value", False) == v:
        return False
    self.current_value = v
    self._dirty = True
    return True

def path_propagate_to_connected_gates(self, editor) -> List[Any]:
    modified_gates = set()

    for conn in (getattr(self, "outputs", []) + getattr(self, "inputs", [])):
        if not isinstance(conn, (list, tuple)):
            continue
        if len(conn) < 3:
            continue
        gate_id = conn[1]
        gate_port = conn[2]

        gate = None
        gates = getattr(editor, "gates", {})
        if isinstance(gates, dict):
            gate = gates.get(gate_id)
        else:
            for g in gates:
                if getattr(g, "id", None) == gate_id:
                    gate = g
                    break
        if gate is None:
            continue

        try:
            gate.receive_input(gate_port, self.current_value)
            modified_gates.add(gate_id)
        except Exception:
            try:
                gate.receive_input_from_path(self, gate_port, self.current_value)
                modified_gates.add(gate_id)
            except Exception:
                pass

    self._dirty = False
    return list(modified_gates)

class Simulator:
    def __init__(self, editor):
        self.editor = editor
        self.queue = deque()
        self._in_queue = set()

    def enqueue(self, typ: str, obj_id):
        key = (typ, obj_id)
        if key in self._in_queue:
            return
        self.queue.append(key)
        self._in_queue.add(key)

    def enqueue_gate(self, gate):
        if gate is None:
            return
        self.enqueue('gate', gate.id)

    def enqueue_path(self, path):
        if path is None:
            return
        self.enqueue('path', path.id)

    def step(self):
        for g in list(getattr(self.editor, "gates", {}).values()):
            if getattr(g, "_dirty", False):
                self.enqueue_gate(g)
        for p in list(getattr(self.editor, "paths", {}).values()):
            if getattr(p, "_dirty", False):
                self.enqueue_path(p)

        iterations = 0
        while self.queue and iterations < MAX_ITERATIONS:
            iterations += 1
            typ, obj_id = self.queue.popleft()
            self._in_queue.discard((typ, obj_id))

            if typ == 'gate':
                gate = None
                gates = getattr(self.editor, "gates", {})
                if isinstance(gates, dict):
                    gate = gates.get(obj_id)
                else:
                    for g in gates:
                        if getattr(g, "id", None) == obj_id:
                            gate = g
                            break
                if gate is None:
                    continue

                try:
                    changed_outputs = gate.evaluate()
                except Exception:
                    try:
                        changed_outputs = gate_evaluate(gate)
                    except Exception:
                        changed_outputs = []

                if changed_outputs:
                    for out_idx, out_val in changed_outputs:
                        for path in list(getattr(self.editor, "paths", {}).values()):
                            updated = False
                            for conn in (getattr(path, "inputs", []) + getattr(path, "outputs", [])):
                                if not isinstance(conn, (list, tuple)):
                                    continue
                                if len(conn) > 2 and conn[1] == gate.id and conn[2] == out_idx:
                                    if path.set_value(out_val, source_gate_id=gate.id, source_gate_port=out_idx):
                                        updated = True
                            if updated:
                                self.enqueue_path(path)

            elif typ == 'path':
                path = None
                paths = getattr(self.editor, "paths", {})
                if isinstance(paths, dict):
                    path = paths.get(obj_id)
                else:
                    for p in paths:
                        if getattr(p, "id", None) == obj_id:
                            path = p
                            break
                if path is None:
                    continue

                try:
                    modified_gate_ids = path.propagate_to_connected_gates(self.editor)
                except Exception:
                    try:
                        modified_gate_ids = path_propagate_to_connected_gates(path, self.editor)
                    except Exception:
                        modified_gate_ids = []

                for gid in modified_gate_ids:
                    g = None
                    gates = getattr(self.editor, "gates", {})
                    if isinstance(gates, dict):
                        g = gates.get(gid)
                    else:
                        for gg in gates:
                            if getattr(gg, "id", None) == gid:
                                g = gg
                                break
                    if g is not None:
                        self.enqueue_gate(g)

        if iterations >= MAX_ITERATIONS:
            print("[Simulator] MAX_ITERATIONS atteints — possible boucle de rétroaction.")

def _inject():
    try:
        from modules.data.nodes.gate import Gate
        from modules.data.nodes.path import Path
    except Exception:
        return

    if not hasattr(Gate, "receive_input"):
        setattr(Gate, "receive_input", gate_receive_input)
    if not hasattr(Gate, "_compute_outputs"):
        # expose sous le nom d'instance attendu
        setattr(Gate, "_compute_outputs", gate__compute_outputs)
    if not hasattr(Gate, "evaluate"):
        setattr(Gate, "evaluate", gate_evaluate)
    if not hasattr(Gate, "force_propagate"):
        setattr(Gate, "force_propagate", gate_force_propagate)

    if not hasattr(Path, "set_value"):
        setattr(Path, "set_value", path_set_value)
    if not hasattr(Path, "propagate_to_connected_gates"):
        setattr(Path, "propagate_to_connected_gates", path_propagate_to_connected_gates)

_inject()

__all__ = [
    "Simulator", "gate_compute_outputs", "gate_receive_input",
    "gate__compute_outputs", "gate_evaluate", "path_set_value",
    "path_propagate_to_connected_gates"
]
