import networkx as nx
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
import dateutil.parser

logger = logging.getLogger(__name__)

class CognitiveGraph:
    """
    Advanced Multi-layered Cognitive Graph (v2).
    Nodes can exist in different logical layers (app, file, context).
    Edges decay over time if not traversed, enabling temporal pruning.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: str, layer: str = "app", metadata: Dict[str, Any] = None) -> None:
        if metadata is None:
            metadata = {}
        
        metadata['layer'] = layer
        metadata['last_seen'] = datetime.utcnow().isoformat()
        
        if self.graph.has_node(node_id):
            for k, v in metadata.items():
                self.graph.nodes[node_id][k] = v
        else:
            self.graph.add_node(node_id, **metadata)
            logger.debug(f"Added multi-layer node {node_id} (Layer: {layer})")

    def add_edge(self, source_id: str, target_id: str, base_weight: float = 1.0, relation_type: str = "transition") -> None:
        if not self.graph.has_node(source_id) or not self.graph.has_node(target_id):
            return

        now_str = datetime.utcnow().isoformat()
        if self.graph.has_edge(source_id, target_id):
            edge = self.graph[source_id][target_id]
            # temporal decay before modifying weight
            decayed = self._calculate_decay(edge.get('weight', 1.0), edge.get('last_updated', now_str))
            
            # Boost the decayed weight
            self.graph[source_id][target_id]['weight'] = decayed + base_weight
            self.graph[source_id][target_id]['last_updated'] = now_str
        else:
            self.graph.add_edge(source_id, target_id, weight=base_weight, type=relation_type, last_updated=now_str)

    def _calculate_decay(self, current_weight: float, last_updated_str: str) -> float:
        """Exponential decay based on hours since last traversal"""
        try:
            last_dt = dateutil.parser.isoparse(last_updated_str)
            hours_diff = (datetime.utcnow() - last_dt).total_seconds() / 3600.0
            decay_factor = max(0.9 ** hours_diff, 0.1) # Decays 10% an hour, floors at 0.1
            return current_weight * decay_factor
        except Exception:
            return current_weight

    def get_probable_next_nodes(self, node_id: str, layer_filter: str = None, top_k: int = 5) -> List[Tuple[str, float]]:
        if not self.graph.has_node(node_id):
            return []

        edges = self.graph.out_edges(node_id, data=True)
        # Apply filters and decay before sorting
        now_str = datetime.utcnow().isoformat()
        candidates = []
        for src, tgt, data in edges:
            tgt_layer = self.graph.nodes[tgt].get('layer')
            if layer_filter and tgt_layer != layer_filter:
                continue
            
            decayed_weight = self._calculate_decay(data.get('weight', 0.0), data.get('last_updated', now_str))
            candidates.append((tgt, decayed_weight))

        sorted_edges = sorted(candidates, key=lambda x: x[1], reverse=True)
        return sorted_edges[:top_k]

