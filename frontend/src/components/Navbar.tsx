// frontend/src/components/Navbar.tsx
'use client';
import styles from './Navbar.module.css';

export function Navbar() {

  const handleScrollToGenerator = () => {
    const element = document.getElementById('generator');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className={styles.nav}>
      <div className={styles.container}>
        <div className={styles.content}>
          <span className={`${styles.brand} font-display`}>SkillRoute</span>
          <button 
            type="button" 
            className={styles.ctaButton}
            onClick={handleScrollToGenerator} // Add the onClick handler here
          >
            Generate Path
          </button>
        </div>
      </div>
    </nav>
  );
}