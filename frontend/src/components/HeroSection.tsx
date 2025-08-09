// frontend/src/components/HeroSection.tsx
'use client';
import { motion } from 'framer-motion';
import styles from './HeroSection.module.css';

export function HeroSection() {
  return (
    <section className={styles.heroContainer}>
      <motion.h1
        className={`${styles.headline} font-display`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        Your Career, Demystified.
      </motion.h1>
      <motion.p
        className={styles.subtext}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
      >
        SkillRoute uses real-time job market data to build your personalized learning path. Stop guessing, start growing.
      </motion.p>
    </section>
  );
}