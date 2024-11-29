package it.visionlab.sapienza.pepper.hmd.model.types;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;

@Getter
@Setter
@ToString
public class PathWithWeight {
    private List<String> path;
    private float weight;

    public PathWithWeight(List<String> path, float weight) {
        this.path = path;
        this.weight = weight;
    }
}
