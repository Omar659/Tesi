package it.visionlab.sapienza.pepper.hmd.utils;


import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class JsonNode {
    @JsonProperty("tags")
    public List<String> tags;

    @JsonProperty("node_name")
    public String nodeName;

    @JsonProperty("north_node")
    public String northNode;

    @JsonProperty("east_node")
    public String eastNode;

    @JsonProperty("south_node")
    public String southNode;

    @JsonProperty("west_node")
    public String westNode;
}
