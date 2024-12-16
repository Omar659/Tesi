package it.visionlab.sapienza.pepper.hmd.model.types;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.*;

@Getter
@Setter
@ToString
public class Graph {
    private Map<String, Node> nodes; // Mappa dei nodi
    private String startNode;        // Nodo di partenza

    public Graph() {
        this.nodes = new HashMap<>();
    }

    // Aggiungi un nodo al grafo
    public void addNode(String nodeName, List<String> tags, String northNode, String eastNode, String southNode, String westNode) {
        nodes.putIfAbsent(nodeName, new Node(nodeName, tags, northNode, eastNode, southNode, westNode));
    }

    // Aggiungi un arco tra due nodi (bidirezionale)
    public void addEdge(String node1, String node2, float weight) {
        Node n1 = nodes.get(node1);
        Node n2 = nodes.get(node2);
        if (n1 != null && n2 != null) {
            n1.addEdge(new Edge(n2, weight));
            n2.addEdge(new Edge(n1, weight));
        }
    }

    // Restituisce tutti i percorsi da startNode a endNode con il loro peso
    public List<PathWithWeight> findAllPaths(String startNode, String endNode) {
        setStartNode(startNode);
        List<PathWithWeight> allPaths = new ArrayList<>();
        List<String> currentPath = new ArrayList<>();
        Set<String> visited = new HashSet<>();
        float currentWeight = 0;

        dfs(nodes.get(startNode), endNode, visited, currentPath, allPaths, currentWeight);

        return allPaths;
    }

    // DFS per trovare tutti i percorsi pesati
    private void dfs(Node current, String endNode, Set<String> visited, List<String> currentPath, List<PathWithWeight> allPaths, float currentWeight) {
        if (current == null || visited.contains(current.getNodeName())) {
            return;
        }

        visited.add(current.getNodeName());
        currentPath.add(current.getNodeName());

        if (current.getNodeName().equals(endNode)) {
            // Se siamo arrivati al nodo finale, aggiungi il percorso e il peso alla lista dei risultati
            allPaths.add(new PathWithWeight(new ArrayList<>(currentPath), currentWeight));
        } else {
            for (Edge edge : current.getEdges()) {
                dfs(edge.getTarget(), endNode, visited, currentPath, allPaths, currentWeight + edge.getWeight());
            }
        }

        // Backtracking
        visited.remove(current.getNodeName());
        currentPath.remove(currentPath.size() - 1);
    }

    // Restituisce l'insieme di tutti i tag presenti nei nodi del grafo
    public Set<String> getAllTags() {
        Set<String> allTags = new HashSet<>();
        for (Node node : nodes.values()) {
            if (node.getTags() != null) {
                allTags.addAll(node.getTags());
            }
        }
        return allTags;
    }

    // Controlla se un tag specifico è presente nell'insieme di tutti i tag
    public boolean containsTag(String tag) {
        Set<String> allTags = getAllTags();               // Ottieni l'insieme di tutti i tag
        return allTags.contains(tag.toUpperCase());       // Verifica se il tag è presente
    }

}
