# TechBridge

**TechBridge** is a career assistance platform designed to help users assess their technical skills, identify their proficiency level, recommend targeted courses to bridge skill gaps, and provide job recommendations based on their resume.

## 🚀 Features

- **Skill Assessment**
  - User selects a skill (e.g., Python, Java, etc.).
  - Multi-level questions (Beginner → Intermediate → Advanced).
  - Determines the user's proficiency level based on score.
  
- **Course Recommendations**
  - Uses **TF-IDF Recommendation Algorithm** to suggest courses tailored to the user's skill level.
  - Helps bridge the gap from current level to the next.

- **Job Recommendations**
  - User uploads a resume (PDF/DOCX).
  - Resume parsing with **Word-to-Word Vectorization**.
  - Matches user profile to relevant job opportunities.

---

## 🛠️ Tech Stack

### Frontend
- **Vue.js** — Interactive user interface for skill selection, assessment, and recommendations.

### Backend
- **Python** — Core business logic, algorithms, and data processing.
- **Flask** — API layer for communication between frontend and backend.

### Algorithms
- **TF-IDF (Term Frequency–Inverse Document Frequency)** — For course recommendations based on user’s assessed level and skill gap.
- **Word-to-Word Vectorization** — For parsing resumes and matching them with job requirements.
