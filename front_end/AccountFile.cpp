#include "AccountFile.h"

#include <algorithm>
#include <fstream>
#include <utility>

namespace {
std::string trimField(const std::string& field) {
    const std::size_t first = field.find_first_not_of(' ');
    if (first == std::string::npos) {
        return "";
    }

    const std::size_t last = field.find_last_not_of(' ');
    return field.substr(first, last - first + 1);
}

bool parseUserType(const std::string& text, UserType& type) {
    if (text == "AA") {
        type = UserType::AA;
    } else if (text == "FS") {
        type = UserType::FS;
    } else if (text == "BS") {
        type = UserType::BS;
    } else if (text == "SS") {
        type = UserType::SS;
    } else {
        return false;
    }

    return true;
}

bool parseNumber(const std::string& text, double& value) {
    try {
        std::size_t parsedCharacters = 0;
        value = std::stod(text, &parsedCharacters);
        return parsedCharacters == text.size();
    } catch (...) {
        return false;
    }
}
}

bool AccountFile::load(std::string path) {
    std::ifstream input(path);
    if (!input) {
        return false;
    }

    std::vector<User> loadedUsers;
    std::string line;
    bool foundEnd = false;

    while (std::getline(input, line)) {
        if (trimField(line.substr(0, 15)) == "END") {
            foundEnd = true;
            break;
        }

        if (line.size() < 28) {
            return false;
        }

        const std::string username = trimField(line.substr(0, 15));
        const std::string typeText = trimField(line.substr(16, 2));
        const std::string creditText = trimField(line.substr(19, 9));

        UserType type = UserType::AA;
        double credit = 0.0;
        if (username.empty() || !parseUserType(typeText, type) ||
            !parseNumber(creditText, credit)) {
            return false;
        }

        loadedUsers.emplace_back(username, type, credit);
    }

    if (!foundEnd) {
        return false;
    }

    users = std::move(loadedUsers);
    return true;
}

User* AccountFile::findUser(std::string username) {
    for (User& user : users) {
        if (user.getUsername() == username) {
            return &user;
        }
    }

    return nullptr;
}

bool AccountFile::userExists(std::string username) {
    return findUser(username) != nullptr;
}

void AccountFile::addUser(User user) {
    users.push_back(user);
}

bool AccountFile::removeUser(std::string username) {
    const auto newEnd = std::remove_if(
        users.begin(), users.end(),
        [&username](User& user) { return user.getUsername() == username; });

    if (newEnd == users.end()) {
        return false;
    }

    users.erase(newEnd, users.end());
    return true;
}

std::vector<User> AccountFile::getAllUsers() {
    return users;
}
