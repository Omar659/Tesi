package it.visionlab.sapienza.pepper.hmd;

import com.fasterxml.jackson.databind.ObjectMapper;
import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.model.types.Graph;
import it.visionlab.sapienza.pepper.hmd.model.types.PathWithWeight;
import it.visionlab.sapienza.pepper.hmd.service.StateService;
import it.visionlab.sapienza.pepper.hmd.utils.JsonEdge;
import it.visionlab.sapienza.pepper.hmd.utils.JsonGraph;
import it.visionlab.sapienza.pepper.hmd.utils.JsonNode;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.ResourceBundle;

import static it.visionlab.sapienza.pepper.hmd.constants.Constants.*;

@SpringBootApplication
public class PepperServerHmdApplication {

    // Main method. The entry point for the Spring Boot application.
    public static void main(String[] args) {
        SpringApplication.run(PepperServerHmdApplication.class, args);
    }
}

// Component annotation. Marks this class as a Spring component that will be managed by the Spring container.
@Component
class StateInitializer implements CommandLineRunner {

    // Service used to manage state operations.
    private final StateService stateService;

    // Constructor-based dependency injection of StateService. Initializes 'stateService'.
    public StateInitializer(StateService stateService) {
        this.stateService = stateService;
    }

    // Method executed when the application context is loaded. Initializes the state.
    @Override
    public void run(String... args) throws Exception {
        try {
            // Usa il ClassLoader per ottenere il file dal classpath
            ClassLoader classLoader = getClass().getClassLoader();
            InputStream inputStream = classLoader.getResourceAsStream("graph.json");

            if (inputStream == null) {
                throw new IllegalArgumentException("File graph.json non trovato nelle risorse!");
            }

            // Leggi il JSON
            ObjectMapper mapper = new ObjectMapper();
            JsonGraph jsonGraph = mapper.readValue(inputStream, JsonGraph.class);

            // Costruisci il grafo
            Graph graph = new Graph();

            // Aggiungi i nodi al grafo
            for (JsonNode node : jsonGraph.nodes) {
                graph.addNode(node.nodeName, node.tags, node.northNode, node.eastNode, node.southNode, node.westNode);
            }

            // Aggiungi gli archi al grafo
            for (JsonEdge edge : jsonGraph.edges) {
                if (edge.edge.size() == 2) {
                    String node1 = edge.edge.get(0);
                    String node2 = edge.edge.get(1);
                    float weight = edge.weight;
                    graph.addEdge(node1, node2, weight);
                }
            }
            // Create an initial state object with predefined constants.
//            State initialState = new State(stateId, flagPepper, flagHMD, stateName, chosenPlace, currentUser, hmdOpen, pepperAction
//                    , graph
//            );
            // Save the initial state using the stateService.
//            stateService.setState(initialState);
//            stateService.putGraph(graph);
            mapGraph = graph;

            // Esegui una ricerca (ad esempio, trova tutti i percorsi da r301 a r302)
            List<PathWithWeight> paths = graph.findAllPaths("r301", "rConf");
            System.out.println("Tutti i percorsi da r301 a rConf:");
            for (PathWithWeight path : paths) {
                System.out.println(path);
            }
            System.out.println(graph.getAllTags());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
