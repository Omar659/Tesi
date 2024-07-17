package it.visionlab.sapienza.pepper.hmd.model;


import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDate;

@Setter
@Getter
@ToString
@Document(collection = "user")
public class User {
    @Id
    private String name;
    private LocalDate lastSeen;

    public User(String name, LocalDate lastSeen) {
        this.name = name;
        this.lastSeen = lastSeen;
    }
}
