#include "SearchTransaction.h"

#include <algorithm>
#include <cctype>
#include <vector>

namespace {
std::string toLower(std::string text) {
    std::transform(text.begin(), text.end(), text.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return text;
}

bool contains(const std::string& text, const std::string& lowerTerm) {
    return toLower(text).find(lowerTerm) != std::string::npos;
}
}

SearchTransaction::SearchTransaction() {
    code = "search";
}

bool SearchTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    std::string term;
    if (!ctx.console.readLine(term)) {
        return false;
    }
    if (term.empty()) {
        ctx.console.showError("search term cannot be empty.");
        return false;
    }

    const std::string lowerTerm = toLower(term);
    const std::vector<Game> available = ctx.games.getAvailable();

    std::vector<Game> matchingGames;
    for (Game game : available) {
        if (contains(game.getName(), lowerTerm)) {
            matchingGames.push_back(game);
        }
    }

    // Admins see every matching user. Everyone else only sees an admin
    // account when that admin has a game for sale.
    const bool viewerIsAdmin = ctx.session.isAdmin();
    std::vector<std::string> matchingUsers;
    for (User user : ctx.accounts.getAllUsers()) {
        if (!contains(user.getUsername(), lowerTerm)) {
            continue;
        }

        if (user.isAdmin() && !viewerIsAdmin) {
            bool sellsAGame = false;
            for (Game game : available) {
                if (game.getSeller() == user.getUsername()) {
                    sellsAGame = true;
                    break;
                }
            }
            if (!sellsAGame) {
                continue;
            }
        }

        matchingUsers.push_back(user.getUsername());
    }

    ctx.console.showSearchResults(term, matchingGames, matchingUsers);
    return true;
}
