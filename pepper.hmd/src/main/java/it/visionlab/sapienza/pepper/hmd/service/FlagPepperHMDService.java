package it.visionlab.sapienza.pepper.hmd.service;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.repository.FlagPepperHMDRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Service
public class FlagPepperHMDService {

    private final FlagPepperHMDRepository flagPepperHMDRepository;

    @Autowired
    public FlagPepperHMDService(FlagPepperHMDRepository flagPepperHMDRepository) {
        this.flagPepperHMDRepository = flagPepperHMDRepository;
    }

    public State getState() {
        return flagPepperHMDRepository.getState();
    }

    public void setState(State state) {
        flagPepperHMDRepository.setState(state);
    }

    public void activate(String who) {
        flagPepperHMDRepository.activate(who);
    }

    public void deactivate(String who) {
        flagPepperHMDRepository.deactivate(who);
    }

    public void nextState(String stateName) {
        flagPepperHMDRepository.nextState(stateName);
    }
}
