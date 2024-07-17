package it.visionlab.sapienza.pepper.hmd.service;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.repository.StateRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StateService {

    private final StateRepository stateRepository;

    @Autowired
    public StateService(StateRepository stateRepository) {
        this.stateRepository = stateRepository;
    }

    public State getState() {
        return stateRepository.getState();
    }

    public void setState(State state) {
        stateRepository.setState(state);
    }

    public void activate(String who) {
        stateRepository.activate(who);
    }

    public void deactivate(String who) {
        stateRepository.deactivate(who);
    }

    public void nextState(String stateName) {
        stateRepository.nextState(stateName);
    }
}
