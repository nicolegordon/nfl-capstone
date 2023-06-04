export interface NflGame {
  homeTeam?: string | null;
  awayTeam?: string | null;
  homeScore?: string | null;
  awayScore?: string | null;
  possessionTeam?: string | null;
}

export interface WinnerPrediction {
  name: string;
  value: number;
}
