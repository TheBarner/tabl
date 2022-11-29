<!-- eslint-disable prettier/prettier -->
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Card from './components/CardComponent.vue'
import axios from 'axios'
</script>

<template>
  <div v-if="!tablOk">
    <textarea v-model="tablText" rows="30" cols="100"></textarea>
    <button v-if="connection" @click="submitTablText">Submit</button>
  </div>
  <div v-else-if="gameOver">
    <div v-for="[nickName, resources] in Object.entries(enemyInfo)">{{nickName}}: <div v-for="[resourceName, number] in Object.entries(resources)">{{resourceName}}: {{number}}</div></div>
    <div v-for="[name, number] in Object.entries(resources)">{{name}}: {{number}}</div>
    {{gameOverText}}
  </div>
  <div v-else>
    <div v-if="!ready">
      Tabl file parsed succesfully.
      <input v-model='nickName' :disabled="playerId != null" placeholder="Nickname" type="text">
      <button @click="readyClicked" :disabled="playerId != null">{{readyButtonText}}</button>
    </div>
    <div v-else>
      <div>
        <div v-for="[nickName, resources] in Object.entries(enemyInfo)">{{nickName}}: <div v-for="[resourceName, number] in Object.entries(resources)">{{resourceName}}: {{number}}</div></div>
      </div>
      <br>
      <hr>
      <br>
      <div>
        <div class='card-group'><div class="col" v-for="(value, name) in marketCards"><Card @cardClicked="buyCard" :cardInfo="value"/></div></div>
      </div>
      <br>
      <hr>
      <br>
      <div>
        <div class='card-group'><div class="col" v-for="(value, name) in hand"><Card @cardClicked="selectCard" :cardInfo="value"/></div></div>
        <br>
        <div v-for="[name, number] in Object.entries(resources)">{{name}}: {{number}}</div>
        <div><button @click="endTurn" :disabled="playerId != activePlayer">End turn</button></div>
      </div>
      <br>
      <div v-for="[limitName, max] in Object.entries(limits)">
        {{limitName}} limit: {{currentLimits[limitName]}}/{{max}}
      </div>
      <br>
      <div v-if="discardMode">Select a card to discard!</div>
      <div v-if="scrapMode">Select a card to scrap!</div>
      <div v-if="targetSelection">
        Choose the target of the card:
        <div v-for="enemy in Object.keys(enemyInfo)">
          <button @click="playCardWithTarget(enemy)">{{enemy}}</button>
        </div>
      </div>
      <br>
      Scrap pile:
      <div v-for="scrapCard in scrapPile">
        <Card :cardInfo="scrapCard"/>
      </div>
      <br>
      Discard pile:
      <div v-for="discardCard in discardPile">
        <Card :cardInfo="discardCard"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      marketCards: null,
      displayMarket: false,
      connection: false,
      enemyInfo: null,
      resources: {},
      readyButtonText: "Ready",
      ready: false,
      playerId: null,
      activePlayer: null,
      cardWaitingForTarget: null,
      targetSelection: false,
      tablOk: false,
      tablText: '',
      discardMode: false,
      scrapMode: false,
      scrapPile: [],
      discardPile: [],
      gameOverText: '',
      gameOver: false,
      limits: {},
      currentLimits: {buy: 0, play: 0}
    };
  },
  mounted() {
    this.connection = new WebSocket("ws://localhost:8000/")
    this.connection.onmessage = event => {
      let response = JSON.parse(event.data)
      console.log(response)
      switch(response.messageType) { 

        case "marketRefresh":
          this.marketCards = response.market.display
          break

        case "playerInfo":
          this.resources = response.player.resources
          this.hand = response.player.hand
          this.enemyInfo = response.enemies
          this.scrapPile = response.scrap
          this.discardPile = response.player.deck.discard
          let toDiscard = response.player.toDiscard
          let toScrap = response.player.toScrap
          this.currentLimits.play = response.player.cardsPlayedThisTurn
          this.currentLimits.buy = response.player.cardsBoughtThisTurn
          if(toDiscard <= 0){
            this.discardMode = false
          }
          else{
            this.discardMode = true
          }
          if(toScrap <= 0){
            this.scrapMode = false
          }
          else{
            this.scrapMode = true
          }
          break

        case "playerId":
          this.playerId = response.playerId
          console.log(this.playerId)
          this.readyButtonText = "Waiting for the other players"
          break

        case "beginGame":
          console.log(response)
          this.enemyInfo = response.enemies
          this.resources = response.player.resources
          this.marketCards = response.market
          this.activePlayer = response.activePlayer
          this.hand = response.player.hand
          this.ready = true
          this.scrapPile = response.scrap
          this.limits = response.limits
          break

        case "activePlayer":
          this.activePlayer = response.activePlayer
          if(this.activePlayer == this.playerId){
            if(response.discard > 0)
              this.discardMode = true
          }
          break
        
        case "tablParsed":
          this.tablOk = response.success
          break

        case "endGame":
          if(response.tie){
            this.gameOverText = "The winners are " + Array.from(response.winner, winner => {winner.nickName}).join(", ") + "."
          }
          else{
            this.gameOverText = "The winner is " + response.winner.nickName + "."
          }
          this.gameOver = true

      }
    }
    this.connection.onopen = _ => {
      this.connection.send(JSON.stringify({'action': 'checkTablParsed'}))
    }
  },
  methods:{
    selectCard(card){
      console.log(card.cardInfo)
      if(this.playerId == this.activePlayer){
        if(this.discardMode){
          this.connection.send(JSON.stringify({'action': 'discard', 'cardId': card.cardInfo.id, 'playerId': this.playerId}))
        }
        else if(this.scrapMode){
          this.connection.send(JSON.stringify({'action': 'scrap', 'cardId': card.cardInfo.id, 'playerId': this.playerId}))
        }
        else{
          let targeted = false
          card.cardInfo.whenPlayedArgs.forEach(effect => {
            if(effect.target){
              this.cardWaitingForTarget = card.cardInfo
              this.targetSelection = true
              targeted = true
            }
          })
        if(!targeted)
          this.connection.send(JSON.stringify({'action': 'playCard', 'cardId': card.cardInfo.id, "playerId": this.playerId}))
        }
        
      }
    },
    playCardWithTarget(target){
      this.connection.send(JSON.stringify({'action': 'playCard', 'cardId': this.cardWaitingForTarget.id, "playerId": this.playerId, "target": target}))
      this.targetSelection = false
      this.cardWaitingForTarget = null
    },
    endTurn(){
      if(this.playerId == this.activePlayer)
        this.connection.send(JSON.stringify({'action': 'endTurn', "playerId": this.playerId}))
    },
    buyCard(card){
      console.log({"action": "buyCard", "card": card})
      if(this.playerId == this.activePlayer)
        this.connection.send(JSON.stringify({"action": "buyCard", "cardId": card.cardInfo.id, "playerId": this.playerId}))
    },
    readyClicked(){
      if(this.playerId == this.activePlayer)
        this.connection.send(JSON.stringify({'action': 'ready', 'nickName': this.nickName}))
    },
    submitTablText(){
      this.connection.send(JSON.stringify({'action': 'gameFile', 'tablText': this.tablText}))
    }
  }
};
</script>

<style scoped>

</style>
