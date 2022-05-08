    CREATE TABLE match_data.rounds (
	  "matchID" TEXT,
	  "mapName" TEXT,
	  "roundNum" INTEGER,
	  "isWarmup" INTEGER,
	  "tScore" INTEGER,
	  "ctScore" INTEGER,
	  "endTScore" INTEGER,
	  "endCTScore" INTEGER,
	  "ctTeam" TEXT,
	  "tTeam" TEXT,
	  "winningSide" TEXT,
	  "winningTeam" TEXT,
	  "losingTeam" TEXT,
	  "roundEndReason" TEXT,
	  "ctStartEqVal" INTEGER,
	  "ctRoundStartEqVal" INTEGER,
	  "ctRoundStartMoney" INTEGER,
	  "ctBuyType" TEXT,
	  "ctSpend" INTEGER,
	  "tStartEqVal" INTEGER,
	  "tRoundStartEqVal" INTEGER,
	  "tRoundStartMoney" INTEGER,
	  "tBuyType" TEXT,
	  "tSpend" INTEGER,
  PRIMARY KEY ("matchID","roundNum") 
);