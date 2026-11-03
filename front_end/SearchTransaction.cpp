
#include "SearchTransaction.h"

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

SearchTransaction::SearchTransaction() {
    code = "search";
}

bool SearchTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    std::string query;
    if (!ctx.console.readLine(query)) {
        return false;
    }

    std::vector<Game> matchingGames;
    std::vector<User> matchingUsers;

    // Find games containing the search query.
    for (Game game : ctx.games.getAvailable()) {
        if (game.getName().find(query) != std::string::npos) {
            matchingGames.push_back(game);
        }
    }

    // Find users containing the search query.
    for (User user : ctx.accounts.getAllUsers()) {
        if (user.getUsername().find(query) == std::string::npos) {
            continue;
        }

        // Hide admins who are not selling games from non-admin users.
        if (!ctx.session.isAdmin() && user.isAdmin()) {
            bool isSelling = false;

            for (Game game : ctx.games.getAvailable()) {
                if (game.getSeller() == user.getUsername()) {
                    isSelling = true;
                    break;
                }
            }

            if (!isSelling) {
                continue;
            }
        }

        matchingUsers.push_back(user);
    }

    std::cout << "Search results for '" << query << "':\n";
    std::cout << "Games:\n";
    
    if (matchingGames.empty()) {
        std::cout << "  (none)\n";
    } else {
        for (Game game : matchingGames) {
            std::cout << "  " << game.getName()
                    << " - " << game.getSeller()
                    << " - $" << std::fixed << std::setprecision(2)
                    << game.getPrice() << "\n";
        }
    }

    std::cout << "Users:\n";

    if (matchingUsers.empty()) {
        std::cout << "  (none)\n";
    } else {
        for (User user : matchingUsers) {
            std::cout << "  " << user.getUsername() << "\n";
        }
    }

    return true;
}
