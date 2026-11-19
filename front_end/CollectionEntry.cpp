#include "CollectionEntry.h"

CollectionEntry::CollectionEntry(std::string owner, std::string gameName)
    : ownerName(owner), gameName(gameName) {
}

std::string CollectionEntry::getOwner() {
    return ownerName;
}

std::string CollectionEntry::getGameName() {
    return gameName;
}
