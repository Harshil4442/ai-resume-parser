export type ResumeParseResponse = {
  resume_id: number;
  skills: string[];
  experience_years: number;
  sections: Record<string, string>;
};

export type JobMatchResponse = {
  match_id: number;
  match_score: number;
  required_skills: string[];
  missing_skills: string[];
  weak_skills: string[];
};

export type AnalyticsSummary = {
  profile_completeness: number;
  avg_match_score: number;
  applications_count: number;
  match_history: { timestamp: string; match_score: number }[];
};
