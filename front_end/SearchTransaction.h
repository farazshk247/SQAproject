
#pragma once

#include "Transaction.h"

class SearchTransaction : public Transaction {
public:
    SearchTransaction();
    bool execute(FrontEndContext& ctx) override;
};
