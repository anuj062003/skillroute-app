
// frontend/src/app/page.tsx
import { Navbar } from "@/components/Navbar";
import { HeroSection } from "@/components/HeroSection";
import { RoadmapForm } from "@/components/RoadmapForm";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <HeroSection />

        {/* This is our new section for the form */}
        <section id="generator" className="py-20 px-6">
          <RoadmapForm />
        </section>

        {/* We will add more "scrollytelling" sections here later */}
      </main>
    </>
  );
}