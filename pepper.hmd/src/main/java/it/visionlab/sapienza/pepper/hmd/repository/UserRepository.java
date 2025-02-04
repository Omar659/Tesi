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

    // MongoTemplate is used to interact with MongoDB.
    private final MongoTemplate mongoTemplate;

    // Constructor-based dependency injection of MongoTemplate. Initializes 'mongoTemplate'.
    public UserRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    // Retrieves a User object from MongoDB based on the provided 'name'.
    public User getUser(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        return mongoTemplate.findOne(query, User.class);
    }

    // Checks if a user exists in MongoDB based on the provided 'name'.
    public boolean getUserExist(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        return mongoTemplate.exists(query, User.class);
    }

    // Inserts a new User document into MongoDB.
    public void createUser(User user) {
        mongoTemplate.insert(user);
    }

    // Updates the 'lastSeen' field of the User document to one day ahead from the current date.
    public void updateUserLastSeen(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        Update update = new Update().set("lastSeen", LocalDate.now().plusDays(1));
        mongoTemplate.updateFirst(query, update, User.class);
    }

    // Updates the 'tutorialSeen' field of the User document to true, indicating that the tutorial has been seen.
    public void updateUserTutorialSeen(String name) {
        Query query = new Query(Criteria.where("name").is(name));
        Update update = new Update().set("tutorialSeen", true);
        mongoTemplate.updateFirst(query, update, User.class);
    }
}
