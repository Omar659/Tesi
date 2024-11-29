package it.visionlab.sapienza.pepper.hmd.utils;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class JsonEdge {
    @JsonProperty("edge")
    public List<String> edge;

    @JsonProperty("weight")
    public float weight;
}
