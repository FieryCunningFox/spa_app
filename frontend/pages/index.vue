<template>
  <div>
  <h1>Articles</h1>
  <div v-for="article in articles" :key="article.slug" class="blog">
    <div class="blog-title">{{ article.h1 }}</div>
    <div class="blog-introtext">{{ article.description }}</div>
    <div class="blog-tag">{{ article.tags }}</div>
  </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  async asyncData(ctx) {
    const { data } = await axios.get(`http://127.0.0.1:8000/api/articles/`);
    return {
      posts: data.results,
    }
  }
}
</script>

<style>

</style>
