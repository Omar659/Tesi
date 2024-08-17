package it.visionlab.sapienza.pepper.hmd.repository;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.model.User;
import lombok.extern.java.Log;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

import static it.visionlab.sapienza.pepper.hmd.constants.Constants.stateId;

@Log
@Repository
public class UserRepository {

    private final MongoTemplate mongoTemplate;

    public UserRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    public User getUser(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        return mongoTemplate.findOne(query, User.class);
    }

    public boolean getUserExist(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        return mongoTemplate.exists(query, User.class);
    }

    public void createUser(User user) {
        mongoTemplate.insert(user);
    }

    public void updateUserLastSeen(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        Update update = new Update().set("lastSeen", LocalDate.now().plusDays(1));
        mongoTemplate.updateFirst(query, update, User.class);
    }

    public void updateUserTutorialSeen(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        Update update = new Update().set("lastSeen", true);
        mongoTemplate.updateFirst(query, update, User.class);
    }
}
