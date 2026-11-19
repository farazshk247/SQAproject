#pragma once

#include <string>

class CollectionEntry {
private:
    std::string ownerName;
    std::string gameName;

public:
    CollectionEntry(std::string owner, std::string gameName);
    std::string getOwner();
    std::string getGameName();
};
