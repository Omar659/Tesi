package it.visionlab.sapienza.pepper.hmd;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.service.StateService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Component;

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
        // Create an initial state object with predefined constants.
        State initialState = new State(stateId, flagPepper, flagHMD, stateName, chosenPlace, currentUser, hmdOpen);
        // Save the initial state using the stateService.
        stateService.setState(initialState);
    }
}
