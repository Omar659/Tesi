package it.visionlab.sapienza.pepper.hmd;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.service.FlagPepperHMDService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Component;

import static it.visionlab.sapienza.pepper.hmd.constants.Constants.*;

@SpringBootApplication
public class PepperServerHmdApplication {

	public static void main(String[] args) {
		SpringApplication.run(PepperServerHmdApplication.class, args);
	}
}

@Component
class FlagInitializer implements CommandLineRunner {

	private final FlagPepperHMDService flagPepperHMDService;

	public FlagInitializer(FlagPepperHMDService flagPepperHMDService) {
		this.flagPepperHMDService = flagPepperHMDService;
	}

	@Override
	public void run(String... args) throws Exception {
		State initialState = new State(stateId, flagPepper,flagHMD,stateName,chosenPlace);
		flagPepperHMDService.setState(initialState);
	}
}
