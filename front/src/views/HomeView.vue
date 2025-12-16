<template>
  <section class="card">
    <p class="eyebrow">MS CINEMA</p>
    <h2>Front en place</h2>
    <p class="lead">
      Front VUE3 branché aux microservices <br>
      Catalog : http://localhost:4001 <br>
      Auth : http://localhost:4002 <br>
      Booking : http://localhost:4003 <br>
    </p>
  </section>
</template>

<script setup></script>

<style scoped>
.lead {
  color: #475569;
  max-width: 680px;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  flex-wrap: wrap;
}
</style>
