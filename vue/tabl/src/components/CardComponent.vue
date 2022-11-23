<script setup>
import App from '../App.vue'
import axios from 'axios'
import { onUpdated } from 'vue';
</script>

<template>
  <div class="card" @click="cardClicked">
    <div class="card-body">
      <h5 class="card-title ">{{cardInfo.name}}</h5>
      <p class="card-text"><div v-for="effect in cardInfo.effectsDisplay">{{effect}}</div></p>
      <p class="card-text" v-if="cardInfo.cost">Cost: {{cardInfo.cost[1]}} {{cardInfo.cost[0]}}</p>
    </div>
  </div>
</template>

<script>
export default {
  inheritAttrs:false,
  name: "Card",
  props: {
    cardInfo: Object
  },
  data() {
    return {

    };
  },
  mounted(){
  },
  methods: {
    cardClicked(){
      this.$emit("cardClicked", this)
    }
  }
};
</script>