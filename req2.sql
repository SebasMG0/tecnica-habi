CREATE TABLE like_history(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE like_history
ADD CONSTRAINT fk_property FOREIGN KEY (property_id) REFERENCES property(id),
ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth_user(id);
