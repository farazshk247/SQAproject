#pragma once

#include <string>
#include <vector>

#include "User.h"

class AccountFile {
private:
    std::vector<User> users;

public:
    bool load(std::string path);
    User* findUser(std::string username);
    bool userExists(std::string username);
    void addUser(User user);
    bool removeUser(std::string username);
    std::vector<User> getAllUsers();
};
