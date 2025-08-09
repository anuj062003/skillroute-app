'use client';

import { useState } from 'react';
import styles from './RoadmapForm.module.css'; // Import the CSS Module

interface RoadmapResponse {
  required_skills: string[];
  missing_skills: string[];
}

export function RoadmapForm() {
  const [currentSkills, setCurrentSkills] = useState('python, sql');
  const [targetRole, setTargetRole] = useState('Data Scientist');
  const [results, setResults] = useState<RoadmapResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setError('');
    setResults(null);

    try {
      const skillsArray = currentSkills.split(',').map(skill => skill.trim()).filter(Boolean);
      
      // Uses the environment variable for the API URL
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/roadmap`;

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_skills: skillsArray,
          target_role: targetRole,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Network response was not ok');
      }
      
      const data: RoadmapResponse = await response.json();
      setResults(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message || 'Failed to fetch roadmap. Is the backend server running?');
      } else {
        setError('An unknown error occurred. Is the backend server running?');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Note how className is now using the 'styles' object we imported
  return (
    <div className={styles.formWrapper}>
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <label htmlFor="current-skills" className={styles.formLabel}>
              Your Current Skills
            </label>
            <input
              type="text"
              id="current-skills"
              value={currentSkills}
              onChange={(e) => setCurrentSkills(e.target.value)}
              placeholder="e.g., python, react, sql"
              className={styles.formInput}
            />
          </div>
          <div>
            <label htmlFor="target-role" className={styles.formLabel}>
              Your Target Role
            </label>
            <input
              type="text"
              id="target-role"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g., Data Scientist, iOS Developer"
              className={styles.formInput}
            />
          </div>
        </div>
        <button type="submit" disabled={isLoading} className={styles.formButton}>
          {isLoading ? `Analyzing ${targetRole}...` : 'Generate Roadmap'}
        </button>
      </form>

      {error && <p style={{marginTop: '1.5rem', textAlign: 'center', color: '#ef4444'}}>{error}</p>}
      
      {results && (
        <div className={styles.resultsContainer}>
          <h2 className={styles.resultsTitle}>Your Learning Roadmap</h2>
          <p className={styles.resultsSubtitle}>
            To become a <span style={{fontWeight: 600, color: 'white'}}>{targetRole}</span>, you need to learn these skills:
          </p>
          <div className={styles.skillsWrapper}>
            {results.missing_skills.length > 0 ? (
              results.missing_skills.map((skill) => (
                <span key={skill} className={styles.skillPill}>
                  {skill}
                </span>
              ))
            ) : (
              <p style={{color: '#22c55e', fontWeight: 500}}>You have all the required skills for this role! 🎉</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}