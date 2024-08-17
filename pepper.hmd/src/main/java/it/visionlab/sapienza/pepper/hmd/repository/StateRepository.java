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
    private final MongoTemplate mongoTemplate;

    public StateRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    public State getState() {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        return mongoTemplate.findOne(query, State.class);
    }

    public Boolean getHmdOpen() {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null;
        return state.getHmdOpen();
    }

    public void setState(State state) {
        if (state != null) {
            mongoTemplate.save(state);
        }
    }

    public void activate(String who) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null;
        Update update;
        if (Objects.equals(who, "pepper")) {
            update = new Update().set("flagPepper", true);
        } else {
            update = new Update().set("flagHMD", true);
        }
        mongoTemplate.updateFirst(query, update, State.class);
    }

    public void deactivate(String who) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null;
        Update update;
        if (Objects.equals(who, pepperFlagName)) {
            update = new Update().set("flagPepper", false);
            mongoTemplate.updateFirst(query, update, State.class);
        } else if (Objects.equals(who, hmdFlagName)) {
            update = new Update().set("flagHMD", false);
            mongoTemplate.updateFirst(query, update, State.class);
        }
    }

    public void nextState(String stateName) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null;
        Update update = new Update().set("stateName", stateName);
        mongoTemplate.updateFirst(query, update, State.class);
    }

    public void setCurrentUser(User user) {
        Query query = new Query(Criteria.where("stateId").is(stateId));
        State state = mongoTemplate.findOne(query, State.class);
        assert state != null;
        Update update = new Update().set("currentUser", user);
        mongoTemplate.updateFirst(query, update, State.class);
    }
}
