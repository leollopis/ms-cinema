<template>
  <div class="layout">
    <header class="hero">
      <div>
        <p class="eyebrow">MS CINEMA</p>
        <h1>{{ isDevops ? "DevOps board" : "Accueil" }}</h1>
        <p class="subtitle">
          {{
            isDevops
              ? "Pilotage direct des microservices (admin)."
              : "Front Vue + DevOps board."
          }}
        </p>
        <div class="links">
          <RouterLink to="/">Accueil</RouterLink>
          <RouterLink to="/devops">DevOps</RouterLink>
        </div>
      </div>
      <div class="hero-meta">
        <span>Version: {{ appVersion }}</span>
      </div>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { computed } from "vue";

const appVersion = __APP_VERSION__;

const route = useRoute();
const isDevops = computed(() => route.path.startsWith("/devops"));
</script>

<style scoped>
.layout {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 16px 48px;
}

.hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 16px;
}

.eyebrow {
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #475569;
  margin: 0 0 4px;
}

h1 {
  margin: 0;
}

.subtitle {
  max-width: 520px;
  color: #475569;
  margin: 8px 0;
}

.links {
  display: inline-flex;
  gap: 12px;
  margin-top: 8px;
}

.links a {
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #fff;
}

.links a.router-link-active {
  border-color: #2563eb;
  color: #2563eb;
}

.hero-meta {
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
  color: #475569;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
