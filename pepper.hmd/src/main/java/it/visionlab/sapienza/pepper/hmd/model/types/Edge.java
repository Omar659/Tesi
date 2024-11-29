package it.visionlab.sapienza.pepper.hmd.model.types;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class Edge {
    private Node target;
    private float weight;

    public Edge(Node target, float weight) {
        this.target = target;
        this.weight = weight;
    }
}
