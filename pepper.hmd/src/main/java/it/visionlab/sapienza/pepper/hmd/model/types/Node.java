package it.visionlab.sapienza.pepper.hmd.model.types;


import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@ToString
public class Node {
    private String nodeName;
    private List<String> tags;
    private String northNode;
    private String eastNode;
    private String southNode;
    private String westNode;
    private List<Edge> edges;

    public Node(String nodeName, List<String> tags, String northNode, String eastNode, String southNode, String westNode) {
        this.nodeName = nodeName;
        this.tags = tags;
        this.northNode = northNode;
        this.eastNode = eastNode;
        this.southNode = southNode;
        this.westNode = westNode;
        this.edges = new ArrayList<>();
    }

    public void addEdge(Edge edge) {
        edges.add(edge);
    }
}