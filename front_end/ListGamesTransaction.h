#pragma once

#include "Transaction.h"

class ListGamesTransaction : public Transaction {
public:
    ListGamesTransaction();
    bool execute(FrontEndContext& ctx) override;
};
