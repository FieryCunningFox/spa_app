<template>
  <div>
    <Navbar />
    <Nuxt />
  </div>
</template>


<script>
import Navbar from "~/components/Navbar";
import Slider from "~/components/Slider";
import Footer from "~/components/Footer";

export default {
  components: {
    Footer,
    Slider,
    Navbar,
  }
};
</script>

<style>

</style>
