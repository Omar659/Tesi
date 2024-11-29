package it.visionlab.sapienza.pepper.hmd.utils;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class JsonGraph {
    @JsonProperty("NODES")
    public List<JsonNode> nodes;

    @JsonProperty("EDGES")
    public List<JsonEdge> edges;
}
