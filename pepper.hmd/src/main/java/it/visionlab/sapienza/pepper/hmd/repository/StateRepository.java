package it.visionlab.sapienza.pepper.hmd.repository;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.model.User;
import lombok.extern.java.Log;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

import java.util.Objects;

import static it.visionlab.sapienza.pepper.hmd.constants.Constants.*;

@Log
@Repository
public class StateRepository {

    // MongoTemplate is used to interact with MongoDB.
    private final MongoTemplate mongoTemplate;

    // Constructor-based dependency injection of MongoTemplate. Initializes 'mongoTemplate'.
    public StateRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    // Retrieves the current state from the MongoDB collection based on the predefined 'stateId'.
    public State getState() {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        return mongoTemplate.findOne(query, State.class);
    }

    // Retrieves the 'hmdOpen' flag value from the current state.
    public Boolean getHmdOpen() {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null; // Ensures that the state object is not null.
        return state.getHmdOpen();
    }

    // Updates the state document in MongoDB with the provided State object.
    public void setState(State state) {
        if (state != null) {
            mongoTemplate.save(state);
        }
    }

    // Activates a feature (Pepper or HMD) based on the 'who' parameter.
    public void activate(String who) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null; // Ensures that the state object is not null.
        Update update;
        if (Objects.equals(who, "pepper")) {
            update = new Update().set("flagPepper", true);
        } else {
            update = new Update().set("flagHMD", true);
        }
        mongoTemplate.updateFirst(query, update, State.class);
    }

    // Deactivates a feature (Pepper or HMD) based on the 'who' parameter.
    public void deactivate(String who) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null; // Ensures that the state object is not null.
        Update update;
        if (Objects.equals(who, pepperFlagName)) {
            update = new Update().set("flagPepper", false);
            mongoTemplate.updateFirst(query, update, State.class);
        } else if (Objects.equals(who, hmdFlagName)) {
            update = new Update().set("flagHMD", false);
            mongoTemplate.updateFirst(query, update, State.class);
        }
    }

    // Updates the 'stateName' field of the state document with the provided 'stateName'.
    public void nextState(String stateName) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null; // Ensures that the state object is not null.
        Update update = new Update().set("stateName", stateName);
        mongoTemplate.updateFirst(query, update, State.class);
    }

    // Sets the 'currentUser' field of the state document to the provided User object.
    public void setCurrentUser(User user) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null; // Ensures that the state object is not null.
        Update update = new Update().set("currentUser", user);
        mongoTemplate.updateFirst(query, update, State.class);
    }

    // Sets the 'hmdOpen' field of the state document to true.
    public void hmdOpened() {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null; // Ensures that the state object is not null.
        Update update = new Update().set("hmdOpen", true);
        mongoTemplate.updateFirst(query, update, State.class);
    }
}
